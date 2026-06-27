"""
House 3 — Sahaja Bhava / Vikrama Bhava (Siblings, Courage, Communication)
Karakas: Mars (siblings, courage), Mercury (communication, skills)
Vargas:  D-1, D-3 (Drekkana/siblings), D-9, D-24 (skills)
"""
from __future__ import annotations
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP, EXALTATION, OWN_SIGNS
from .base import analyze_house, finalize

HOUSE_CONFIG = {
    'number': 3,
    'karakas': ['Mars', 'Mercury'],
    'primary_karaka': 'Mars',
    'natural_significations': [
        'Siblings (especially younger)', 'Courage, valor, and initiative',
        'Communication, writing, and media', 'Short journeys and local travel',
        'Skills, arts, and crafts', 'Arms, shoulders, and hands',
        'Efforts, hard work, and persistence', 'Neighbours and immediate community',
    ],
    'body_parts': ['Arms', 'Shoulders', 'Hands', 'Collar bones', 'Neck (lower)', 'Ears'],
    'preferred_vargas': [1, 3, 9, 24],
}


def _significations(positions: dict, lagna_sign: int, house_sign: int,
                    lord: str, dasha: dict) -> dict:
    mars = positions.get('MARS', {})
    merc = positions.get('MERCURY', {})

    mars_sign = mars.get('sign_index', 0)
    merc_sign = merc.get('sign_index', 0)
    mars_house = (mars_sign - lagna_sign) % 12 + 1
    merc_house = (merc_sign - lagna_sign) % 12 + 1

    def _strong(planet: str, sign: int) -> bool:
        return sign in OWN_SIGNS.get(planet, []) or sign == EXALTATION.get(planet)

    mars_strong = _strong('Mars', mars_sign)
    merc_strong = _strong('Mercury', merc_sign)
    lord_sign   = positions.get(PLANET_KEY_MAP.get(lord, lord.upper()), {}).get('sign_index', 0)
    lord_house  = (lord_sign - lagna_sign) % 12 + 1
    lord_strong = _strong(lord, lord_sign)

    siblings_score = 50
    if mars_strong:        siblings_score += 15
    if lord_strong:        siblings_score += 15
    if mars_house == 3:    siblings_score += 10
    if lord_house in (1,3,11): siblings_score += 10
    if mars_house in (6,8,12): siblings_score -= 20
    siblings_score = max(0, min(100, siblings_score))

    courage_score = 50
    if mars_strong:        courage_score += 25
    if mars_house in (1,3,6,10,11): courage_score += 15
    if mars_house in (8,12):        courage_score -= 10
    if mars.get('is_retrograde'):   courage_score -= 5
    courage_score = max(0, min(100, courage_score))

    comm_score = 50
    if merc_strong:         comm_score += 20
    if merc_house in (1,3,6,10,11): comm_score += 15
    if merc_house in (8,12):        comm_score -= 10
    comm_score = max(0, min(100, comm_score))

    skills_score = 50
    if merc_strong:  skills_score += 15
    if mars_strong:  skills_score += 10
    if merc_house in (3, 10, 11): skills_score += 10
    skills_score = max(0, min(100, skills_score))

    def _sl(s: int) -> str:
        if s >= 70: return 'Strong'
        if s >= 45: return 'Moderate'
        return 'Weak'

    return {
        'siblings': {
            'score': siblings_score,
            'strength': _sl(siblings_score),
            'indicators': [
                f'Mars (siblings karaka) in {SIGNS[mars_sign]} (house {mars_house})',
                f'3rd lord {lord} in house {lord_house}',
            ],
        },
        'courage_and_initiative': {
            'score': courage_score,
            'strength': _sl(courage_score),
            'indicators': [
                f'Mars in {SIGNS[mars_sign]} (house {mars_house}) — {"strong parakrama" if courage_score >= 60 else "moderate courage"}',
                'Strong Mars in 3rd → excellent initiative and valor',
            ],
        },
        'communication_and_writing': {
            'score': comm_score,
            'strength': _sl(comm_score),
            'indicators': [
                f'Mercury in {SIGNS[merc_sign]} (house {merc_house})',
                f'{"Excellent" if comm_score >= 70 else "Average"} writing and communication skills',
            ],
        },
        'skills_and_arts': {
            'score': skills_score,
            'strength': _sl(skills_score),
            'indicators': [
                f'Mercury {"strong" if merc_strong else "moderate"} — technical/artistic skills',
                f'Mars {"strong" if mars_strong else "moderate"} — craft and execution ability',
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
