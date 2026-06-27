"""
Vimshottari Dasha engine.
Moon nakshatra → birth dasha lord → build full dasha/bhukti timeline.
"""
from __future__ import annotations
from datetime import date, timedelta, datetime
from .constants import (DASHA_ORDER, DASHA_YEARS, TOTAL_DASHA_YEARS,
                         DAYS_PER_YEAR, NAKSHATRA_LORDS, SIGN_LORDS, PLANET_KEY_MAP, SIGNS)


def _moon_nakshatra(moon_lon: float) -> int:
    return int(moon_lon / (360.0 / 27))


def _parse_date(s: str) -> date:
    return datetime.strptime(s, '%Y-%m-%d').date()


# ── Dasha timeline ────────────────────────────────────────────────────────


def _dasha_start_before_birth(moon_lon: float, birth_date: date) -> tuple[date, str]:
    """
    Return the start date of the birth-dasha and its lord.
    (This date is always ≤ birth_date.)
    """
    nak_idx = _moon_nakshatra(moon_lon)
    lord = NAKSHATRA_LORDS[nak_idx % 9]

    nak_span = 360.0 / 27
    deg_in_nak = moon_lon % nak_span
    fraction_elapsed = deg_in_nak / nak_span

    elapsed_days = fraction_elapsed * DASHA_YEARS[lord] * DAYS_PER_YEAR
    dasha_start = birth_date - timedelta(days=elapsed_days)
    return dasha_start, lord


def _walk_dashas(dasha_start: date, start_lord: str,
                 target_date: date) -> tuple[str, date, date]:
    """
    Walk through Mahadashas from dasha_start until we find the one containing
    target_date.  Returns (lord, maha_start, maha_end).
    """
    lord_idx = DASHA_ORDER.index(start_lord)
    cursor = dasha_start
    for i in range(18):          # 120-year cycle runs at most twice in a life
        lord = DASHA_ORDER[(lord_idx + i) % 9]
        maha_end = cursor + timedelta(days=int(DASHA_YEARS[lord] * DAYS_PER_YEAR))
        if cursor <= target_date < maha_end:
            return lord, cursor, maha_end
        cursor = maha_end
    # Fallback (should never happen within 120 years)
    lord = DASHA_ORDER[(lord_idx) % 9]
    return lord, cursor, cursor + timedelta(days=int(DASHA_YEARS[lord] * DAYS_PER_YEAR))


def _walk_bhuktis(maha_lord: str, maha_start: date,
                  target_date: date) -> tuple[str, date, date, list[dict]]:
    lord_idx = DASHA_ORDER.index(maha_lord)
    cursor = maha_start
    all_bhuktis = []
    current = None

    for i in range(9):
        bhukti_lord = DASHA_ORDER[(lord_idx + i) % 9]
        days = (DASHA_YEARS[maha_lord] * DASHA_YEARS[bhukti_lord] / TOTAL_DASHA_YEARS) * DAYS_PER_YEAR
        bhukti_end = cursor + timedelta(days=int(days))
        is_cur = cursor <= target_date < bhukti_end
        all_bhuktis.append({
            'lord': bhukti_lord,
            'start_date': cursor.isoformat(),
            'end_date': bhukti_end.isoformat(),
            'is_current': is_cur,
        })
        if is_cur:
            current = (bhukti_lord, cursor, bhukti_end)
        cursor = bhukti_end

    if current is None:
        current = (all_bhuktis[-1]['lord'],
                   _parse_date(all_bhuktis[-1]['start_date']),
                   _parse_date(all_bhuktis[-1]['end_date']))
    return (*current, all_bhuktis)


def get_dasha_bhukti(moon_lon: float, birth_date_str: str, current_date_str: str) -> dict:
    birth  = _parse_date(birth_date_str)
    today  = _parse_date(current_date_str)

    dasha_start, birth_lord = _dasha_start_before_birth(moon_lon, birth)
    maha_lord, maha_start, maha_end = _walk_dashas(dasha_start, birth_lord, today)
    bhukti_lord, bh_start, bh_end, all_bhuktis = _walk_bhuktis(maha_lord, maha_start, today)

    return {
        'mahadasha': {
            'lord': maha_lord,
            'start_date': maha_start.isoformat(),
            'end_date': maha_end.isoformat(),
            'duration_years': DASHA_YEARS[maha_lord],
            'years_remaining': round((maha_end - today).days / DAYS_PER_YEAR, 2),
        },
        'bhukti': {
            'lord': bhukti_lord,
            'start_date': bh_start.isoformat(),
            'end_date': bh_end.isoformat(),
            'days_remaining': (bh_end - today).days,
        },
        'all_bhuktis_in_mahadasha': all_bhuktis,
    }


# ── 2nd-house relationship analysis ──────────────────────────────────────


def _house_rel(planet_name: str, positions: dict,
               lagna_sign: int, second_house_sign: int) -> dict:
    key = PLANET_KEY_MAP.get(planet_name, planet_name.upper())
    planet_sign = positions.get(key, {}).get('sign_index', 0)
    planet_house = (planet_sign - lagna_sign) % 12 + 1
    from_planet_to_2nd = (second_house_sign - planet_sign) % 12 + 1

    if from_planet_to_2nd in (1, 4, 7, 10):
        rel = 'Kendra (Angular)'
        favorable = True
    elif from_planet_to_2nd in (5, 9):
        rel = 'Trikona (Trine)'
        favorable = True
    elif from_planet_to_2nd in (2, 11):
        rel = 'Labha / Dhana'
        favorable = True
    elif from_planet_to_2nd in (6, 8, 12):
        rel = f'Dusthana ({from_planet_to_2nd}th from planet)'
        favorable = False
    else:
        rel = 'Neutral (3rd)'
        favorable = True

    return {
        'planet_house_in_d1': planet_house,
        'planet_sign': SIGNS[planet_sign],
        'houses_to_2nd': from_planet_to_2nd,
        'relationship_type': rel,
        'is_favorable': favorable,
    }


def analyze_dasha_relationship(dasha_bhukti: dict, positions: dict,
                                lagna_sign: int) -> dict:
    second_house_sign = (lagna_sign + 1) % 12
    seventh_house_sign = (lagna_sign + 6) % 12

    second_lord  = SIGN_LORDS[second_house_sign]
    seventh_lord = SIGN_LORDS[seventh_house_sign]
    maraka_lords = list({second_lord, seventh_lord})

    maha_lord   = dasha_bhukti['mahadasha']['lord']
    bhukti_lord = dasha_bhukti['bhukti']['lord']

    maha_rel   = _house_rel(maha_lord,   positions, lagna_sign, second_house_sign)
    bhukti_rel = _house_rel(bhukti_lord, positions, lagna_sign, second_house_sign)

    maha_is_maraka   = maha_lord   in maraka_lords
    bhukti_is_maraka = bhukti_lord in maraka_lords
    is_maraka_period = maha_is_maraka or bhukti_is_maraka

    both_fav = maha_rel['is_favorable'] and bhukti_rel['is_favorable']
    one_fav  = maha_rel['is_favorable'] or  bhukti_rel['is_favorable']

    if is_maraka_period:
        assessment = (f'Maraka Alert: {maha_lord}/{bhukti_lord} are 2nd/7th lords — '
                      'health vigilance required; avoid major financial risks')
    elif both_fav:
        assessment = 'Highly Favorable: both period lords strengthen 2nd house significations'
    elif one_fav:
        assessment = 'Mixed: one period lord supports 2nd house; moderate expectations'
    else:
        assessment = 'Challenging: both lords in dusthana tension with 2nd house — delays likely'

    return {
        'second_lord_d1': second_lord,
        'seventh_lord_d1': seventh_lord,
        'maraka_lords': maraka_lords,
        'mahadasha_lord': {'lord': maha_lord, 'is_maraka': maha_is_maraka, **maha_rel},
        'bhukti_lord':    {'lord': bhukti_lord, 'is_maraka': bhukti_is_maraka, **bhukti_rel},
        'is_maraka_period': is_maraka_period,
        'wealth_activation': both_fav and not is_maraka_period,
        'overall_assessment': assessment,
    }
