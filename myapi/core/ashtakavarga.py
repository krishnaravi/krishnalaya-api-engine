"""
Full Ashtakavarga Engine (Parashari).

BAV  — Bhinnashtakavarga: per-planet benefic bindu counts per sign.
SAV  — Sarvashtakavarga: sum of all 7 planets' BAV (total = 337).
Trikona Shodhana  — trine-group reduction applied to each planet BAV.
Ekadhipatya Shodhana — dual-lord reduction applied to the Sodhya SAV.
Prashtara — 8 reference-point × 12 sign contribution matrix per planet.
"""
from __future__ import annotations
from .constants import BAV_TABLES, SIGNS, SIGN_LORDS

_PLANETS_7 = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']

_REF_MAP = {
    'Sun': 'SUN', 'Moon': 'MOON', 'Mars': 'MARS', 'Mercury': 'MERCURY',
    'Jupiter': 'JUPITER', 'Venus': 'VENUS', 'Saturn': 'SATURN', 'Lagna': 'LAGNA',
}

# Signs that share the same lord — for Ekadhipatya Shodhana
_DUAL_LORD_SIGNS: dict[str, tuple[int, int]] = {
    'Mercury': (2, 5),    # Gemini, Virgo
    'Venus':   (1, 6),    # Taurus, Libra
    'Mars':    (0, 7),    # Aries, Scorpio
    'Jupiter': (8, 11),   # Sagittarius, Pisces
    'Saturn':  (9, 10),   # Capricorn, Aquarius
}

# Trine groups (0-indexed sign indices)
_TRIKONA_GROUPS = [(0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11)]


# ── Core BAV / SAV ────────────────────────────────────────────────────────


def _compute_bav(planet: str, positions: dict) -> dict[int, int]:
    """Bhinnashtakavarga for one planet: bindus per sign (keys 0-11)."""
    table = BAV_TABLES.get(planet, {})
    bav: dict[int, int] = {i: 0 for i in range(12)}

    for ref_name, pos_key in _REF_MAP.items():
        if pos_key not in positions:
            continue
        ref_sign = positions[pos_key]['sign_index']
        benefic  = set(table.get(ref_name, []))
        for sign in range(12):
            house_from_ref = (sign - ref_sign) % 12 + 1  # 1-indexed
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


# ── Shodhana ──────────────────────────────────────────────────────────────


def trikona_shodhana(bav: dict[int, int]) -> dict[int, int]:
    """Apply trine-group reduction to a BAV or SAV table."""
    result = dict(bav)
    for group in _TRIKONA_GROUPS:
        min_val = min(result[s] for s in group)
        for s in group:
            result[s] = max(0, result[s] - min_val)
    return result


def ekadhipatya_shodhana(sav: dict[int, int], positions: dict) -> dict[int, int]:
    """Apply dual-lordship reduction to the (already trikona-reduced) SAV."""
    result = dict(sav)
    occupied = {d['sign_index'] for p, d in positions.items() if p != 'LAGNA'}

    for _planet, (s1, s2) in _DUAL_LORD_SIGNS.items():
        s1_occ = s1 in occupied
        s2_occ = s2 in occupied

        if s1_occ and s2_occ:
            continue                        # both occupied — no reduction
        elif s1_occ and not s2_occ:
            result[s2] = 0
        elif s2_occ and not s1_occ:
            result[s1] = 0
        else:
            # Neither occupied: zero the sign with fewer bindus
            if result[s1] <= result[s2]:
                result[s1] = 0
            else:
                result[s2] = 0

    return result


# ── Prashtara table ───────────────────────────────────────────────────────


def compute_prashtara_table(planet: str, positions: dict) -> dict[str, dict[str, int]]:
    """8 reference points × 12 signs contribution matrix (values 0 or 1)."""
    table   = BAV_TABLES.get(planet, {})
    prashtara: dict[str, dict[str, int]] = {}

    for ref_name, pos_key in _REF_MAP.items():
        row: dict[str, int] = {}
        if pos_key not in positions:
            prashtara[ref_name] = {s: 0 for s in SIGNS}
            continue
        ref_sign = positions[pos_key]['sign_index']
        benefic  = set(table.get(ref_name, []))
        for sign_idx in range(12):
            hfr = (sign_idx - ref_sign) % 12 + 1
            row[SIGNS[sign_idx]] = 1 if hfr in benefic else 0
        prashtara[ref_name] = row

    return prashtara


# ── Strength labels ───────────────────────────────────────────────────────


def _sav_strength(bindus: int) -> str:
    if bindus < 25:    return 'Weak'
    if bindus <= 28:   return 'Moderate'
    return 'Strong'


def _bav_strength(bindus: int) -> str:
    if bindus < 4:   return 'Weak'
    if bindus == 4:  return 'Moderate'
    return 'Strong'


# ── Full analysis APIs ────────────────────────────────────────────────────


def get_house_av(positions: dict, house_sign: int,
                 lord: str, karaka: str | None = None) -> dict:
    """AV analysis for one house sign: SAV + BAV of lord + BAV of karaka."""
    all_bav = compute_all_bav(positions)
    sav     = compute_sav(all_bav)

    sav_val  = sav[house_sign]
    lord_bav = all_bav.get(lord, {}).get(house_sign, 0)
    kar_bav  = all_bav.get(karaka, {}).get(house_sign, 0) if karaka else 0

    sav_sc   = min(int(sav_val  / 40 * 40), 40)
    lord_sc  = min(int(lord_bav / 8  * 30), 30)
    kar_sc   = min(int(kar_bav  / 8  * 30), 30) if karaka else 0

    result = {
        'house_sign': SIGNS[house_sign],
        'sav': {
            'bindus': sav_val,
            'strength': _sav_strength(sav_val),
            'thresholds': {'weak': '<25', 'moderate': '25-28', 'strong': '>28'},
        },
        'bav_lord': {
            'planet': lord,
            'bindus': lord_bav,
            'strength': _bav_strength(lord_bav),
        },
        'full_sav_by_sign': {SIGNS[i]: sav[i] for i in range(12)},
        'full_bav': {
            p: {SIGNS[i]: all_bav[p][i] for i in range(12)}
            for p in _PLANETS_7
        },
    }
    if karaka:
        result['bav_karaka'] = {
            'planet': karaka,
            'bindus': kar_bav,
            'strength': _bav_strength(kar_bav),
        }
        result['composite_av_score'] = sav_sc + lord_sc + kar_sc
    else:
        result['composite_av_score'] = sav_sc + lord_sc

    return result


# Legacy alias used by second_house module
def get_ashtakavarga_analysis(positions: dict, second_house_sign: int,
                               second_lord: str) -> dict:
    return get_house_av(positions, second_house_sign, second_lord, 'Jupiter')


def get_full_ashtakavarga(positions: dict) -> dict:
    """Complete engine: raw → trikona shodhana → ekadhipatya shodhana."""
    all_bav  = compute_all_bav(positions)
    sav_raw  = compute_sav(all_bav)

    # Trikona Shodhana on each planet's BAV, then sum
    all_bav_sodhita = {p: trikona_shodhana(bav) for p, bav in all_bav.items()}
    sodhya_sav      = compute_sav(all_bav_sodhita)

    # Ekadhipatya Shodhana on Sodhya SAV
    final_sav = ekadhipatya_shodhana(sodhya_sav, positions)

    sav_total    = sum(sav_raw.values())   # should be 337
    sodhya_total = sum(sodhya_sav.values())
    final_total  = sum(final_sav.values())

    # Best houses by SAV (raw)
    sorted_signs = sorted(range(12), key=lambda i: sav_raw[i], reverse=True)

    return {
        'raw': {
            'bav': {
                p: {SIGNS[i]: all_bav[p][i] for i in range(12)}
                for p in _PLANETS_7
            },
            'bav_totals': {p: sum(all_bav[p].values()) for p in _PLANETS_7},
            'sav': {SIGNS[i]: sav_raw[i] for i in range(12)},
            'sav_total': sav_total,
            'sav_strength': {SIGNS[i]: _sav_strength(sav_raw[i]) for i in range(12)},
        },
        'after_trikona_shodhana': {
            'bav': {
                p: {SIGNS[i]: all_bav_sodhita[p][i] for i in range(12)}
                for p in _PLANETS_7
            },
            'sav': {SIGNS[i]: sodhya_sav[i] for i in range(12)},
            'sav_total': sodhya_total,
        },
        'after_ekadhipatya_shodhana': {
            'sav': {SIGNS[i]: final_sav[i] for i in range(12)},
            'sav_total': final_total,
            'sav_strength': {SIGNS[i]: _sav_strength(final_sav[i]) for i in range(12)},
        },
        'insights': {
            'strongest_signs': [SIGNS[i] for i in sorted_signs[:3]],
            'weakest_signs':   [SIGNS[i] for i in sorted_signs[-3:]],
            'strong_transit_signs': [
                SIGNS[i] for i in range(12) if sav_raw[i] > 28
            ],
        },
    }


def get_bav_report(planet: str, positions: dict) -> dict:
    """Full BAV report for one planet with prashtara and strength."""
    bav       = _compute_bav(planet, positions)
    prashtara = compute_prashtara_table(planet, positions)
    sodhita   = trikona_shodhana(bav)

    planet_sign = positions.get(
        planet.upper() if planet.upper() in positions else planet, {}
    ).get('sign_index', None)

    own_bindu = bav.get(planet_sign, 0) if planet_sign is not None else 0

    sorted_signs = sorted(range(12), key=lambda i: bav[i], reverse=True)

    return {
        'planet': planet,
        'bav': {SIGNS[i]: bav[i] for i in range(12)},
        'bav_total': sum(bav.values()),
        'bav_strength': {SIGNS[i]: _bav_strength(bav[i]) for i in range(12)},
        'after_trikona_shodhana': {SIGNS[i]: sodhita[i] for i in range(12)},
        'prashtara_table': prashtara,
        'own_sign_bindus': own_bindu,
        'strongest_signs': [SIGNS[i] for i in sorted_signs[:4]],
        'weakest_signs':   [SIGNS[i] for i in sorted_signs[-4:]],
    }
