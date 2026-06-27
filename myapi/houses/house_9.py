"""
House 9 — Dharma Bhava (House of Dharma, Father, Luck, Higher Wisdom)
Karakas: Jupiter (guru, higher learning, dharma), Sun (father)
Vargas:  D-1, D-9, D-12 (parents), D-24 (higher education)
"""
from __future__ import annotations
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP, EXALTATION, OWN_SIGNS
from .base import analyze_house, finalize

HOUSE_CONFIG = {
    'number': 9,
    'karakas': ['Jupiter', 'Sun'],
    'primary_karaka': 'Jupiter',
    'natural_significations': [
        'Father and paternal figures', 'Guru, preceptor, and spiritual teacher',
        'Luck, fortune, and divine grace', 'Higher education and philosophical studies',
        'Religion, dharma, and righteous conduct', 'Long-distance travel and pilgrimage',
        'Foreign connections and cultures', 'Law and legal principles',
    ],
    'body_parts': ['Thighs', 'Hips', 'Sciatic nerve', 'Arterial system'],
    'preferred_vargas': [1, 9, 12, 24],
}


def _significations(positions: dict, lagna_sign: int, house_sign: int,
                    lord: str, dasha: dict) -> dict:
    jup = positions.get('JUPITER', {})
    sun = positions.get('SUN', {})

    def _house(sign: int) -> int: return (sign - lagna_sign) % 12 + 1
    def _strong(p: str, s: int) -> bool:
        return s in OWN_SIGNS.get(p, []) or s == EXALTATION.get(p)

    jup_sign  = jup.get('sign_index', 0)
    sun_sign  = sun.get('sign_index', 0)
    lord_sign = positions.get(PLANET_KEY_MAP.get(lord, lord.upper()), {}).get('sign_index', 0)

    jup_house  = _house(jup_sign)
    sun_house  = _house(sun_sign)
    lord_house = _house(lord_sign)

    jup_strong  = _strong('Jupiter', jup_sign)
    sun_strong  = _strong('Sun', sun_sign)
    lord_strong = _strong(lord, lord_sign)

    # Father
    father_score = 50
    if sun_strong:   father_score += 20
    if sun_house in (1, 9, 10, 11): father_score += 15
    if sun_house in (6, 8, 12):     father_score -= 20
    if jup_strong:   father_score += 10
    father_score = max(0, min(100, father_score))

    # Guru / Spiritual teacher
    guru_score = 50
    if jup_strong:   guru_score += 25
    if jup_house in (1, 5, 9): guru_score += 15
    if jup_house in (6, 8, 12): guru_score -= 15
    if lord_strong:  guru_score += 10
    guru_score = max(0, min(100, guru_score))

    # Luck and fortune (Bhagya)
    luck_score = 50
    if jup_strong:  luck_score += 20
    if lord_strong: luck_score += 20
    if jup_house in (5, 9, 1, 11): luck_score += 10
    if lord_house in (6, 8, 12):   luck_score -= 15
    luck_score = max(0, min(100, luck_score))

    # Higher education and religion
    dharma_score = 50
    if jup_strong:   dharma_score += 20
    if lord_strong:  dharma_score += 15
    if jup_house in (9, 5, 1, 4): dharma_score += 10
    dharma_score = max(0, min(100, dharma_score))

    def _sl(s: int) -> str:
        if s >= 70: return 'Strong'
        if s >= 45: return 'Moderate'
        return 'Weak'

    return {
        'father_and_authority': {
            'score': father_score,
            'strength': _sl(father_score),
            'indicators': [
                f'Sun (Pitrukaraka) in {SIGNS[sun_sign]} (house {sun_house})',
                f'9th lord {lord} in house {lord_house}',
                f'Father relationship {"supported" if father_score >= 60 else "may have challenges"}',
            ],
        },
        'guru_and_spiritual_teacher': {
            'score': guru_score,
            'strength': _sl(guru_score),
            'indicators': [
                f'Jupiter (Gurukaraka) in {SIGNS[jup_sign]} (house {jup_house})',
                f'{"Excellent" if jup_strong else "Average"} for receiving guru\'s grace and guidance',
            ],
        },
        'luck_fortune_and_bhagya': {
            'score': luck_score,
            'strength': _sl(luck_score),
            'indicators': [
                f'9th lord {lord} in {SIGNS[lord_sign]} (house {lord_house})',
                f'Jupiter {"strong" if jup_strong else "moderate"} — {"abundant blessings" if luck_score >= 65 else "moderate fortune"}',
            ],
            'bhagya_classification': (
                'Raja Bhagya — exceptional fortune' if luck_score >= 80 else
                'Uttama Bhagya — good fortune' if luck_score >= 65 else
                'Madhyama Bhagya — average fortune' if luck_score >= 45 else
                'Alpa Bhagya — needs effort to realize fortune'
            ),
        },
        'dharma_and_higher_learning': {
            'score': dharma_score,
            'strength': _sl(dharma_score),
            'indicators': [
                f'Jupiter in {SIGNS[jup_sign]} — philosophical and religious orientation',
                f'9th house sign {SIGNS[house_sign]} — nature of dharmic path and beliefs',
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
