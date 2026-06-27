"""
Divisional chart (Varga) engine.
Supports D-1 (Rasi), D-2 (Hora), D-9 (Navamsha), D-16 (Shodashamsha).
"""
from __future__ import annotations
from .constants import SIGNS, SIGN_LORDS, SIGN_ELEMENTS, SIGN_MODALITY, EXALTATION, DEBILITATION, OWN_SIGNS, PLANET_KEY_MAP


# ── Divisional sign calculators ───────────────────────────────────────────


def _d1_sign(lon: float) -> int:
    return int(lon / 30) % 12


def _d2_sign(lon: float) -> int:
    """
    Hora chart: only Cancer (3) and Leo (4) exist.
    Odd signs (0-indexed even: Aries, Gemini…): 0–15° → Leo, 15–30° → Cancer
    Even signs (0-indexed odd: Taurus, Cancer…): 0–15° → Cancer, 15–30° → Leo
    """
    sign = int(lon / 30) % 12
    deg = lon % 30
    if sign % 2 == 0:          # Aries=0 is an odd sign (1st)
        return 4 if deg < 15 else 3
    else:
        return 3 if deg < 15 else 4


def _d9_sign(lon: float) -> int:
    sign = int(lon / 30) % 12
    part = int((lon % 30) / (30.0 / 9))   # 0-8
    starts = {'Fire': 0, 'Earth': 9, 'Air': 6, 'Water': 3}
    return (starts[SIGN_ELEMENTS[sign]] + part) % 12


def _d16_sign(lon: float) -> int:
    sign = int(lon / 30) % 12
    part = int((lon % 30) / (30.0 / 16))  # 0-15
    starts = {'Movable': 0, 'Fixed': 4, 'Dual': 8}
    return (starts[SIGN_MODALITY[sign]] + part) % 12


_VARGA_FN = {1: _d1_sign, 2: _d2_sign, 9: _d9_sign, 16: _d16_sign}


def get_varga_sign(lon: float, varga: int) -> int:
    fn = _VARGA_FN.get(varga)
    if fn is None:
        raise ValueError(f"Unsupported varga: {varga}")
    return fn(lon)


# ── Planet dignity ────────────────────────────────────────────────────────


def planet_dignity(planet: str, sign_idx: int) -> str:
    if planet not in EXALTATION:
        return 'Neutral'
    if sign_idx == EXALTATION[planet]:
        return 'Exalted'
    if sign_idx == DEBILITATION[planet]:
        return 'Debilitated'
    if sign_idx in OWN_SIGNS.get(planet, []):
        return 'Own Sign'
    return 'Neutral'


# ── Varga chart analysis ──────────────────────────────────────────────────


def analyze_varga(positions: dict, d1_lagna_sign: int, varga: int) -> dict:
    """
    For the given varga, return 2nd-house focused analysis dict.
    For D-1 the lagna is the actual Lagna; for other vargas the varga-lagna
    is computed from the Lagna's longitude using the same divisional formula.
    """
    # Varga sign for every graha + Lagna
    varga_signs: dict[str, int] = {}
    for planet, data in positions.items():
        varga_signs[planet] = get_varga_sign(data['longitude'], varga)

    if varga == 1:
        v_lagna = d1_lagna_sign
    else:
        v_lagna = varga_signs['LAGNA']

    v_2nd_sign = (v_lagna + 1) % 12
    v_2nd_lord = SIGN_LORDS[v_2nd_sign]

    lord_key = PLANET_KEY_MAP.get(v_2nd_lord, v_2nd_lord.upper())
    lord_v_sign = varga_signs.get(lord_key, 0)
    lord_v_house = (lord_v_sign - v_lagna) % 12 + 1

    planets_in_2nd = [
        p for p, s in varga_signs.items()
        if p not in ('LAGNA',) and s == v_2nd_sign
    ]

    # All planets with sign + house in this varga
    all_pos = {}
    for p, s in varga_signs.items():
        house = (s - v_lagna) % 12 + 1 if p != 'LAGNA' else 1
        all_pos[p] = {'sign_index': s, 'sign': SIGNS[s], 'house': house}

    return {
        'varga': f'D-{varga}',
        'lagna_sign_index': v_lagna,
        'lagna_sign': SIGNS[v_lagna],
        'second_house_sign_index': v_2nd_sign,
        'second_house_sign': SIGNS[v_2nd_sign],
        'second_lord': v_2nd_lord,
        'second_lord_sign_index': lord_v_sign,
        'second_lord_sign': SIGNS[lord_v_sign],
        'second_lord_house': lord_v_house,
        'second_lord_dignity': planet_dignity(v_2nd_lord, lord_v_sign),
        'planets_in_second_house': planets_in_2nd,
        'all_positions': all_pos,
    }
