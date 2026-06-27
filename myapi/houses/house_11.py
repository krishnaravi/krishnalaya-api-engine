"""
House 11 — Labha Bhava (House of Gains, Fulfillment, Elder Siblings)
Karaka: Jupiter (gains, expansion, fulfillment)
Vargas:  D-1, D-9, D-10 (income from career), D-24
Note: Upachaya — all planets including malefics give gains over time.
"""
from __future__ import annotations
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP, EXALTATION, OWN_SIGNS
from .base import analyze_house, finalize

HOUSE_CONFIG = {
    'number': 11,
    'karakas': ['Jupiter'],
    'primary_karaka': 'Jupiter',
    'natural_significations': [
        'Financial gains and income', 'Fulfillment of wishes and desires',
        'Elder siblings and friends', 'Social networks and communities',
        'Profits from business and investments', 'Recognition and awards',
        'Left ear', 'Ankles and shins',
    ],
    'body_parts': ['Left ear', 'Ankles', 'Shins', 'Calf muscles'],
    'preferred_vargas': [1, 9, 10, 24],
}


def _significations(positions: dict, lagna_sign: int, house_sign: int,
                    lord: str, dasha: dict) -> dict:
    jup = positions.get('JUPITER', {})

    def _house(sign: int) -> int: return (sign - lagna_sign) % 12 + 1
    def _strong(p: str, s: int) -> bool:
        return s in OWN_SIGNS.get(p, []) or s == EXALTATION.get(p)

    jup_sign  = jup.get('sign_index', 0)
    lord_sign = positions.get(PLANET_KEY_MAP.get(lord, lord.upper()), {}).get('sign_index', 0)

    jup_house  = _house(jup_sign)
    lord_house = _house(lord_sign)

    jup_strong  = _strong('Jupiter', jup_sign)
    lord_strong = _strong(lord, lord_sign)

    # Occupants of 11th — all planets give gains in Upachaya house over time
    occupants_11 = [p for p, d in positions.items()
                    if p != 'LAGNA' and d['sign_index'] == house_sign]

    # Financial gains
    gains_score = 50
    if jup_strong:   gains_score += 20
    if lord_strong:  gains_score += 20
    if jup_house in (11, 5, 1, 9): gains_score += 10
    if lord_house in (6, 8, 12):   gains_score -= 15
    if len(occupants_11) > 0:      gains_score += 5   # planets in 11th generally help gains
    gains_score = max(0, min(100, gains_score))

    # Wishes and desires fulfilled
    wish_score = 50
    if jup_strong:  wish_score += 20
    if lord_strong: wish_score += 15
    if jup_house in (11, 1, 5): wish_score += 10
    wish_score = max(0, min(100, wish_score))

    # Elder siblings and social network
    sibling_score = 50
    if lord_strong: sibling_score += 15
    if lord_house in (11, 3, 1): sibling_score += 10
    if lord_house in (6, 8, 12): sibling_score -= 15
    sibling_score = max(0, min(100, sibling_score))

    # Income sources from occupation of 11th
    income_indicators = []
    planet_income = {
        'SUN': 'Government, authority, solar industries',
        'MOON': 'Public, hospitality, liquids, maternal businesses',
        'MARS': 'Real estate, engineering, military, sports',
        'MERCURY': 'Trade, communication, IT, education, accounting',
        'JUPITER': 'Finance, teaching, law, religion, advisory',
        'VENUS': 'Arts, luxury, entertainment, beauty',
        'SATURN': 'Mining, agriculture, service, construction',
        'RAHU': 'Foreign sources, technology, speculation',
        'KETU': 'Spiritual economy, alternative income',
    }
    for p in occupants_11:
        theme = planet_income.get(p)
        if theme:
            income_indicators.append(f'{p.title()}: {theme}')

    def _sl(s: int) -> str:
        if s >= 70: return 'Strong'
        if s >= 45: return 'Moderate'
        return 'Weak'

    return {
        'financial_gains_and_income': {
            'score': gains_score,
            'strength': _sl(gains_score),
            'indicators': [
                f'Jupiter (Labhakaraka) in {SIGNS[jup_sign]} (house {jup_house})',
                f'11th lord {lord} in {SIGNS[lord_sign]} (house {lord_house})',
                f'11th house occupants: {[p.title() for p in occupants_11] or ["None"]}',
            ],
            'income_sources': income_indicators or [f'{lord} indicates {planet_income.get(PLANET_KEY_MAP.get(lord, ""), "varied income")}'],
            'note': 'Upachaya house — all planets improve gains over time with sustained effort',
        },
        'wish_fulfillment': {
            'score': wish_score,
            'strength': _sl(wish_score),
            'indicators': [
                f'Jupiter {"strong" if jup_strong else "moderate"} — {"abundant fulfillment" if wish_score >= 65 else "moderate wish fulfillment"}',
                f'11th lord {lord} — desire manifestation capacity',
            ],
        },
        'elder_siblings_and_friends': {
            'score': sibling_score,
            'strength': _sl(sibling_score),
            'indicators': [
                f'11th lord {lord} in house {lord_house}',
                f'{"Supportive" if sibling_score >= 60 else "Moderate"} relations with elder siblings and social circles',
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
