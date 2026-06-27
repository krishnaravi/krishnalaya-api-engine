"""
Generic house analysis engine — shared by all 12 house modules.

analyze_house(config, ...) orchestrates:
  1. Planetary positions (Swiss Ephemeris / Lahiri)
  2. House sign, lord, occupants, aspects received
  3. Ashtakavarga (SAV + BAV lord + BAV karaka)
  4. Varga analysis across preferred divisional charts
  5. Varga Bala (Vaiseshikamsa) for the house lord
  6. Dasha-Bhukti activation of this house
  7. Karakatwa (signification) strength assessment
  8. Summary score and findings
"""
from __future__ import annotations
import time
from datetime import date as Date

from core.planetary import get_positions
from core.varga import analyze_varga, compute_varga_bala
from core.ashtakavarga import get_house_av, compute_all_bav, compute_sav
from core.dasha import get_dasha_bhukti
from core.constants import (SIGNS, SIGN_LORDS, PLANET_KEY_MAP, HOUSE_NAMES,
                              HOUSE_TYPES, NATURAL_FRIENDS, NATURAL_ENEMIES,
                              EXALTATION, DEBILITATION, OWN_SIGNS, MOOLATRIKONA)

_PLANETS_7 = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']

_SPECIAL_ASPECTS: dict[str, list[int]] = {
    'MARS':    [4, 8],
    'JUPITER': [5, 9],
    'SATURN':  [3, 10],
    'RAHU':    [5, 9],
    'KETU':    [5, 9],
}

_BENEFICS = {'Jupiter', 'Venus', 'Moon', 'Mercury'}
_MALEFICS = {'Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu'}


# ── Helpers ───────────────────────────────────────────────────────────────


def _aspects_on_sign(positions: dict, target: int) -> list[dict]:
    out = []
    for planet, data in positions.items():
        if planet == 'LAGNA':
            continue
        ps = data['sign_index']
        if ps == target:
            continue
        offsets = [7] + _SPECIAL_ASPECTS.get(planet, [])
        for off in offsets:
            if (ps + off - 1) % 12 == target:
                pname = planet.title()
                out.append({
                    'planet': pname,
                    'from_sign': SIGNS[ps],
                    'from_house': None,          # filled later
                    'nature': 'Benefic' if pname in _BENEFICS else 'Malefic',
                    'aspect_type': f'{off}th aspect',
                })
                break
    return out


def _planets_in_sign(positions: dict, sign: int) -> list[dict]:
    out = []
    for p, d in positions.items():
        if p == 'LAGNA':
            continue
        if d['sign_index'] == sign:
            pname = p.title()
            out.append({
                'planet': pname,
                'degree_in_sign': round(d['degree_in_sign'], 2),
                'nakshatra': d.get('nakshatra', ''),
                'is_retrograde': d.get('is_retrograde', False),
                'nature': 'Benefic' if pname in _BENEFICS else 'Malefic',
            })
    return out


def _lord_info(lord: str, positions: dict, lagna_sign: int) -> dict:
    key  = PLANET_KEY_MAP.get(lord, lord.upper())
    data = positions.get(key, {})
    sign = data.get('sign_index', 0)
    house = (sign - lagna_sign) % 12 + 1

    # Dignity
    dig = 'Neutral'
    if lord in EXALTATION:
        if sign == EXALTATION[lord]:          dig = 'Exalted'
        elif sign == DEBILITATION.get(lord):  dig = 'Debilitated'
        elif sign in OWN_SIGNS.get(lord, []):
            dig = 'Moolatrikona' if sign == MOOLATRIKONA.get(lord) else 'Own Sign'
        else:
            sign_lord = SIGN_LORDS[sign]
            if sign_lord in NATURAL_FRIENDS.get(lord, []):   dig = 'Friendly'
            elif sign_lord in NATURAL_ENEMIES.get(lord, []): dig = 'Enemy'

    dig_score = {'Exalted': 5, 'Moolatrikona': 4, 'Own Sign': 4,
                 'Friendly': 3, 'Neutral': 2, 'Enemy': 1, 'Debilitated': 0}.get(dig, 2)

    # Lord strength score (0-100)
    lord_score = dig_score * 20

    # Benefic/auspicious houses bonus
    if house in (1, 4, 7, 10, 5, 9):   lord_score = min(100, lord_score + 10)
    if house in (6, 8, 12):             lord_score = max(0, lord_score - 20)
    if data.get('is_retrograde'):       lord_score = max(0, lord_score - 5)

    return {
        'planet': lord,
        'sign': SIGNS[sign],
        'sign_index': sign,
        'house': house,
        'degree_in_sign': round(data.get('degree_in_sign', 0), 2),
        'nakshatra': data.get('nakshatra', ''),
        'is_retrograde': data.get('is_retrograde', False),
        'dignity': dig,
        'dignity_score': dig_score,
        'lord_strength_score': lord_score,
    }


def _karaka_info(karaka: str, positions: dict, lagna_sign: int) -> dict:
    info = _lord_info(karaka, positions, lagna_sign)
    info['role'] = 'Natural Significator'
    return info


def _dasha_house_relation(dasha: dict, positions: dict,
                          lagna_sign: int, house_number: int) -> dict:
    house_sign = (lagna_sign + house_number - 1) % 12
    house_lord = SIGN_LORDS[house_sign]

    def _rel(planet_name: str) -> dict:
        key   = PLANET_KEY_MAP.get(planet_name, planet_name.upper())
        sign  = positions.get(key, {}).get('sign_index', 0)
        house = (sign - lagna_sign) % 12 + 1
        to_h  = (house_sign - sign) % 12 + 1

        if to_h in (1, 4, 7, 10):   rel_type, fav = 'Kendra',   True
        elif to_h in (5, 9):         rel_type, fav = 'Trikona',  True
        elif to_h in (2, 11):        rel_type, fav = 'Labha/Dhana', True
        elif to_h in (6, 8, 12):     rel_type, fav = f'Dusthana ({to_h}th)', False
        else:                        rel_type, fav = f'Neutral ({to_h}th)', True

        activates = (planet_name == house_lord)
        return {
            'planet': planet_name,
            'planet_sign': SIGNS[sign],
            'planet_house': house,
            'houses_to_target': to_h,
            'relationship_type': rel_type,
            'is_favorable': fav,
            'activates_house_lord': activates,
        }

    maha_lord   = dasha['mahadasha']['lord']
    bhukti_lord = dasha['bhukti']['lord']
    maha_rel    = _rel(maha_lord)
    bhukti_rel  = _rel(bhukti_lord)

    both_fav = maha_rel['is_favorable'] and bhukti_rel['is_favorable']
    one_fav  = maha_rel['is_favorable'] or  bhukti_rel['is_favorable']
    lord_active = maha_rel['activates_house_lord'] or bhukti_rel['activates_house_lord']

    if both_fav and lord_active:
        assess = f'Highly Favorable — both period lords activate {house_number}th house themes'
    elif both_fav:
        assess = f'Favorable — period lords support {house_number}th house significations'
    elif one_fav:
        assess = f'Mixed — partial {house_number}th house activation'
    else:
        assess = f'Challenging — period lords in dusthana tension with {house_number}th house'

    return {
        'house_lord': house_lord,
        'mahadasha': {**dasha['mahadasha'], **maha_rel},
        'bhukti':    {**dasha['bhukti'],    **bhukti_rel},
        'house_lord_activated': lord_active,
        'is_favorable': both_fav,
        'is_mixed': one_fav and not both_fav,
        'overall_assessment': assess,
    }


def _all_planets_d1(positions: dict, lagna_sign: int) -> dict:
    return {
        p: {
            'sign': d['sign'],
            'sign_index': d['sign_index'],
            'house': (d['sign_index'] - lagna_sign) % 12 + 1 if p != 'LAGNA' else 1,
            'degree_in_sign': round(d['degree_in_sign'], 2),
            'nakshatra': d.get('nakshatra', ''),
            'pada': d.get('pada', 0),
            'is_retrograde': d.get('is_retrograde', False),
            'sign_lord': SIGN_LORDS[d['sign_index']],
        }
        for p, d in positions.items()
    }


def _score_label(score: int) -> str:
    if score >= 75: return 'Very Strong'
    if score >= 55: return 'Strong'
    if score >= 40: return 'Moderate'
    if score >= 25: return 'Weak'
    return 'Very Weak'


def _benefic_malefic_balance(planets: list[dict]) -> dict:
    benefics  = [p['planet'] for p in planets if p['nature'] == 'Benefic']
    malefics  = [p['planet'] for p in planets if p['nature'] == 'Malefic']
    if benefics and not malefics: bal, score = 'Benefic occupation', 70
    elif malefics and not benefics: bal, score = 'Malefic occupation', 30
    elif benefics and malefics: bal, score = 'Mixed occupation', 50
    else: bal, score = 'Empty (unoccupied)', 50
    return {'label': bal, 'benefics': benefics, 'malefics': malefics, 'score': score}


# ── Main orchestrator ─────────────────────────────────────────────────────


def analyze_house(
    config: dict,
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

    house_num  = config['number']
    karakas    = config.get('karakas', [])
    primary_ka = config.get('primary_karaka', karakas[0] if karakas else None)
    vargas     = config.get('preferred_vargas', [1, 9, 10, 12, 24, 60])

    # ── Step 1: Positions ──────────────────────────────────────────────────
    positions   = get_positions(date_str, time_str, timezone_str, latitude, longitude)
    lagna_sign  = positions['LAGNA']['sign_index']
    house_sign  = (lagna_sign + house_num - 1) % 12
    lord        = SIGN_LORDS[house_sign]

    # ── Step 2: House occupants and aspects ───────────────────────────────
    occupants = _planets_in_sign(positions, house_sign)
    aspects   = _aspects_on_sign(positions, house_sign)
    for a in aspects:
        a['from_house'] = (positions[PLANET_KEY_MAP.get(
            a['planet'], a['planet'].upper())]['sign_index'] - lagna_sign) % 12 + 1

    occupation = _benefic_malefic_balance(occupants)

    # ── Step 3: Lord and karaka analysis ─────────────────────────────────
    lord_data = _lord_info(lord, positions, lagna_sign)
    karaka_data = {k: _karaka_info(k, positions, lagna_sign) for k in karakas}

    # ── Step 4: Ashtakavarga ──────────────────────────────────────────────
    av = get_house_av(positions, house_sign, lord, primary_ka)

    # ── Step 5: Varga analysis ────────────────────────────────────────────
    varga_results = {}
    for v in vargas:
        try:
            res = analyze_varga(positions, lagna_sign, v, house_number=house_num)
            key = res['varga'].replace(' ', '_').replace('-', '').lower()
            res_stripped = {k: val for k, val in res.items() if k != 'all_positions'}
            varga_results[key] = res_stripped
        except Exception:
            pass

    # ── Step 6: Varga Bala for lord ───────────────────────────────────────
    varga_bala = compute_varga_bala(lord, positions, vargas)

    # ── Step 7: Dasha-Bhukti ─────────────────────────────────────────────
    dasha     = get_dasha_bhukti(positions['MOON']['longitude'], date_str, current_date_str)
    dasha_rel = _dasha_house_relation(dasha, positions, lagna_sign, house_num)

    # ── Step 8: Composite scoring ─────────────────────────────────────────
    sav_bindus  = av['sav']['bindus']
    sav_sc      = min(int(sav_bindus / 40 * 35), 35)
    lord_sc     = min(lord_data['lord_strength_score'] * 35 // 100, 35)
    occ_sc      = min(occupation['score'] * 20 // 100, 20)
    dasha_sc    = 10 if dasha_rel['is_favorable'] else (5 if dasha_rel['is_mixed'] else 0)
    composite   = sav_sc + lord_sc + occ_sc + dasha_sc

    # ── Step 9: Key findings and warnings ────────────────────────────────
    findings, warnings = [], []
    if lord_data['dignity'] in ('Exalted', 'Moolatrikona', 'Own Sign'):
        findings.append(f'House lord {lord} is {lord_data["dignity"]} — strong house')
    if lord_data['dignity'] == 'Debilitated':
        warnings.append(f'House lord {lord} is Debilitated — house significations weakened')
    if lord_data['is_retrograde']:
        findings.append(f'{lord} is retrograde — intensified but unpredictable results')
    if sav_bindus > 28:
        findings.append(f'Strong SAV ({sav_bindus} bindus) in this house')
    elif sav_bindus < 25:
        warnings.append(f'Weak SAV ({sav_bindus} bindus) — house needs strengthening')
    benefic_aspects = [a for a in aspects if a['nature'] == 'Benefic']
    malefic_aspects = [a for a in aspects if a['nature'] == 'Malefic']
    if benefic_aspects:
        findings.append(f"Benefic aspects from {', '.join(a['planet'] for a in benefic_aspects)}")
    if malefic_aspects:
        warnings.append(f"Malefic aspects from {', '.join(a['planet'] for a in malefic_aspects)}")
    if dasha_rel['is_favorable']:
        findings.append(f"Current {dasha['mahadasha']['lord']}/{dasha['bhukti']['lord']} dasha activates this house")
    if varga_bala['strength'] in ('Very Strong', 'Strong'):
        findings.append(f"Lord {lord} shows {varga_bala['strength'].lower()} varga bala")

    house_name_tuple = HOUSE_NAMES.get(house_num, (f'House {house_num}', '', ''))
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
            'degree_in_sign': round(positions['LAGNA']['degree_in_sign'], 2),
            'nakshatra': positions['LAGNA']['nakshatra'],
            'lord': SIGN_LORDS[lagna_sign],
        },
        'all_planets': _all_planets_d1(positions, lagna_sign),
        'house': {
            'number': house_num,
            'name': house_name_tuple[0],
            'english_name': house_name_tuple[1],
            'natural_karaka': house_name_tuple[2],
            'house_types': HOUSE_TYPES.get(house_num, []),
            'natural_significations': config.get('natural_significations', []),
            'body_parts': config.get('body_parts', []),
            'sign': SIGNS[house_sign],
            'sign_index': house_sign,
            'lord': lord,
            'lord_info': lord_data,
            'karakas': karaka_data,
            'planets_in_house': occupants,
            'house_occupation': occupation,
            'aspects_received': aspects,
        },
        'ashtakavarga': av,
        'varga_analysis': varga_results,
        'varga_bala_lord': varga_bala,
        'dasha_bhukti': {**dasha, 'house_activation': dasha_rel},
        # significations added by each house module
        'summary': {
            'house_strength': _score_label(composite),
            'composite_score': composite,
            'scoring_breakdown': {
                'sav_score': sav_sc,
                'lord_strength_score': lord_sc,
                'occupation_score': occ_sc,
                'dasha_score': dasha_sc,
            },
            'key_findings': findings,
            'warnings': warnings,
            'current_period_assessment': dasha_rel['overall_assessment'],
        },
        '_positions': positions,    # private — for house-specific signification analysis
        '_lagna_sign': lagna_sign,
        '_house_sign': house_sign,
        '_lord': lord,
        '_dasha': dasha,
    }


def finalize(result: dict) -> dict:
    """Strip private underscore keys before returning to the client."""
    return {k: v for k, v in result.items() if not k.startswith('_')}
