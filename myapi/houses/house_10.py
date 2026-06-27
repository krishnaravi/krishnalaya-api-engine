"""
House 10 — Karma Bhava (House of Career, Action, Public Life)
Karakas: Sun (authority), Mercury (intellect/business), Jupiter (wisdom/expansion), Saturn (hard work)
Vargas:  D-1, D-9, D-10 (Dasamsa — primary for career), D-24
"""
from __future__ import annotations
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP, EXALTATION, OWN_SIGNS
from .base import analyze_house, finalize

HOUSE_CONFIG = {
    'number': 10,
    'karakas': ['Sun', 'Mercury', 'Jupiter', 'Saturn'],
    'primary_karaka': 'Sun',
    'natural_significations': [
        'Career, profession, and vocation', 'Public reputation and social status',
        'Authority, power, and governance', 'Actions and karma in this life',
        'Employer and senior authority figures', 'Fame and recognition',
        'Father (secondary to 9th)', 'Knees and joints',
    ],
    'body_parts': ['Knees', 'Knee joints', 'Patella', 'Skeletal structure'],
    'preferred_vargas': [1, 9, 10, 24],
}

_CAREER_PLANET_THEMES = {
    'Sun':     'Authority, government, politics, leadership, administration',
    'Moon':    'Public service, hospitality, nursing, emotional support roles',
    'Mars':    'Engineering, military, surgery, athletics, real estate',
    'Mercury': 'Business, communication, accounting, IT, writing, trade',
    'Jupiter': 'Teaching, law, finance, religion, consulting, advisory roles',
    'Venus':   'Arts, entertainment, luxury goods, fashion, music, beauty industry',
    'Saturn':  'Service sectors, engineering, mining, agriculture, judiciary',
    'Rahu':    'Foreign connections, technology, unconventional professions',
    'Ketu':    'Spiritual roles, research, healing, metaphysics',
}


def _significations(positions: dict, lagna_sign: int, house_sign: int,
                    lord: str, dasha: dict) -> dict:
    sun  = positions.get('SUN', {})
    sat  = positions.get('SATURN', {})
    merc = positions.get('MERCURY', {})
    jup  = positions.get('JUPITER', {})

    def _house(sign: int) -> int: return (sign - lagna_sign) % 12 + 1
    def _strong(p: str, s: int) -> bool:
        return s in OWN_SIGNS.get(p, []) or s == EXALTATION.get(p)

    sun_sign  = sun.get('sign_index', 0)
    sat_sign  = sat.get('sign_index', 0)
    merc_sign = merc.get('sign_index', 0)
    jup_sign  = jup.get('sign_index', 0)
    lord_sign = positions.get(PLANET_KEY_MAP.get(lord, lord.upper()), {}).get('sign_index', 0)

    sun_house  = _house(sun_sign)
    sat_house  = _house(sat_sign)
    lord_house = _house(lord_sign)

    sun_strong  = _strong('Sun', sun_sign)
    sat_strong  = _strong('Saturn', sat_sign)
    lord_strong = _strong(lord, lord_sign)

    # Career strength
    career_score = 50
    if sun_strong:    career_score += 15
    if lord_strong:   career_score += 20
    if sun_house in (1, 5, 9, 10): career_score += 10
    if lord_house in (1, 5, 9, 10, 11): career_score += 10
    if lord_house in (6, 8, 12):    career_score -= 15
    if sat_strong:    career_score += 5
    career_score = max(0, min(100, career_score))

    # Status and recognition
    status_score = 50
    if sun_strong: status_score += 20
    if sun_house in (1, 10, 9, 5): status_score += 15
    if lord_strong: status_score += 15
    status_score = max(0, min(100, status_score))

    # Work ethic / discipline
    work_score = 50
    if sat_strong: work_score += 20
    if sat_house in (10, 6, 3, 11): work_score += 15
    if sat_house in (1, 4): work_score -= 5
    work_score = max(0, min(100, work_score))

    # Career-indicating planets in 10th
    occupants_10 = [p for p, d in positions.items()
                    if p != 'LAGNA' and d['sign_index'] == house_sign]
    career_themes = [_CAREER_PLANET_THEMES.get(p.title(), '') for p in occupants_10
                     if _CAREER_PLANET_THEMES.get(p.title())]

    # Dominant 10th lord career profile
    lord_career_theme = _CAREER_PLANET_THEMES.get(lord, 'Varied career path')

    def _sl(s: int) -> str:
        if s >= 70: return 'Strong'
        if s >= 45: return 'Moderate'
        return 'Weak'

    return {
        'career_and_profession': {
            'score': career_score,
            'strength': _sl(career_score),
            'indicators': [
                f'10th lord {lord} in {SIGNS[lord_sign]} (house {lord_house})',
                f'Sun (Karmakaraka) in {SIGNS[sun_sign]} (house {sun_house})',
                f'Saturn (effort karaka) in {SIGNS[sat_sign]} (house {sat_house})',
            ],
            'career_field_indicators': career_themes or [lord_career_theme],
            'lord_career_theme': lord_career_theme,
            'note': 'D-10 (Dasamsa) is the primary chart for career analysis',
        },
        'status_and_recognition': {
            'score': status_score,
            'strength': _sl(status_score),
            'indicators': [
                f'Sun in {SIGNS[sun_sign]} (house {sun_house}) — public recognition potential',
                f'10th lord {"strong" if lord_strong else "moderate"} — status in society',
            ],
        },
        'work_ethic_and_discipline': {
            'score': work_score,
            'strength': _sl(work_score),
            'indicators': [
                f'Saturn (Karma karaka) in {SIGNS[sat_sign]} (house {sat_house})',
                f'{"Excellent" if sat_strong else "Average"} discipline and persistence in career',
            ],
        },
        'planets_influencing_career': {
            'occupants': [p.title() for p in occupants_10],
            'themes_from_occupants': career_themes,
            'lord': lord,
            'lord_theme': lord_career_theme,
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
