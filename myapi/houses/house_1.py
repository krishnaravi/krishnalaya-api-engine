"""
House 1 — Tanu Bhava (House of Self / Ascendant)
Karakas: Sun (vitality, soul), Mars (physical body, courage)
Vargas:  D-1, D-9 (inner self), D-24 (intellect), D-60 (past karma)
"""
from __future__ import annotations
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP, EXALTATION, DEBILITATION, OWN_SIGNS
from .base import analyze_house, finalize

HOUSE_CONFIG = {
    'number': 1,
    'karakas': ['Sun', 'Mars'],
    'primary_karaka': 'Sun',
    'natural_significations': [
        'Physical body and appearance', 'Personality and character',
        'Health and vitality', 'Self-expression and identity',
        'Early life and longevity', 'Intelligence and natural tendencies',
        'Fame and reputation', 'Beginnings and fresh starts',
    ],
    'body_parts': ['Head', 'Brain', 'Face', 'Hair', 'Overall constitution'],
    'preferred_vargas': [1, 9, 24, 60],
}

_LAGNA_SIGN_PERSONALITY = {
    0:  ('Aries',       'Pioneering, energetic, impulsive, natural leader'),
    1:  ('Taurus',      'Steady, sensual, stubborn, loves comfort and beauty'),
    2:  ('Gemini',      'Intellectual, communicative, versatile, curious'),
    3:  ('Cancer',      'Nurturing, emotional, intuitive, family-oriented'),
    4:  ('Leo',         'Confident, dramatic, generous, natural authority'),
    5:  ('Virgo',       'Analytical, meticulous, health-conscious, service-oriented'),
    6:  ('Libra',       'Diplomatic, artistic, relationship-focused, fair-minded'),
    7:  ('Scorpio',     'Intense, secretive, transformative, psychic depth'),
    8:  ('Sagittarius', 'Philosophical, adventurous, optimistic, freedom-loving'),
    9:  ('Capricorn',   'Disciplined, ambitious, practical, authority-seeking'),
    10: ('Aquarius',    'Humanitarian, unconventional, intellectual, community-minded'),
    11: ('Pisces',      'Intuitive, spiritual, compassionate, dreamy, artistic'),
}


def _significations(positions: dict, lagna_sign: int, house_sign: int,
                    lord: str, dasha: dict) -> dict:
    sun  = positions.get('SUN',  {})
    mars = positions.get('MARS', {})
    lagna_data = positions['LAGNA']

    sun_sign  = sun.get('sign_index', 0)
    mars_sign = mars.get('sign_index', 0)
    sun_house  = (sun_sign  - lagna_sign) % 12 + 1
    mars_house = (mars_sign - lagna_sign) % 12 + 1

    # Physical constitution based on lagna sign
    _, personality_desc = _LAGNA_SIGN_PERSONALITY.get(lagna_sign, (SIGNS[lagna_sign], 'Balanced'))
    sign_element = {0:'Fire',1:'Earth',2:'Air',3:'Water',
                    4:'Fire',5:'Earth',6:'Air',7:'Water',
                    8:'Fire',9:'Earth',10:'Air',11:'Water'}[lagna_sign]

    constitution_map = {'Fire': 'Pitta (fiery, dynamic)',
                        'Earth': 'Kapha (stable, grounded)',
                        'Air': 'Vata (mobile, communicative)',
                        'Water': 'Kapha-Vata (fluid, sensitive)'}

    # Body health score
    sun_strong = sun.get('sign_index') in OWN_SIGNS.get('Sun', []) or sun.get('sign_index') == EXALTATION.get('Sun')
    lord_strong = positions.get(PLANET_KEY_MAP.get(lord, lord.upper()), {}).get('sign_index') in \
                  (OWN_SIGNS.get(lord, []) + [EXALTATION.get(lord)])

    body_score = 50
    if sun_strong:   body_score += 20
    if lord_strong:  body_score += 20
    if sun_house in (1,4,7,10,5,9):  body_score += 10
    if sun_house in (6,8,12):        body_score -= 20
    body_score = max(0, min(100, body_score))

    # Self and personality score
    personality_score = 50
    if lagna_sign in OWN_SIGNS.get(lord, []):  personality_score += 15
    if mars_house in (1, 10, 5):               personality_score += 10
    personality_score = min(100, personality_score)

    # Longevity indicator
    long_score = 50
    if lord_strong:       long_score += 20
    if sun_strong:        long_score += 10
    if sun_house == 8:    long_score += 15   # Sun in 8th supports longevity
    if sun_house == 12:   long_score -= 10
    long_score = max(0, min(100, long_score))

    def _sl(s: int) -> str:
        if s >= 70: return 'Strong'
        if s >= 45: return 'Moderate'
        return 'Weak'

    return {
        'self_and_personality': {
            'score': personality_score,
            'strength': _sl(personality_score),
            'lagna_sign': SIGNS[lagna_sign],
            'constitution': constitution_map[sign_element],
            'personality_traits': personality_desc,
            'indicators': [
                f'Sun (karaka) in {SIGNS[sun_sign]} ({sun_house}th house)',
                f'Mars (body karaka) in {SIGNS[mars_sign]} ({mars_house}th house)',
                f'Lagna lord {lord} placed in house {(positions.get(PLANET_KEY_MAP.get(lord, lord.upper()), {}).get("sign_index", 0) - lagna_sign) % 12 + 1}',
            ],
        },
        'physical_body_and_health': {
            'score': body_score,
            'strength': _sl(body_score),
            'element': sign_element,
            'constitution': constitution_map[sign_element],
            'sun_strength': 'Strong' if sun_strong else 'Moderate',
            'indicators': [
                f'Sun in {SIGNS[sun_sign]} ({sun_house}th) — {"well-placed" if sun_house not in (6,8,12) else "challenging placement"}',
                f'Lagna lord {lord} — {"strong" if lord_strong else "needs strengthening"}',
            ],
        },
        'longevity_and_vitality': {
            'score': long_score,
            'strength': _sl(long_score),
            'indicators': [
                f'Sun in {SIGNS[sun_sign]} (house {sun_house})',
                f'Lagna degree: {round(lagna_data.get("degree_in_sign", 0), 1)}° {SIGNS[lagna_sign]}',
            ],
            'note': 'Full longevity calculation requires Ayurdasamsha and Shodasamsha analysis',
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
