"""
Main orchestrator for 3rd House (Sahaja/Vikrama Bhava) analysis.
Karaka: Mars (courage, siblings) | Mercury (communication)
Vargas:  D-1, D-3 (Drekkana), D-9 (Navamsha), D-24 (Siddhamsha)
"""
from __future__ import annotations
import time
from datetime import date as Date

from core.planetary import get_positions
from core.varga import analyze_varga
from core.ashtakavarga import compute_all_bav, compute_sav
from core.dasha import get_dasha_bhukti
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP

from .significations import (
    analyze_siblings, analyze_courage,
    analyze_communication, analyze_short_journeys, analyze_skills_arts,
)


# ── Helpers ───────────────────────────────────────────────────────────────

SPECIAL_ASPECTS: dict[str, list[int]] = {
    'MARS': [4, 8], 'JUPITER': [5, 9],
    'SATURN': [3, 10], 'RAHU': [5, 9], 'KETU': [5, 9],
}


def _aspects_on_sign(positions: dict, target_sign: int) -> list[dict]:
    results = []
    for planet, data in positions.items():
        if planet == 'LAGNA':
            continue
        ps = data['sign_index']
        if ps == target_sign:
            continue
        offsets = [7] + SPECIAL_ASPECTS.get(planet, [])
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
    return {
        p: {
            'sign': d['sign'],
            'sign_index': d['sign_index'],
            'house': (d['sign_index'] - lagna_sign) % 12 + 1 if p != 'LAGNA' else 1,
            'degree_in_sign': d['degree_in_sign'],
            'nakshatra': d.get('nakshatra', ''),
            'is_retrograde': d.get('is_retrograde', False),
        }
        for p, d in positions.items()
    }


def _strip(varga: dict) -> dict:
    return {k: v for k, v in varga.items() if k != 'all_positions'}


def _score_label(score: int) -> str:
    if score >= 70: return 'Strong'
    if score >= 45: return 'Moderate'
    return 'Weak'


def _lord_position(lord: str, positions: dict, lagna_sign: int) -> dict:
    key = PLANET_KEY_MAP.get(lord, lord.upper())
    d = positions.get(key, {})
    sign = d.get('sign_index', 0)
    return {
        'sign': SIGNS[sign], 'sign_index': sign,
        'house': (sign - lagna_sign) % 12 + 1,
        'degree_in_sign': d.get('degree_in_sign', 0),
        'nakshatra': d.get('nakshatra', ''),
        'is_retrograde': d.get('is_retrograde', False),
    }


# ── Ashtakavarga — 3rd house (karaka: Mars) ───────────────────────────────

_BAV_STRENGTH = lambda b: 'Strong' if b > 4 else 'Moderate' if b == 4 else 'Weak'
_SAV_STRENGTH = lambda b: 'Strong' if b > 28 else 'Moderate' if b >= 25 else 'Weak'
_PLANETS_7 = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']


def _get_ashtakavarga(positions: dict, third_house_sign: int, third_lord: str) -> dict:
    all_bav = compute_all_bav(positions)
    sav     = compute_sav(all_bav)

    sav_3rd       = sav[third_house_sign]
    lord_bav_3rd  = all_bav.get(third_lord, {}).get(third_house_sign, 0)
    mars_bav_3rd  = all_bav.get('Mars', {}).get(third_house_sign, 0)

    composite = (
        min(int(sav_3rd / 40 * 40), 40) +
        min(int(lord_bav_3rd / 8 * 30), 30) +
        min(int(mars_bav_3rd  / 8 * 30), 30)
    )

    return {
        'third_house_sign': SIGNS[third_house_sign],
        'sav': {
            'bindus': sav_3rd,
            'strength': _SAV_STRENGTH(sav_3rd),
            'thresholds': {'weak': '<25', 'moderate': '25-28', 'strong': '>28'},
        },
        'bav_third_lord': {
            'planet': third_lord,
            'bindus_in_third_house': lord_bav_3rd,
            'strength': _BAV_STRENGTH(lord_bav_3rd),
            'thresholds': {'weak': '<4', 'moderate': '4', 'strong': '>4'},
        },
        'bav_mars': {
            'bindus_in_third_house': mars_bav_3rd,
            'strength': _BAV_STRENGTH(mars_bav_3rd),
            'thresholds': {'weak': '<4', 'moderate': '4', 'strong': '>4'},
        },
        'composite_av_score': composite,
        'full_sav_by_sign': {SIGNS[i]: sav[i] for i in range(12)},
        'full_bav_by_planet': {
            p: {SIGNS[i]: all_bav[p][i] for i in range(12)}
            for p in _PLANETS_7
        },
    }


# ── Dasha relationship with 3rd house ────────────────────────────────────


def _dasha_3rd_relationship(dasha: dict, positions: dict, lagna_sign: int) -> dict:
    third_house_sign = (lagna_sign + 2) % 12
    third_lord = SIGN_LORDS[third_house_sign]

    def planet_rel(planet_name: str) -> dict:
        key  = PLANET_KEY_MAP.get(planet_name, planet_name.upper())
        sign = positions.get(key, {}).get('sign_index', 0)
        house = (sign - lagna_sign) % 12 + 1
        to_3rd = (third_house_sign - sign) % 12 + 1

        if to_3rd in (1, 4, 7, 10):
            rel, fav = 'Kendra (Angular)', True
        elif to_3rd in (5, 9):
            rel, fav = 'Trikona (Trine)', True
        elif to_3rd in (2, 11):
            rel, fav = 'Labha / Dhana', True
        elif to_3rd in (6, 8, 12):
            rel, fav = f'Dusthana ({to_3rd}th from planet)', False
        else:
            rel, fav = 'Neutral (3rd)', True

        return {
            'planet_house': house,
            'planet_sign': SIGNS[sign],
            'houses_to_3rd': to_3rd,
            'relationship_type': rel,
            'is_favorable': fav,
            'activates_3rd_lord': (planet_name == third_lord),
        }

    maha_lord   = dasha['mahadasha']['lord']
    bhukti_lord = dasha['bhukti']['lord']

    maha_rel   = planet_rel(maha_lord)
    bhukti_rel = planet_rel(bhukti_lord)

    both_fav = maha_rel['is_favorable'] and bhukti_rel['is_favorable']
    one_fav  = maha_rel['is_favorable'] or  bhukti_rel['is_favorable']

    activates_parakrama = (
        maha_lord in ('Mars', third_lord) or
        bhukti_lord in ('Mars', third_lord)
    )

    if both_fav and activates_parakrama:
        assessment = 'Highly Favorable: period lords activate 3rd house — courage, travel, and skills flourish'
    elif both_fav:
        assessment = 'Favorable: both period lords support 3rd house significations'
    elif one_fav:
        assessment = 'Mixed: one period lord supports 3rd house; partial activation of themes'
    else:
        assessment = 'Challenging: both lords in dusthana tension — 3rd house themes face delays'

    return {
        'third_lord': third_lord,
        'mahadasha_lord': {'lord': maha_lord, **maha_rel},
        'bhukti_lord':    {'lord': bhukti_lord, **bhukti_rel},
        'activates_parakrama': activates_parakrama,
        'courage_travel_active': both_fav,
        'overall_assessment': assessment,
    }


# ── Main compute ──────────────────────────────────────────────────────────


def compute(
    date_str: str, time_str: str,
    latitude: float, longitude: float,
    timezone_str: str, place_name: str = '',
    current_date_str: str | None = None,
) -> dict:
    t0 = time.time()

    if not current_date_str:
        current_date_str = Date.today().isoformat()

    # Step 1: Planetary positions
    positions = get_positions(date_str, time_str, timezone_str, latitude, longitude)
    lagna_sign        = positions['LAGNA']['sign_index']
    third_house_sign  = (lagna_sign + 2) % 12
    third_lord        = SIGN_LORDS[third_house_sign]

    # Step 2: Varga charts (D-1, D-3, D-9, D-24)
    d1  = analyze_varga(positions, lagna_sign, 1,  house_number=3)
    d3  = analyze_varga(positions, lagna_sign, 3,  house_number=3)
    d9  = analyze_varga(positions, lagna_sign, 9,  house_number=3)
    d24 = analyze_varga(positions, lagna_sign, 24, house_number=3)

    # Step 3: Ashtakavarga (Mars as karaka)
    ashtakavarga = _get_ashtakavarga(positions, third_house_sign, third_lord)

    # Step 4: Dasha-Bhukti
    dasha     = get_dasha_bhukti(positions['MOON']['longitude'], date_str, current_date_str)
    dasha_rel = _dasha_3rd_relationship(dasha, positions, lagna_sign)

    # Step 5: Significations
    siblings      = analyze_siblings(positions, lagna_sign, d3, ashtakavarga)
    courage       = analyze_courage(positions, lagna_sign, ashtakavarga)
    communication = analyze_communication(positions, lagna_sign, d3)
    journeys      = analyze_short_journeys(positions, lagna_sign)
    skills        = analyze_skills_arts(positions, lagna_sign, d24)

    # Step 6: Summary
    composite = (siblings['score'] + courage['score'] +
                 communication['score'] + journeys['score'] + skills['score']) // 5

    key_findings, warnings = [], []
    if courage['score'] >= 70:
        key_findings.append('Strong Parakrama Yoga — exceptional courage and initiative')
    if communication['score'] >= 70:
        key_findings.append('Strong Mercury-3rd connection — gifted communicator or writer')
    if skills['score'] >= 70:
        key_findings.append('High artistic/technical skill potential confirmed by D-24')
    if siblings['score'] < 45:
        warnings.append('Sibling relationships may face karmic challenges — Mars and 3rd lord remedies advised')
    if ashtakavarga['sav']['strength'] == 'Weak':
        warnings.append(f'Weak SAV ({ashtakavarga["sav"]["bindus"]} bindus) — 3rd house needs energising')
    if dasha_rel['courage_travel_active']:
        key_findings.append('Current Dasha-Bhukti activates 3rd house — favourable for bold actions and travel')
    elif not dasha_rel['courage_travel_active']:
        warnings.append('Current period lords not strongly aligned with 3rd house themes')

    elapsed = round((time.time() - t0) * 1000, 2)

    return {
        'status': 'success',
        'computation_time_ms': elapsed,
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
        'third_house': {
            'sign': SIGNS[third_house_sign],
            'sign_index': third_house_sign,
            'lord': third_lord,
            'lord_position': _lord_position(third_lord, positions, lagna_sign),
            'planets_in_house': _planets_in_sign(positions, third_house_sign),
            'aspects_received': _aspects_on_sign(positions, third_house_sign),
        },
        'all_planets_d1': _all_planets_formatted(positions, lagna_sign),
        'varga_analysis': {
            'd1_rasi':        _strip(d1),
            'd3_drekkana':    _strip(d3),
            'd9_navamsha':    _strip(d9),
            'd24_siddhamsha': _strip(d24),
        },
        'ashtakavarga': ashtakavarga,
        'dasha_bhukti': {**dasha, 'relationship_with_3rd_house': dasha_rel},
        'significations': {
            'siblings':      siblings,
            'courage':       courage,
            'communication': communication,
            'short_journeys': journeys,
            'skills_arts':   skills,
        },
        'summary': {
            'overall_3rd_house_strength': _score_label(composite),
            'composite_score': composite,
            'siblings_score':      siblings['score'],
            'courage_score':       courage['score'],
            'communication_score': communication['score'],
            'short_journeys_score': journeys['score'],
            'skills_arts_score':   skills['score'],
            'key_findings': key_findings,
            'warnings': warnings,
            'current_period_assessment': dasha_rel['overall_assessment'],
        },
    }
