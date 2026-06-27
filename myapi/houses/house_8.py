"""
House 8 — Randhra Bhava (House of Longevity, Occult, Transformation)
Karaka: Saturn (longevity, death, delay, obstacles)
Vargas: D-1, D-9, D-60 (past karma)
Note: Dusthana — difficult house; natural home of occult sciences (Anga: Scorpio).
"""
from __future__ import annotations
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP, EXALTATION, OWN_SIGNS
from .base import analyze_house, finalize

HOUSE_CONFIG = {
    'number': 8,
    'karakas': ['Saturn'],
    'primary_karaka': 'Saturn',
    'natural_significations': [
        'Longevity, lifespan, and death', 'Sudden events and transformations',
        'Occult, mysticism, and hidden knowledge', 'Inheritance and legacies',
        'Joint finances and others\' resources', 'Chronic illness and acute crises',
        'Research, investigation, and deep inquiry', 'Obstacles and delays',
    ],
    'body_parts': ['Genitals', 'Anus', 'Colon', 'Excretory system'],
    'preferred_vargas': [1, 9, 60],
}


def _significations(positions: dict, lagna_sign: int, house_sign: int,
                    lord: str, dasha: dict) -> dict:
    sat = positions.get('SATURN', {})

    def _house(sign: int) -> int: return (sign - lagna_sign) % 12 + 1
    def _strong(p: str, s: int) -> bool:
        return s in OWN_SIGNS.get(p, []) or s == EXALTATION.get(p)

    sat_sign  = sat.get('sign_index', 0)
    lord_sign = positions.get(PLANET_KEY_MAP.get(lord, lord.upper()), {}).get('sign_index', 0)

    sat_house  = _house(sat_sign)
    lord_house = _house(lord_sign)

    sat_strong  = _strong('Saturn', sat_sign)
    lord_strong = _strong(lord, lord_sign)

    # Longevity strength (Ayurdaya)
    long_score = 50
    if sat_strong:    long_score += 20
    if lord_strong:   long_score += 15
    if sat_house in (8, 1, 10): long_score += 10  # Saturn in kendra/8th can give long life
    if lord_house in (6, 8, 12): long_score -= 10
    # Benefics aspecting 8th improve longevity
    jup = positions.get('JUPITER', {})
    jup_sign = jup.get('sign_index', 0)
    jup_from_8 = (house_sign - jup_sign) % 12 + 1
    if jup_from_8 in (5, 9, 7):  long_score += 10   # Jupiter aspects 8th
    long_score = max(0, min(100, long_score))

    # Occult and hidden knowledge
    occult_score = 50
    ketu = positions.get('KETU', {})
    rahu = positions.get('RAHU', {})
    ketu_sign = ketu.get('sign_index', 0)
    ketu_house = _house(ketu_sign)
    if ketu_house in (8, 12): occult_score += 20   # Ketu in 8/12 = strong mystic
    if sat_strong:  occult_score += 10
    if lord_house in (8, 12): occult_score += 10
    occult_score = max(0, min(100, occult_score))

    # Sudden events / transformations (8th house events)
    sudden_score = 50   # Score represents intensity, not positivity
    occupants_8 = [p for p, d in positions.items()
                   if p != 'LAGNA' and d['sign_index'] == house_sign]
    if 'RAHU' in occupants_8 or 'KETU' in occupants_8: sudden_score += 20
    if 'MARS' in occupants_8: sudden_score += 15

    # Inheritance / others' resources
    inherit_score = 50
    if lord_strong:  inherit_score += 15
    if sat_strong:   inherit_score += 10
    if lord_house in (1, 2, 9, 11): inherit_score += 10
    inherit_score = max(0, min(100, inherit_score))

    def _sl(s: int) -> str:
        if s >= 70: return 'Strong'
        if s >= 45: return 'Moderate'
        return 'Weak'

    return {
        'longevity_and_lifespan': {
            'score': long_score,
            'strength': _sl(long_score),
            'indicators': [
                f'Saturn (Ayurkaraka) in {SIGNS[sat_sign]} (house {sat_house})',
                f'8th lord {lord} in {SIGNS[lord_sign]} (house {lord_house})',
                f'Jupiter aspect on 8th: {"present" if jup_from_8 in (5,9,7) else "absent"} — {"protective" if jup_from_8 in (5,9,7) else "no Jupiter protection"}',
            ],
            'note': 'Full Ayurdasamsha (D-8) analysis needed for precise longevity calculation',
        },
        'occult_and_mysticism': {
            'score': occult_score,
            'strength': _sl(occult_score),
            'indicators': [
                f'Ketu in {SIGNS[ketu_sign]} (house {ketu_house}) — {"strong mystic tendency" if ketu_house in (8,12) else "moderate occult interest"}',
                f'8th house sign {SIGNS[house_sign]} — nature of mystical experiences',
            ],
        },
        'sudden_events_and_transformation': {
            'score': sudden_score,
            'strength': 'High intensity' if sudden_score >= 65 else 'Moderate',
            'indicators': [
                f'8th house occupants: {[p.title() for p in occupants_8] or ["None"]}',
                'High-intensity events are more likely when malefics occupy or aspect 8th',
            ],
            'note': '8th house themes include sudden ups/downs, hidden matters, and radical change',
        },
        'inheritance_and_joint_resources': {
            'score': inherit_score,
            'strength': _sl(inherit_score),
            'indicators': [
                f'8th lord {lord} in house {lord_house}',
                f'{"Good" if inherit_score >= 60 else "Average"} indications for inheritance and joint finances',
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
