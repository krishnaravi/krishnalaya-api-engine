"""
Divisional chart (Varga) engine.
Supports D-1, D-2, D-3, D-9, D-10, D-12, D-16, D-24, D-60.
"""
from __future__ import annotations
from .constants import (SIGNS, SIGN_LORDS, SIGN_ELEMENTS, SIGN_MODALITY,
                         EXALTATION, DEBILITATION, OWN_SIGNS, MOOLATRIKONA,
                         PLANET_KEY_MAP, NATURAL_FRIENDS, NATURAL_ENEMIES)


# ── Divisional sign calculators ───────────────────────────────────────────


def _d1(lon: float) -> int:
    return int(lon / 30) % 12


def _d2(lon: float) -> int:
    """Hora: Cancer (3) or Leo (4) only."""
    sign = int(lon / 30) % 12
    deg  = lon % 30
    return (4 if deg < 15 else 3) if sign % 2 == 0 else (3 if deg < 15 else 4)


def _d3(lon: float) -> int:
    """Parashari Drekkana — 0-10° same sign, 10-20° 5th, 20-30° 9th."""
    sign = int(lon / 30) % 12
    part = int((lon % 30) / 10)
    return (sign + [0, 4, 8][part]) % 12


def _d9(lon: float) -> int:
    """Navamsha (inner self, spouse)."""
    sign = int(lon / 30) % 12
    part = int((lon % 30) / (30.0 / 9))
    starts = {'Fire': 0, 'Earth': 9, 'Air': 6, 'Water': 3}
    return (starts[SIGN_ELEMENTS[sign]] + part) % 12


def _d10(lon: float) -> int:
    """Dasamsa (career, profession, public life)."""
    sign = int(lon / 30) % 12
    part = int((lon % 30) / 3)   # 0-9
    # Odd signs (0-indexed even): start from same sign; even signs: start from 9th
    start = sign if sign % 2 == 0 else (sign + 8) % 12
    return (start + part) % 12


def _d12(lon: float) -> int:
    """Dwadasamsa (parents, ancestry, past-life karma)."""
    sign = int(lon / 30) % 12
    part = int((lon % 30) / 2.5)  # 0-11
    return (sign + part) % 12


def _d16(lon: float) -> int:
    """Shodashamsha (vehicles, luxuries, comforts)."""
    sign = int(lon / 30) % 12
    part = int((lon % 30) / (30.0 / 16))
    starts = {'Movable': 0, 'Fixed': 4, 'Dual': 8}
    return (starts[SIGN_MODALITY[sign]] + part) % 12


def _d24(lon: float) -> int:
    """Siddhamsha / Chaturvimshamsha (skills, education, arts).
    Odd ordinal signs (0-indexed even) → Leo (4); even ordinal → Cancer (3).
    """
    sign = int(lon / 30) % 12
    part = int((lon % 30) / 1.25)  # 0-23
    start = 4 if sign % 2 == 0 else 3
    return (start + part) % 12


def _d60(lon: float) -> int:
    """Shastiamsha (deep past karma, accumulated destiny).
    Odd ordinal signs → Aries (0); even ordinal signs → Libra (6).
    """
    sign = int(lon / 30) % 12
    part = int((lon % 30) / 0.5)  # 0-59
    start = 0 if sign % 2 == 0 else 6
    return (start + part) % 12


_VARGA_FN: dict[int, object] = {
    1: _d1, 2: _d2, 3: _d3, 9: _d9, 10: _d10,
    12: _d12, 16: _d16, 24: _d24, 60: _d60,
}

_VARGA_LABELS: dict[int, str] = {
    1:  'D-1 Rasi',         2:  'D-2 Hora',
    3:  'D-3 Drekkana',     9:  'D-9 Navamsha',
    10: 'D-10 Dasamsa',     12: 'D-12 Dwadasamsa',
    16: 'D-16 Shodashamsha', 24: 'D-24 Siddhamsha',
    60: 'D-60 Shastiamsha',
}

_VARGA_THEMES: dict[int, str] = {
    1:  'Physical self, overall life',
    2:  'Wealth, financial resources',
    3:  'Siblings, courage, communication',
    9:  'Dharma, inner self, spouse, spiritual',
    10: 'Career, profession, public status',
    12: 'Parents, ancestry, lineage',
    16: 'Vehicles, luxuries, comforts',
    24: 'Skills, education, arts, learning',
    60: 'Past karma, deep destiny, accumulated merit',
}


def get_varga_sign(lon: float, varga: int) -> int:
    fn = _VARGA_FN.get(varga)
    if fn is None:
        raise ValueError(f"Unsupported varga: {varga}")
    return fn(lon)  # type: ignore[call-arg]


# ── Planet dignity ────────────────────────────────────────────────────────


def planet_dignity(planet: str, sign_idx: int) -> str:
    if planet not in EXALTATION:
        return 'Neutral'
    if sign_idx == EXALTATION.get(planet):
        return 'Exalted'
    if sign_idx == DEBILITATION.get(planet):
        return 'Debilitated'
    if sign_idx in OWN_SIGNS.get(planet, []):
        if sign_idx == MOOLATRIKONA.get(planet):
            return 'Moolatrikona'
        return 'Own Sign'
    lord = SIGN_LORDS[sign_idx]
    friends = NATURAL_FRIENDS.get(planet, [])
    enemies = NATURAL_ENEMIES.get(planet, [])
    if lord in friends:
        return 'Friendly'
    if lord in enemies:
        return 'Enemy'
    return 'Neutral'


def dignity_score(dignity: str) -> int:
    return {'Exalted': 5, 'Moolatrikona': 4, 'Own Sign': 4,
            'Friendly': 3, 'Neutral': 2, 'Enemy': 1, 'Debilitated': 0}.get(dignity, 2)


# ── Varga Bala ────────────────────────────────────────────────────────────


def compute_varga_bala(planet: str, positions: dict, vargas: list[int] | None = None) -> dict:
    """Compute a planet's strength across the requested vargas."""
    if vargas is None:
        vargas = [1, 2, 3, 9, 10, 12, 16, 24, 60]
    lon = positions.get(PLANET_KEY_MAP.get(planet, planet.upper()), {}).get('longitude', 0.0)

    details: dict[str, dict] = {}
    total = 0
    max_score = len(vargas) * 5

    for v in vargas:
        try:
            v_sign = get_varga_sign(lon, v)
        except ValueError:
            continue
        dig  = planet_dignity(planet, v_sign)
        sc   = dignity_score(dig)
        total += sc
        details[_VARGA_LABELS.get(v, f'D-{v}')] = {
            'sign': SIGNS[v_sign],
            'dignity': dig,
            'score': sc,
        }

    pct = round(total / max_score * 100) if max_score else 0

    if pct >= 70:   strength = 'Very Strong'
    elif pct >= 55: strength = 'Strong'
    elif pct >= 40: strength = 'Moderate'
    elif pct >= 25: strength = 'Weak'
    else:           strength = 'Very Weak'

    # Vaiseshikamsa classification
    exalted_or_own = sum(1 for d in details.values() if d['dignity'] in ('Exalted', 'Own Sign', 'Moolatrikona'))
    if exalted_or_own >= 5:   vaiseshika = 'Paravata (exceptional)'
    elif exalted_or_own >= 4: vaiseshika = 'Uttama (very good)'
    elif exalted_or_own >= 3: vaiseshika = 'Gopura (good)'
    elif exalted_or_own >= 2: vaiseshika = 'Simhasana (moderate)'
    elif exalted_or_own >= 1: vaiseshika = 'Paravatamsa (some strength)'
    else:                      vaiseshika = 'No special vaiseshika bala'

    return {
        'planet': planet,
        'total_score': total,
        'max_score': max_score,
        'percentage': pct,
        'strength': strength,
        'vaiseshikamsa': vaiseshika,
        'exalted_or_own_count': exalted_or_own,
        'varga_details': details,
    }


# ── Generic varga chart analysis ──────────────────────────────────────────


def analyze_varga(positions: dict, d1_lagna_sign: int,
                  varga: int, house_number: int = 2) -> dict:
    """Analyse a varga chart focused on a specific house."""
    varga_signs: dict[str, int] = {
        p: get_varga_sign(d['longitude'], varga)
        for p, d in positions.items()
    }

    v_lagna = d1_lagna_sign if varga == 1 else varga_signs.get('LAGNA', d1_lagna_sign)
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
        'theme': _VARGA_THEMES.get(varga, ''),
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
        'lord_dignity_score': dignity_score(planet_dignity(v_lord, lord_v_sign)),
        'planets_in_house': planets_in_house,
        'all_positions': all_pos,
    }


def get_full_varga_chart(positions: dict, d1_lagna_sign: int, varga: int) -> dict:
    """Return a full varga chart: Lagna + all 12 houses with occupants."""
    varga_signs: dict[str, int] = {
        p: get_varga_sign(d['longitude'], varga)
        for p, d in positions.items()
    }
    v_lagna = d1_lagna_sign if varga == 1 else varga_signs.get('LAGNA', d1_lagna_sign)

    houses = {}
    for h in range(1, 13):
        h_sign = (v_lagna + h - 1) % 12
        lord   = SIGN_LORDS[h_sign]
        lord_key = PLANET_KEY_MAP.get(lord, lord.upper())
        lord_sign = varga_signs.get(lord_key, 0)
        occupants = [p for p, s in varga_signs.items() if p != 'LAGNA' and s == h_sign]
        houses[str(h)] = {
            'sign': SIGNS[h_sign],
            'sign_index': h_sign,
            'lord': lord,
            'lord_sign': SIGNS[lord_sign],
            'lord_house': (lord_sign - v_lagna) % 12 + 1,
            'lord_dignity': planet_dignity(lord, lord_sign),
            'occupants': occupants,
        }

    planet_positions = {
        p: {
            'sign': SIGNS[s], 'sign_index': s,
            'house': (s - v_lagna) % 12 + 1 if p != 'LAGNA' else 1,
            'dignity': planet_dignity(p.title(), s) if p != 'LAGNA' else 'N/A',
        }
        for p, s in varga_signs.items()
    }

    return {
        'varga': _VARGA_LABELS.get(varga, f'D-{varga}'),
        'theme': _VARGA_THEMES.get(varga, ''),
        'lagna': SIGNS[v_lagna],
        'lagna_sign_index': v_lagna,
        'houses': houses,
        'planet_positions': planet_positions,
    }
