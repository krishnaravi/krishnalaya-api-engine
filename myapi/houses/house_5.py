"""
House 5 — Putra Bhava (House of Children, Intelligence, Creativity)
Karaka: Jupiter (children, wisdom, dharmic merit)
Vargas: D-1, D-9, D-24 (education), D-60 (past karma)
"""
from __future__ import annotations
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP, EXALTATION, OWN_SIGNS
from .base import analyze_house, finalize

HOUSE_CONFIG = {
    'number': 5,
    'karakas': ['Jupiter'],
    'primary_karaka': 'Jupiter',
    'natural_significations': [
        'Children and progeny', 'Intelligence, wisdom, and higher learning',
        'Creative expression and artistic talents', 'Romantic love and courtship',
        'Speculation, gambling, and investments', 'Past-life merit (Purva Punya)',
        'Mantra, sacred knowledge, and spiritual practices', 'Stomach and digestive system',
    ],
    'body_parts': ['Upper abdomen', 'Stomach', 'Liver (with 6th)', 'Spine'],
    'preferred_vargas': [1, 9, 24, 60],
}


def _significations(positions: dict, lagna_sign: int, house_sign: int,
                    lord: str, dasha: dict) -> dict:
    jup = positions.get('JUPITER', {})

    def _house(sign: int) -> int: return (sign - lagna_sign) % 12 + 1
    def _strong(p: str, s: int) -> bool:
        return s in OWN_SIGNS.get(p, []) or s == EXALTATION.get(p)

    jup_sign   = jup.get('sign_index', 0)
    lord_sign  = positions.get(PLANET_KEY_MAP.get(lord, lord.upper()), {}).get('sign_index', 0)
    jup_house  = _house(jup_sign)
    lord_house = _house(lord_sign)

    jup_strong  = _strong('Jupiter', jup_sign)
    lord_strong = _strong(lord, lord_sign)

    # Children
    children_score = 50
    if jup_strong:  children_score += 25
    if jup_house in (5, 7, 9, 11): children_score += 15
    if jup_house in (6, 8, 12):    children_score -= 20
    if jup.get('is_retrograde'):   children_score -= 10
    if lord_strong:  children_score += 10
    children_score = max(0, min(100, children_score))

    # Intelligence
    intel_score = 50
    if jup_strong: intel_score += 20
    if lord_strong: intel_score += 15
    sun = positions.get('SUN', {})
    sun_house = _house(sun.get('sign_index', 0))
    if sun_house == 5: intel_score += 10
    intel_score = max(0, min(100, intel_score))

    # Creativity and romance
    creativity_score = 50
    venus = positions.get('VENUS', {})
    venus_sign = venus.get('sign_index', 0)
    venus_house = _house(venus_sign)
    venus_strong = _strong('Venus', venus_sign)
    if venus_strong: creativity_score += 15
    if venus_house in (5, 7, 9, 11): creativity_score += 10
    if jup_strong: creativity_score += 10
    creativity_score = max(0, min(100, creativity_score))

    # Past life merit / Purva Punya
    punya_score = 50
    if jup_strong: punya_score += 20
    if lord_strong: punya_score += 10
    if jup_house in (5, 9, 1): punya_score += 10
    punya_score = max(0, min(100, punya_score))

    def _sl(s: int) -> str:
        if s >= 70: return 'Strong'
        if s >= 45: return 'Moderate'
        return 'Weak'

    return {
        'children_and_progeny': {
            'score': children_score,
            'strength': _sl(children_score),
            'indicators': [
                f'Jupiter (Putrakaraka) in {SIGNS[jup_sign]} (house {jup_house})',
                f'5th lord {lord} in house {lord_house}',
                f'Jupiter {"strong" if jup_strong else "weakened"} — {"favourable" if children_score >= 60 else "challenges possible"} for children',
            ],
            'putrakaraka': 'Jupiter',
        },
        'intelligence_and_wisdom': {
            'score': intel_score,
            'strength': _sl(intel_score),
            'indicators': [
                f'Jupiter in {SIGNS[jup_sign]} (house {jup_house}) — wisdom and higher learning',
                f'5th lord {lord} in {SIGNS[lord_sign]} — intellectual capacity',
            ],
        },
        'creativity_and_romance': {
            'score': creativity_score,
            'strength': _sl(creativity_score),
            'indicators': [
                f'Venus in {SIGNS[venus_sign]} (house {venus_house}) — romantic potential',
                f'Jupiter in house {jup_house} — creative inspiration',
            ],
        },
        'purva_punya_past_karma': {
            'score': punya_score,
            'strength': _sl(punya_score),
            'indicators': [
                f'5th house sign: {SIGNS[house_sign]} — nature of past-life merit',
                f'Jupiter {"strong" if jup_strong else "moderate"} — {"rich" if punya_score >= 65 else "average"} accumulated merit',
            ],
            'note': 'Strong 5th house = good past-life karma supporting present life opportunities',
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
