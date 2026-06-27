"""
House 7 — Kalatra Bhava (House of Spouse, Partnership, Desire)
Karakas: Venus (wife/love), Jupiter (husband/wisdom in relationships)
Vargas:  D-1, D-9 (Navamsha — most important for marriage), D-60
"""
from __future__ import annotations
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP, EXALTATION, OWN_SIGNS
from .base import analyze_house, finalize

HOUSE_CONFIG = {
    'number': 7,
    'karakas': ['Venus', 'Jupiter'],
    'primary_karaka': 'Venus',
    'natural_significations': [
        'Spouse, life partner, and marriage', 'Business partnerships and joint ventures',
        'Desires and passion', 'Open enemies and public adversaries',
        'Foreign countries and long journeys', 'Sexual vitality and pleasures',
        'Trade, commerce, and negotiations', 'Contractual agreements',
    ],
    'body_parts': ['Loins', 'Genitals', 'Kidneys', 'Lower back'],
    'preferred_vargas': [1, 9, 60],
}


def _significations(positions: dict, lagna_sign: int, house_sign: int,
                    lord: str, dasha: dict) -> dict:
    venus = positions.get('VENUS', {})
    jup   = positions.get('JUPITER', {})

    def _house(sign: int) -> int: return (sign - lagna_sign) % 12 + 1
    def _strong(p: str, s: int) -> bool:
        return s in OWN_SIGNS.get(p, []) or s == EXALTATION.get(p)

    venus_sign = venus.get('sign_index', 0)
    jup_sign   = jup.get('sign_index', 0)
    lord_sign  = positions.get(PLANET_KEY_MAP.get(lord, lord.upper()), {}).get('sign_index', 0)

    venus_house = _house(venus_sign)
    jup_house   = _house(jup_sign)
    lord_house  = _house(lord_sign)

    venus_strong = _strong('Venus', venus_sign)
    jup_strong   = _strong('Jupiter', jup_sign)
    lord_strong  = _strong(lord, lord_sign)

    # Malefics in 7th can delay/affect marriage
    occupants_7 = [p for p, d in positions.items()
                   if p != 'LAGNA' and d['sign_index'] == house_sign]
    malefic_in_7 = any(p in ('MARS','SATURN','RAHU','KETU') for p in occupants_7)

    # Marriage / spouse
    marriage_score = 50
    if venus_strong:     marriage_score += 20
    if jup_strong:       marriage_score += 10
    if lord_strong:      marriage_score += 15
    if venus_house in (1,2,7,9,11): marriage_score += 10
    if venus_house in (6,8,12):     marriage_score -= 15
    if malefic_in_7:               marriage_score -= 10
    if venus.get('is_retrograde'): marriage_score -= 5
    marriage_score = max(0, min(100, marriage_score))

    # Business partnerships
    partnership_score = 50
    if lord_strong:  partnership_score += 20
    if venus_strong: partnership_score += 10
    if lord_house in (1,7,10,11): partnership_score += 10
    if lord_house in (6,8,12):    partnership_score -= 15
    partnership_score = max(0, min(100, partnership_score))

    # Desire / passion
    desire_score = 50
    if venus_strong: desire_score += 20
    if venus_house in (7,5,2): desire_score += 10
    desire_score = max(0, min(100, desire_score))

    # Spouse qualities (Navamsha is primary — we give a note)
    spouse_desc = {
        0: 'Energetic, independent, and assertive spouse',
        1: 'Stable, sensual, artistic spouse who values security',
        2: 'Intellectual, communicative, dual-natured spouse',
        3: 'Nurturing, emotional, homebody spouse',
        4: 'Proud, authoritative, generous spouse with leadership qualities',
        5: 'Analytical, health-conscious, service-oriented spouse',
        6: 'Diplomatic, beautiful, harmonious and relationship-focused spouse',
        7: 'Intense, secretive, magnetic, and transformative spouse',
        8: 'Philosophical, adventurous, spiritual spouse',
        9: 'Disciplined, ambitious, career-focused spouse',
        10: 'Unconventional, humanitarian, intellectual spouse',
        11: 'Spiritual, compassionate, artistic, and intuitive spouse',
    }

    def _sl(s: int) -> str:
        if s >= 70: return 'Strong'
        if s >= 45: return 'Moderate'
        return 'Weak'

    return {
        'marriage_and_spouse': {
            'score': marriage_score,
            'strength': _sl(marriage_score),
            'indicators': [
                f'Venus (Strikalatra karaka) in {SIGNS[venus_sign]} (house {venus_house})',
                f'Jupiter (Jaya karaka) in {SIGNS[jup_sign]} (house {jup_house})',
                f'7th lord {lord} in {SIGNS[lord_sign]} (house {lord_house})',
                f'{"Malefics in 7th may cause delay/challenges" if malefic_in_7 else "No malefic occupation of 7th"}',
            ],
            'spouse_nature': spouse_desc.get(house_sign, 'Determined by 7th house sign and occupants'),
            'note': 'D-9 (Navamsha) is the primary chart for marriage analysis',
        },
        'business_partnerships': {
            'score': partnership_score,
            'strength': _sl(partnership_score),
            'indicators': [
                f'7th lord {lord} in house {lord_house} — partnership style',
                f'Venus {"strong" if venus_strong else "moderate"} — collaborative energy',
            ],
        },
        'desires_and_passion': {
            'score': desire_score,
            'strength': _sl(desire_score),
            'indicators': [
                f'Venus in {SIGNS[venus_sign]} (house {venus_house}) — desire nature',
                '7th house rules Kama (desires) among the four life goals',
            ],
        },
    }


def compute(
    date_str: str, time_str: str,
    latitude: float, longitude: float,
    timezone_str: str, place_name: str = '',
    current_date_str: str | None = None,
) -> dict:
    result = analyze_house(HOUSE_CONFIG, date_str, time_str, latitude, longitude,
                           timezone_str, place_name, current_date_str)
    result['significations'] = _significations(
        result['_positions'], result['_lagna_sign'],
        result['_house_sign'], result['_lord'], result['_dasha'])
    return finalize(result)
