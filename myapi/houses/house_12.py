"""
House 12 — Vyaya Bhava (House of Loss, Liberation, Foreign Lands)
Karakas: Saturn (loss, renunciation), Ketu (liberation, past karma)
Vargas:  D-1, D-9, D-60 (deep karma)
Note: Dusthana — but also Moksha Bhava (house of liberation and spirituality).
"""
from __future__ import annotations
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP, EXALTATION, OWN_SIGNS
from .base import analyze_house, finalize

HOUSE_CONFIG = {
    'number': 12,
    'karakas': ['Saturn', 'Ketu'],
    'primary_karaka': 'Saturn',
    'natural_significations': [
        'Expenditure, loss, and hidden costs', 'Foreign lands and settlement abroad',
        'Liberation (Moksha) and spiritual transcendence', 'Bed pleasures and sleep',
        'Hospitals, asylums, prisons, and confinement', 'Charitable activities',
        'Left eye', 'Feet and ankles (lower extremities)',
    ],
    'body_parts': ['Feet', 'Left eye', 'Lymphatic system', 'Sleep disorders'],
    'preferred_vargas': [1, 9, 60],
}


def _significations(positions: dict, lagna_sign: int, house_sign: int,
                    lord: str, dasha: dict) -> dict:
    sat  = positions.get('SATURN', {})
    ketu = positions.get('KETU', {})

    def _house(sign: int) -> int: return (sign - lagna_sign) % 12 + 1
    def _strong(p: str, s: int) -> bool:
        return s in OWN_SIGNS.get(p, []) or s == EXALTATION.get(p)

    sat_sign  = sat.get('sign_index', 0)
    ketu_sign = ketu.get('sign_index', 0)
    lord_sign = positions.get(PLANET_KEY_MAP.get(lord, lord.upper()), {}).get('sign_index', 0)

    sat_house  = _house(sat_sign)
    ketu_house = _house(ketu_sign)
    lord_house = _house(lord_sign)

    sat_strong  = _strong('Saturn', sat_sign)
    lord_strong = _strong(lord, lord_sign)

    occupants_12 = [p for p, d in positions.items()
                    if p != 'LAGNA' and d['sign_index'] == house_sign]

    # Expenditure and financial loss
    # Strong 12th lord can control/redirect losses; weak → uncontrolled spending
    loss_score = 50
    if lord_strong:   loss_score += 15  # strong lord = controlled expenditure
    if sat_strong:    loss_score += 10
    if lord_house in (6, 8, 12): loss_score -= 15  # lord in dusthana = more losses
    if lord_house in (2, 11):    loss_score += 10  # lord in dhana houses = expenditure controlled
    loss_score = max(0, min(100, loss_score))

    # Foreign travel / settlement
    foreign_score = 50
    rahu = positions.get('RAHU', {})
    rahu_sign = rahu.get('sign_index', 0)
    rahu_house = _house(rahu_sign)
    if rahu_house in (12, 9, 7): foreign_score += 20   # Rahu in 12/9/7 → foreign
    if 'RAHU' in occupants_12:   foreign_score += 15
    if lord_house in (9, 12):    foreign_score += 10
    foreign_score = max(0, min(100, foreign_score))

    # Moksha and spirituality
    moksha_score = 50
    if ketu_house in (12, 8): moksha_score += 25   # Ketu in 12/8 = strong moksha indicator
    if sat_strong:             moksha_score += 10
    if lord_house in (12, 8, 9): moksha_score += 10
    jup = positions.get('JUPITER', {})
    jup_house = _house(jup.get('sign_index', 0))
    if jup_house in (12, 9): moksha_score += 10    # Jupiter in 12/9 = spiritual wisdom
    moksha_score = max(0, min(100, moksha_score))

    # Sleep and bed pleasures (12th house quality)
    sleep_score = 50
    moon = positions.get('MOON', {})
    moon_house = _house(moon.get('sign_index', 0))
    if moon_house == 12: sleep_score += 15  # Moon in 12th = deep sleep, vivid dreams
    venus = positions.get('VENUS', {})
    venus_house = _house(venus.get('sign_index', 0))
    if venus_house == 12: sleep_score += 10
    sleep_score = max(0, min(100, sleep_score))

    def _sl(s: int) -> str:
        if s >= 70: return 'Strong'
        if s >= 45: return 'Moderate'
        return 'Weak'

    return {
        'expenditure_and_loss': {
            'score': loss_score,
            'strength': _sl(loss_score),
            'note': 'Higher score = better control over expenditures; 12th house governs all outflows',
            'indicators': [
                f'12th lord {lord} in {SIGNS[lord_sign]} (house {lord_house})',
                f'Saturn in {SIGNS[sat_sign]} (house {sat_house}) — expenditure discipline',
                f'12th house occupants: {[p.title() for p in occupants_12] or ["None"]}',
            ],
        },
        'foreign_lands_and_travel': {
            'score': foreign_score,
            'strength': _sl(foreign_score),
            'indicators': [
                f'Rahu in {SIGNS[rahu_sign]} (house {rahu_house}) — foreign inclination',
                f'12th lord in house {lord_house} — {"foreign settlement likely" if lord_house in (9,12) else "foreign travel possible"}',
            ],
        },
        'moksha_and_spirituality': {
            'score': moksha_score,
            'strength': _sl(moksha_score),
            'indicators': [
                f'Ketu in {SIGNS[ketu_sign]} (house {ketu_house}) — {"strong liberation tendency" if ketu_house in (12,8) else "moderate spiritual focus"}',
                f'Jupiter in house {jup_house} — philosophical depth',
                '12th house is the seat of Moksha — liberation from cycle of rebirth',
            ],
        },
        'sleep_and_hidden_pleasures': {
            'score': sleep_score,
            'strength': _sl(sleep_score),
            'indicators': [
                f'Moon in house {moon_house} — quality of sleep and subconscious',
                f'Venus in house {venus_house} — enjoyment and bed pleasures',
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
