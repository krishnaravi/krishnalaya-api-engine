"""
House 2 — Dhana Bhava (House of Wealth & Speech)
Karakas: Jupiter (wealth, expansion), Mercury (speech, business)
Vargas:  D-1, D-2 (Hora/wealth), D-9, D-24 (learning)
"""
from __future__ import annotations
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP, EXALTATION, OWN_SIGNS
from .base import analyze_house, finalize

HOUSE_CONFIG = {
    'number': 2,
    'karakas': ['Jupiter', 'Mercury'],
    'primary_karaka': 'Jupiter',
    'natural_significations': [
        'Wealth, savings, and accumulated resources', 'Speech, voice, and communication style',
        'Family lineage and family values', 'Face, eyes, teeth, and tongue',
        'Food and dietary habits', 'Self-worth and values',
        'Financial security and net worth', 'Memory and early education',
    ],
    'body_parts': ['Face', 'Right eye', 'Teeth', 'Tongue', 'Throat', 'Neck'],
    'preferred_vargas': [1, 2, 9, 24],
}


def _significations(positions: dict, lagna_sign: int, house_sign: int,
                    lord: str, dasha: dict) -> dict:
    jup  = positions.get('JUPITER', {})
    merc = positions.get('MERCURY', {})

    jup_sign  = jup.get('sign_index', 0)
    merc_sign = merc.get('sign_index', 0)
    jup_house  = (jup_sign  - lagna_sign) % 12 + 1
    merc_house = (merc_sign - lagna_sign) % 12 + 1

    def _strong(planet: str, sign: int) -> bool:
        return sign in OWN_SIGNS.get(planet, []) or sign == EXALTATION.get(planet)

    jup_strong  = _strong('Jupiter', jup_sign)
    merc_strong = _strong('Mercury', merc_sign)
    lord_sign   = positions.get(PLANET_KEY_MAP.get(lord, lord.upper()), {}).get('sign_index', 0)
    lord_house  = (lord_sign - lagna_sign) % 12 + 1
    lord_strong = _strong(lord, lord_sign)

    wealth_score = 50
    if jup_strong:           wealth_score += 20
    if lord_strong:          wealth_score += 20
    if jup_house in (1,2,5,9,11):  wealth_score += 10
    if jup_house in (6,8,12):      wealth_score -= 20
    if lord_house in (6,8,12):     wealth_score -= 15
    wealth_score = max(0, min(100, wealth_score))

    speech_score = 50
    if merc_strong:          speech_score += 20
    if merc_house in (1,2,3,10,11): speech_score += 15
    if merc_house in (6,8,12):      speech_score -= 15
    speech_score = max(0, min(100, speech_score))

    family_score = 50
    if lord_strong: family_score += 20
    if lord_house in (1,2,4,5):  family_score += 10
    family_score = max(0, min(100, family_score))

    def _sl(s: int) -> str:
        if s >= 70: return 'Strong'
        if s >= 45: return 'Moderate'
        return 'Weak'

    return {
        'wealth_and_savings': {
            'score': wealth_score,
            'strength': _sl(wealth_score),
            'indicators': [
                f'Jupiter (wealth karaka) in {SIGNS[jup_sign]} (house {jup_house}) — {"strong" if jup_strong else "needs support"}',
                f'2nd lord {lord} in house {lord_house} — {"well-placed" if lord_house in (1,2,4,5,9,10,11) else "challenging"}',
            ],
            'dhana_yoga': jup_strong and lord_strong,
        },
        'speech_and_communication': {
            'score': speech_score,
            'strength': _sl(speech_score),
            'indicators': [
                f'Mercury (speech karaka) in {SIGNS[merc_sign]} (house {merc_house})',
                f'Mercury {"strong" if merc_strong else "moderate/weak"} — speech quality influenced',
            ],
        },
        'family_and_lineage': {
            'score': family_score,
            'strength': _sl(family_score),
            'house_sign': SIGNS[house_sign],
            'indicators': [
                f'2nd lord {lord} in {SIGNS[lord_sign]} (house {lord_house})',
                f'House sign {SIGNS[house_sign]} represents family nature and values',
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
