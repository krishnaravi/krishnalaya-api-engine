"""
Ashtakavarga engine.
BAV (Bhinnashtakavarga) – per-planet benefic bindu counts per sign.
SAV (Sarvashtakavarga) – sum of all 7 planets' BAV per sign.

Thresholds (2nd house):
  SAV  : Weak <25 | Moderate 25-28 | Strong >28
  BAV  : Weak <4  | Moderate = 4   | Strong >4
"""
from __future__ import annotations
from .constants import BAV_TABLES, SIGNS

_PLANETS_7 = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']

_REF_MAP = {
    'Sun': 'SUN', 'Moon': 'MOON', 'Mars': 'MARS', 'Mercury': 'MERCURY',
    'Jupiter': 'JUPITER', 'Venus': 'VENUS', 'Saturn': 'SATURN', 'Lagna': 'LAGNA'
}


def _compute_bav(planet: str, positions: dict) -> dict[int, int]:
    """Bhinnashtakavarga for one planet: bindus per sign (0-11)."""
    table = BAV_TABLES.get(planet, {})
    bav: dict[int, int] = {i: 0 for i in range(12)}

    for ref_name, pos_key in _REF_MAP.items():
        if pos_key not in positions:
            continue
        ref_sign = positions[pos_key]['sign_index']
        benefic = set(table.get(ref_name, []))

        for sign in range(12):
            house_from_ref = (sign - ref_sign) % 12 + 1   # 1-indexed
            if house_from_ref in benefic:
                bav[sign] += 1

    return bav


def compute_all_bav(positions: dict) -> dict[str, dict[int, int]]:
    return {p: _compute_bav(p, positions) for p in _PLANETS_7}


def compute_sav(all_bav: dict[str, dict[int, int]]) -> dict[int, int]:
    sav: dict[int, int] = {i: 0 for i in range(12)}
    for bav in all_bav.values():
        for sign, v in bav.items():
            sav[sign] += v
    return sav


def _sav_strength(bindus: int) -> str:
    if bindus < 25:   return 'Weak'
    if bindus <= 28:  return 'Moderate'
    return 'Strong'


def _bav_strength(bindus: int) -> str:
    if bindus < 4:   return 'Weak'
    if bindus == 4:  return 'Moderate'
    return 'Strong'


def get_ashtakavarga_analysis(positions: dict, second_house_sign: int,
                               second_lord: str) -> dict:
    all_bav = compute_all_bav(positions)
    sav = compute_sav(all_bav)

    sav_2nd = sav[second_house_sign]
    lord_bav_2nd = all_bav.get(second_lord, {}).get(second_house_sign, 0)
    jup_bav_2nd  = all_bav.get('Jupiter', {}).get(second_house_sign, 0)

    sav_str   = _sav_strength(sav_2nd)
    lord_str  = _bav_strength(lord_bav_2nd)
    jup_str   = _bav_strength(jup_bav_2nd)

    # Composite 0-100 score: SAV(40%) + lord BAV(30%) + Jupiter BAV(30%)
    sav_score  = min(int(sav_2nd / 40 * 40), 40)
    lord_score = min(int(lord_bav_2nd / 8 * 30), 30)
    jup_score  = min(int(jup_bav_2nd  / 8 * 30), 30)
    composite  = sav_score + lord_score + jup_score

    return {
        'second_house_sign': SIGNS[second_house_sign],
        'sav': {
            'bindus': sav_2nd,
            'strength': sav_str,
            'thresholds': {'weak': '<25', 'moderate': '25-28', 'strong': '>28'},
        },
        'bav_second_lord': {
            'planet': second_lord,
            'bindus_in_second_house': lord_bav_2nd,
            'strength': lord_str,
            'thresholds': {'weak': '<4', 'moderate': '4', 'strong': '>4'},
        },
        'bav_jupiter': {
            'bindus_in_second_house': jup_bav_2nd,
            'strength': jup_str,
            'thresholds': {'weak': '<4', 'moderate': '4', 'strong': '>4'},
        },
        'composite_av_score': composite,
        'full_sav_by_sign': {SIGNS[i]: sav[i] for i in range(12)},
        'full_bav_by_planet': {
            planet: {SIGNS[i]: all_bav[planet][i] for i in range(12)}
            for planet in _PLANETS_7
        },
    }
