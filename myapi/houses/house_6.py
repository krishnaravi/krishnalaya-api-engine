"""
House 6 — Ari Bhava (House of Enemies, Disease, Service)
Karakas: Mars (enemies, competition), Saturn (chronic illness, service)
Vargas:  D-1, D-9, D-24, D-60
Note: Dusthana but also Upachaya — planets here can give victory over enemies.
"""
from __future__ import annotations
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP, EXALTATION, OWN_SIGNS
from .base import analyze_house, finalize

HOUSE_CONFIG = {
    'number': 6,
    'karakas': ['Mars', 'Saturn'],
    'primary_karaka': 'Mars',
    'natural_significations': [
        'Enemies, opponents, and rivals', 'Disease, illness, and health challenges',
        'Debt, loans, and financial liabilities', 'Service, employment, and daily work',
        'Legal disputes and litigation', 'Maternal uncle (Mama)',
        'Pets and small animals', 'Digestive system and assimilation',
    ],
    'body_parts': ['Lower abdomen', 'Intestines', 'Digestive tract', 'Navel region'],
    'preferred_vargas': [1, 9, 24, 60],
}

_UPACHAYA_PLANETS = {'Mars', 'Saturn', 'Sun', 'Mercury'}


def _significations(positions: dict, lagna_sign: int, house_sign: int,
                    lord: str, dasha: dict) -> dict:
    mars = positions.get('MARS', {})
    sat  = positions.get('SATURN', {})

    def _house(sign: int) -> int: return (sign - lagna_sign) % 12 + 1
    def _strong(p: str, s: int) -> bool:
        return s in OWN_SIGNS.get(p, []) or s == EXALTATION.get(p)

    mars_sign = mars.get('sign_index', 0)
    sat_sign  = sat.get('sign_index', 0)
    lord_sign = positions.get(PLANET_KEY_MAP.get(lord, lord.upper()), {}).get('sign_index', 0)

    mars_house = _house(mars_sign)
    sat_house  = _house(sat_sign)
    lord_house = _house(lord_sign)

    mars_strong = _strong('Mars', mars_sign)
    sat_strong  = _strong('Saturn', sat_sign)
    lord_strong = _strong(lord, lord_sign)

    # Planets in 6th house (Upachaya — malefics good here)
    occupants_6 = [p for p, d in positions.items()
                   if p != 'LAGNA' and d['sign_index'] == house_sign]
    malefic_in_6 = any(p in ('MARS','SATURN','SUN','RAHU','KETU') for p in occupants_6)

    # Enemy defeat / competition
    enemy_score = 50
    if mars_strong:   enemy_score += 20
    if malefic_in_6:  enemy_score += 15   # malefics in 6th = victory over enemies
    if mars_house in (3, 6, 10, 11): enemy_score += 10
    if lord_strong: enemy_score += 10
    enemy_score = max(0, min(100, enemy_score))

    # Health / disease resistance
    health_score = 50
    # Strong 6th house lord = ability to overcome illness
    if lord_strong:  health_score += 15
    if sat_strong:   health_score += 10
    if lord_house in (6, 8, 12): health_score -= 15  # lord in dusthana weakens
    if malefic_in_6: health_score -= 10              # malefics in 6th indicate health challenges
    health_score = max(0, min(100, health_score))

    # Debt and legal
    debt_score = 50
    if lord_strong: debt_score += 10
    if lord_house in (1,5,9,10,11): debt_score += 10  # good lord placement = resolves debt
    if lord_house in (6,8,12): debt_score -= 15
    debt_score = max(0, min(100, debt_score))

    # Service and employment
    service_score = 50
    if sat_strong: service_score += 15
    if sat_house in (6, 10, 11): service_score += 10
    if mars_strong: service_score += 10
    service_score = max(0, min(100, service_score))

    def _sl(s: int) -> str:
        if s >= 70: return 'Strong'
        if s >= 45: return 'Moderate'
        return 'Weak'

    return {
        'enemies_and_competition': {
            'score': enemy_score,
            'strength': _sl(enemy_score),
            'indicators': [
                f'Mars (enemy karaka) in {SIGNS[mars_sign]} (house {mars_house})',
                f'6th lord {lord} in house {lord_house}',
                f'{"Malefics in 6th — victory over enemies likely" if malefic_in_6 else "Benefics in 6th — enemies may initially prevail"}',
            ],
            'note': 'Upachaya house: malefic planets here enhance ability to defeat adversaries',
        },
        'health_and_disease': {
            'score': health_score,
            'strength': _sl(health_score),
            'indicators': [
                f'Saturn (chronic illness karaka) in {SIGNS[sat_sign]} (house {sat_house})',
                f'6th lord {lord} in {SIGNS[lord_sign]} — disease-resistance factor',
                f'Body parts: intestines, digestive system require attention',
            ],
        },
        'debt_and_litigation': {
            'score': debt_score,
            'strength': _sl(debt_score),
            'indicators': [
                f'6th lord {lord} in house {lord_house} — {"debt resolved" if lord_house in (1,5,9,11) else "debt accumulation possible"}',
            ],
        },
        'service_and_employment': {
            'score': service_score,
            'strength': _sl(service_score),
            'indicators': [
                f'Saturn in {SIGNS[sat_sign]} (house {sat_house}) — service orientation',
                f'6th house represents subordinate employment and daily work routines',
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
