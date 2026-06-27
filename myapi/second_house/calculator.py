"""
Main orchestrator for 2nd House (Dhana/Vak Sthana) analysis.
Calls: planetary → varga → ashtakavarga → dasha → significations
"""
from __future__ import annotations
import time
from datetime import date as Date

from .planetary import get_positions
from .varga import analyze_varga
from .ashtakavarga import get_ashtakavarga_analysis
from .dasha import get_dasha_bhukti, analyze_dasha_relationship
from .significations import (
    analyze_wealth, analyze_speech_profession,
    analyze_childbirth_family, analyze_maraka,
)
from .constants import SIGNS, SIGN_LORDS


def _aspects_on_sign(positions: dict, target_sign: int) -> list[dict]:
    """
    Vedic aspects on a target sign.
    All planets: 7th aspect.
    Mars: +4, +8  (4th & 8th).
    Jupiter: +5, +9 (5th & 9th).
    Saturn: +3, +10 (3rd & 10th).
    Rahu/Ketu: +5, +9.
    """
    SPECIAL: dict[str, list[int]] = {
        'MARS':    [4, 8],
        'JUPITER': [5, 9],
        'SATURN':  [3, 10],
        'RAHU':    [5, 9],
        'KETU':    [5, 9],
    }
    results = []
    for planet, data in positions.items():
        if planet == 'LAGNA':
            continue
        ps = data['sign_index']
        if ps == target_sign:
            continue
        offsets = [7] + SPECIAL.get(planet, [])
        for off in offsets:
            if (ps + off - 1) % 12 == target_sign:
                results.append({'planet': planet, 'from_sign': SIGNS[ps]})
                break
    return results


def _planets_in_sign(positions: dict, sign: int) -> list[dict]:
    return [
        {
            'planet': p,
            'degree_in_sign': d['degree_in_sign'],
            'is_retrograde': d.get('is_retrograde', False),
            'nakshatra': d.get('nakshatra', ''),
        }
        for p, d in positions.items()
        if p != 'LAGNA' and d['sign_index'] == sign
    ]


def _all_planets_formatted(positions: dict, lagna_sign: int) -> dict:
    out = {}
    for p, d in positions.items():
        house = (d['sign_index'] - lagna_sign) % 12 + 1 if p != 'LAGNA' else 1
        out[p] = {
            'sign': d['sign'],
            'sign_index': d['sign_index'],
            'house': house,
            'degree_in_sign': d['degree_in_sign'],
            'nakshatra': d.get('nakshatra', ''),
            'is_retrograde': d.get('is_retrograde', False),
        }
    return out


def _strip_all_positions(varga_dict: dict) -> dict:
    """Remove verbose all_positions key for cleaner top-level output."""
    return {k: v for k, v in varga_dict.items() if k != 'all_positions'}


def _score_label(score: int) -> str:
    if score >= 70:  return 'Strong'
    if score >= 45:  return 'Moderate'
    return 'Weak'


def compute(
    date_str: str,
    time_str: str,
    latitude: float,
    longitude: float,
    timezone_str: str,
    place_name: str = '',
    current_date_str: str | None = None,
) -> dict:
    t0 = time.time()

    if not current_date_str:
        current_date_str = Date.today().isoformat()

    # ── Step 1: Planetary positions ──────────────────────────────────────
    positions = get_positions(date_str, time_str, timezone_str, latitude, longitude)
    lagna_sign = positions['LAGNA']['sign_index']
    second_house_sign = (lagna_sign + 1) % 12
    second_lord = SIGN_LORDS[second_house_sign]

    # ── Step 2: Varga charts ─────────────────────────────────────────────
    d1  = analyze_varga(positions, lagna_sign, 1)
    d2  = analyze_varga(positions, lagna_sign, 2)
    d9  = analyze_varga(positions, lagna_sign, 9)
    d16 = analyze_varga(positions, lagna_sign, 16)

    # ── Step 3: Ashtakavarga ─────────────────────────────────────────────
    ashtakavarga = get_ashtakavarga_analysis(positions, second_house_sign, second_lord)

    # ── Step 4: Dasha-Bhukti ─────────────────────────────────────────────
    moon_lon = positions['MOON']['longitude']
    dasha = get_dasha_bhukti(moon_lon, date_str, current_date_str)
    dasha_rel = analyze_dasha_relationship(dasha, positions, lagna_sign)

    # ── Step 5: Significations ───────────────────────────────────────────
    wealth  = analyze_wealth(positions, lagna_sign, ashtakavarga, d2)
    speech  = analyze_speech_profession(positions, lagna_sign)
    family  = analyze_childbirth_family(positions, lagna_sign)
    maraka  = analyze_maraka(positions, lagna_sign, dasha)

    # ── Step 6: Summary ──────────────────────────────────────────────────
    composite = (wealth['score'] + speech['score'] + family['score']) // 3

    key_findings, warnings = [], []
    if wealth['score'] >= 70:
        key_findings.append('Strong Dhana yoga — significant financial growth potential')
    elif wealth['score'] < 45:
        warnings.append('Weak Dhana indicators — sustained financial planning advised')
    if speech['score'] >= 70:
        key_findings.append('High speech/communication-based career potential')
    if ashtakavarga['sav']['strength'] == 'Strong':
        key_findings.append(f'Strong SAV ({ashtakavarga["sav"]["bindus"]} bindus) in 2nd house sign')
    if maraka['risk_level'] == 'High':
        warnings.append(f'Active Maraka period — {dasha["mahadasha"]["lord"]}/{dasha["bhukti"]["lord"]} health vigilance required')
    elif maraka['risk_level'] == 'Moderate':
        warnings.append('Moderate Maraka influence — routine health checks recommended')
    if dasha_rel['wealth_activation']:
        key_findings.append('Current Dasha-Bhukti actively supports 2nd house significations')
    elif not dasha_rel['is_maraka_period'] and not dasha_rel['wealth_activation']:
        warnings.append('Current period lords not fully favorable for 2nd house matters')

    elapsed_ms = round((time.time() - t0) * 1000, 2)

    return {
        'status': 'success',
        'computation_time_ms': elapsed_ms,
        'input': {
            'date': date_str, 'time': time_str,
            'latitude': latitude, 'longitude': longitude,
            'timezone': timezone_str, 'place': place_name,
            'analysis_date': current_date_str,
        },
        'lagna': {
            'sign': positions['LAGNA']['sign'],
            'sign_index': lagna_sign,
            'degree_in_sign': positions['LAGNA']['degree_in_sign'],
            'nakshatra': positions['LAGNA']['nakshatra'],
            'lord': SIGN_LORDS[lagna_sign],
        },
        'second_house': {
            'sign': SIGNS[second_house_sign],
            'sign_index': second_house_sign,
            'lord': second_lord,
            'lord_position': {
                k: v for k, v in _all_planets_formatted(positions, lagna_sign).get(
                    {'Sun':'SUN','Moon':'MOON','Mars':'MARS','Mercury':'MERCURY',
                     'Jupiter':'JUPITER','Venus':'VENUS','Saturn':'SATURN',
                     'Rahu':'RAHU','Ketu':'KETU'}.get(second_lord, second_lord.upper()),
                    {}).items()
            },
            'planets_in_house': _planets_in_sign(positions, second_house_sign),
            'aspects_received': _aspects_on_sign(positions, second_house_sign),
        },
        'all_planets_d1': _all_planets_formatted(positions, lagna_sign),
        'varga_analysis': {
            'd1_rasi':           _strip_all_positions(d1),
            'd2_hora':           _strip_all_positions(d2),
            'd9_navamsha':       _strip_all_positions(d9),
            'd16_shodashamsha':  _strip_all_positions(d16),
        },
        'ashtakavarga': ashtakavarga,
        'dasha_bhukti': {**dasha, 'relationship_with_2nd_house': dasha_rel},
        'significations': {
            'wealth_income':      wealth,
            'speech_profession':  speech,
            'childbirth_family':  family,
            'maraka_analysis':    maraka,
        },
        'summary': {
            'overall_2nd_house_strength': _score_label(composite),
            'composite_score': composite,
            'wealth_score': wealth['score'],
            'speech_career_score': speech['score'],
            'family_expansion_score': family['score'],
            'maraka_risk_level': maraka['risk_level'],
            'key_findings': key_findings,
            'warnings': warnings,
            'current_period_assessment': dasha_rel['overall_assessment'],
        },
    }
