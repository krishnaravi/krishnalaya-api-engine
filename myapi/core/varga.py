"""
Divisional chart (Varga) engine — shared across all house modules.
Supports D-1, D-2, D-3, D-9, D-16, D-24.
"""
from __future__ import annotations
from .constants import (SIGNS, SIGN_LORDS, SIGN_ELEMENTS, SIGN_MODALITY,
                         EXALTATION, DEBILITATION, OWN_SIGNS, PLANET_KEY_MAP)


# ── Divisional sign calculators ───────────────────────────────────────────


def _d1(lon: float) -> int:
    return int(lon / 30) % 12


def _d2(lon: float) -> int:
    """Hora: Cancer (3) or Leo (4) only."""
    sign = int(lon / 30) % 12
    deg  = lon % 30
    return (4 if deg < 15 else 3) if sign % 2 == 0 else (3 if deg < 15 else 4)


def _d3(lon: float) -> int:
    """
    Parashari Drekkana (siblings, courage, communication).
    0-10° → same sign | 10-20° → 5th from sign | 20-30° → 9th from sign
    """
    sign = int(lon / 30) % 12
    part = int((lon % 30) / 10)        # 0, 1, 2
    return (sign + [0, 4, 8][part]) % 12


def _d9(lon: float) -> int:
    """Navamsha."""
    sign = int(lon / 30) % 12
    part = int((lon % 30) / (30.0 / 9))
    starts = {'Fire': 0, 'Earth': 9, 'Air': 6, 'Water': 3}
    return (starts[SIGN_ELEMENTS[sign]] + part) % 12


def _d16(lon: float) -> int:
    """Shodashamsha (vehicles, luxuries)."""
    sign = int(lon / 30) % 12
    part = int((lon % 30) / (30.0 / 16))
    starts = {'Movable': 0, 'Fixed': 4, 'Dual': 8}
    return (starts[SIGN_MODALITY[sign]] + part) % 12


def _d24(lon: float) -> int:
    """
    Siddhamsha / Chaturvimshamsha (skills, education, arts).
    Odd signs → 24 divisions from Leo (4)
    Even signs → 24 divisions from Cancer (3)
    """
    sign = int(lon / 30) % 12
    part = int((lon % 30) / 1.25)      # 0-23
    start = 4 if sign % 2 == 0 else 3  # Leo for odd signs, Cancer for even
    return (start + part) % 12


_VARGA_FN = {1: _d1, 2: _d2, 3: _d3, 9: _d9, 16: _d16, 24: _d24}

_VARGA_LABELS = {
    1: 'D-1 Rasi', 2: 'D-2 Hora', 3: 'D-3 Drekkana',
    9: 'D-9 Navamsha', 16: 'D-16 Shodashamsha', 24: 'D-24 Siddhamsha',
}


def get_varga_sign(lon: float, varga: int) -> int:
    fn = _VARGA_FN.get(varga)
    if fn is None:
        raise ValueError(f"Unsupported varga: {varga}")
    return fn(lon)


# ── Planet dignity ────────────────────────────────────────────────────────


def planet_dignity(planet: str, sign_idx: int) -> str:
    if planet not in EXALTATION:
        return 'Neutral'
    if sign_idx == EXALTATION[planet]:       return 'Exalted'
    if sign_idx == DEBILITATION[planet]:     return 'Debilitated'
    if sign_idx in OWN_SIGNS.get(planet, []): return 'Own Sign'
    return 'Neutral'


# ── Generic varga chart analysis ──────────────────────────────────────────


def analyze_varga(positions: dict, d1_lagna_sign: int,
                  varga: int, house_number: int = 2) -> dict:
    """
    Analyse a varga chart focused on a specific house (default: 2nd).
    Returns lord position, dignity, planets in house, and all positions.
    """
    varga_signs: dict[str, int] = {
        p: get_varga_sign(d['longitude'], varga)
        for p, d in positions.items()
    }

    v_lagna = d1_lagna_sign if varga == 1 else varga_signs['LAGNA']
    v_house_sign = (v_lagna + house_number - 1) % 12
    v_lord = SIGN_LORDS[v_house_sign]

    lord_key    = PLANET_KEY_MAP.get(v_lord, v_lord.upper())
    lord_v_sign = varga_signs.get(lord_key, 0)
    lord_v_house = (lord_v_sign - v_lagna) % 12 + 1

    planets_in_house = [
        p for p, s in varga_signs.items()
        if p != 'LAGNA' and s == v_house_sign
    ]

    all_pos = {
        p: {
            'sign_index': s,
            'sign': SIGNS[s],
            'house': (s - v_lagna) % 12 + 1 if p != 'LAGNA' else 1,
        }
        for p, s in varga_signs.items()
    }

    return {
        'varga': _VARGA_LABELS.get(varga, f'D-{varga}'),
        'lagna_sign_index': v_lagna,
        'lagna_sign': SIGNS[v_lagna],
        'house_number': house_number,
        'house_sign_index': v_house_sign,
        'house_sign': SIGNS[v_house_sign],
        'lord': v_lord,
        'lord_sign_index': lord_v_sign,
        'lord_sign': SIGNS[lord_v_sign],
        'lord_house': lord_v_house,
        'lord_dignity': planet_dignity(v_lord, lord_v_sign),
        'planets_in_house': planets_in_house,
        'all_positions': all_pos,
    }
