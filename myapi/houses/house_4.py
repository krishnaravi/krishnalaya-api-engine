"""
House 4 — Sukha Bhava (House of Happiness, Mother, Property)
Karakas: Moon (mother, mind), Mars (property/land), Venus (vehicles, comforts)
Vargas:  D-1, D-9, D-16 (vehicles/comforts), D-12 (parents)
"""
from __future__ import annotations
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP, EXALTATION, OWN_SIGNS
from .base import analyze_house, finalize

HOUSE_CONFIG = {
    'number': 4,
    'karakas': ['Moon', 'Mars', 'Venus'],
    'primary_karaka': 'Moon',
    'natural_significations': [
        'Mother and maternal figures', 'Home, residence, and domestic life',
        'Happiness, contentment, and inner peace', 'Property, land, and real estate',
        'Education (school level) and foundational learning', 'Vehicles and conveyances',
        'Heart and emotional stability', 'Ancestral property and roots',
    ],
    'body_parts': ['Chest', 'Heart', 'Lungs', 'Breasts', 'Stomach'],
    'preferred_vargas': [1, 9, 12, 16],
}


def _significations(positions: dict, lagna_sign: int, house_sign: int,
                    lord: str, dasha: dict) -> dict:
    moon  = positions.get('MOON', {})
    mars  = positions.get('MARS', {})
    venus = positions.get('VENUS', {})

    def _house(sign: int) -> int: return (sign - lagna_sign) % 12 + 1
    def _strong(p: str, s: int) -> bool:
        return s in OWN_SIGNS.get(p, []) or s == EXALTATION.get(p)

    moon_sign  = moon.get('sign_index', 0)
    mars_sign  = mars.get('sign_index', 0)
    venus_sign = venus.get('sign_index', 0)
    lord_sign  = positions.get(PLANET_KEY_MAP.get(lord, lord.upper()), {}).get('sign_index', 0)

    moon_h  = _house(moon_sign)
    mars_h  = _house(mars_sign)
    venus_h = _house(venus_sign)
    lord_h  = _house(lord_sign)

    moon_strong  = _strong('Moon', moon_sign)
    mars_strong  = _strong('Mars', mars_sign)
    venus_strong = _strong('Venus', venus_sign)
    lord_strong  = _strong(lord, lord_sign)

    # Mother
    mother_score = 50
    if moon_strong:  mother_score += 20
    if moon_h in (1,4,5,9,10): mother_score += 10
    if moon_h in (6,8,12):     mother_score -= 20
    mother_score = max(0, min(100, mother_score))

    # Happiness / peace of mind
    happiness_score = 50
    if moon_strong:       happiness_score += 15
    if lord_strong:       happiness_score += 15
    if moon_h == 4:       happiness_score += 10
    if lord_h in (1,4,9): happiness_score += 10
    if moon.get('is_retrograde'): happiness_score -= 5
    happiness_score = max(0, min(100, happiness_score))

    # Property / Real estate
    property_score = 50
    if mars_strong:   property_score += 20
    if lord_strong:   property_score += 10
    if mars_h in (4,10,11): property_score += 15
    if mars_h in (6,8,12):  property_score -= 15
    property_score = max(0, min(100, property_score))

    # Vehicles / Conveyances
    vehicle_score = 50
    if venus_strong:   vehicle_score += 20
    if venus_h in (4,7,10,11): vehicle_score += 15
    if venus_h in (6,8,12):    vehicle_score -= 10
    vehicle_score = max(0, min(100, vehicle_score))

    def _sl(s: int) -> str:
        if s >= 70: return 'Strong'
        if s >= 45: return 'Moderate'
        return 'Weak'

    return {
        'mother_and_nurturing': {
            'score': mother_score,
            'strength': _sl(mother_score),
            'indicators': [
                f'Moon (karaka for mother) in {SIGNS[moon_sign]} (house {moon_h})',
                f'{"Excellent" if moon_strong else "Moderate"} lunar strength for maternal relations',
            ],
        },
        'happiness_and_peace_of_mind': {
            'score': happiness_score,
            'strength': _sl(happiness_score),
            'indicators': [
                f'Moon in {SIGNS[moon_sign]} (house {moon_h}) — emotional wellbeing',
                f'4th lord {lord} in house {lord_h} — domestic happiness',
            ],
        },
        'property_and_real_estate': {
            'score': property_score,
            'strength': _sl(property_score),
            'indicators': [
                f'Mars (karaka for property) in {SIGNS[mars_sign]} (house {mars_h})',
                f'4th lord {lord} in {SIGNS[lord_sign]} (house {lord_h})',
            ],
        },
        'vehicles_and_comforts': {
            'score': vehicle_score,
            'strength': _sl(vehicle_score),
            'indicators': [
                f'Venus (karaka for vehicles) in {SIGNS[venus_sign]} (house {venus_h})',
                f'{"Good" if vehicle_score >= 60 else "Average"} indications for vehicles and material comforts',
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
