"""
Ashtakavarga router.

POST /api/v1/ashtakavarga/bav      — BAV for all 7 planets + Prashtara tables
POST /api/v1/ashtakavarga/sav      — SAV (total=337) + strength per sign
POST /api/v1/ashtakavarga/shodhana — Trikona + Ekadhipatya Shodhana result
"""
from __future__ import annotations
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
import pytz

from core.planetary import get_positions
from core.ashtakavarga import (
    compute_all_bav, compute_sav, get_bav_report, get_full_ashtakavarga,
    trikona_shodhana, ekadhipatya_shodhana,
)
from core.constants import SIGNS, SIGN_LORDS

router = APIRouter(prefix='/api/v1/ashtakavarga', tags=['Ashtakavarga'])

_PLANETS_7 = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']

_EXPECTED_TOTALS = {
    'Sun': 48, 'Moon': 49, 'Mars': 39, 'Mercury': 54,
    'Jupiter': 56, 'Venus': 52, 'Saturn': 39, 'SAV': 337,
}


class BirthInput(BaseModel):
    date:      str   = Field(..., examples=['1990-05-15'])
    time:      str   = Field(..., examples=['06:30:00'])
    latitude:  float = Field(..., ge=-90,  le=90,  examples=[13.0827])
    longitude: float = Field(..., ge=-180, le=180, examples=[80.2707])
    timezone:  str   = Field(..., examples=['Asia/Kolkata'])
    place:     str   = Field('', max_length=100)

    @field_validator('date')
    @classmethod
    def _vdate(cls, v: str) -> str:
        datetime.strptime(v, '%Y-%m-%d'); return v

    @field_validator('time')
    @classmethod
    def _vtime(cls, v: str) -> str:
        datetime.strptime(v, '%H:%M:%S'); return v

    @field_validator('timezone')
    @classmethod
    def _vtz(cls, v: str) -> str:
        if v not in pytz.all_timezones_set:
            raise ValueError(f'Unknown timezone: {v}')
        return v


def _sav_strength(b: int) -> str:
    if b < 25: return 'Weak'
    if b <= 28: return 'Moderate'
    return 'Strong'


def _bav_strength(b: int) -> str:
    if b < 4: return 'Weak'
    if b == 4: return 'Moderate'
    return 'Strong'


@router.post('/bav',
             summary='Bhinnashtakavarga — all 7 planets with Prashtara tables',
             description=(
                 'Computes the Bhinnashtakavarga (BAV) for each of the 7 planets. '
                 'Returns bindu counts per sign, Prashtara reference table, and '
                 'Trikona-Shodhana reduced values.'
             ))
async def get_bav(body: BirthInput) -> dict:
    try:
        positions = get_positions(body.date, body.time, body.timezone, body.latitude, body.longitude)
        lagna_sign = positions['LAGNA']['sign_index']

        reports = {p: get_bav_report(p, positions) for p in _PLANETS_7}
        totals  = {p: reports[p]['bav_total'] for p in _PLANETS_7}
        sav_total = sum(totals.values())

        return {
            'status': 'success',
            'input': {'date': body.date, 'time': body.time, 'timezone': body.timezone},
            'lagna': {'sign': SIGNS[lagna_sign], 'sign_index': lagna_sign},
            'sav_total_raw': sav_total,
            'expected_sav_total': 337,
            'planet_reports': reports,
            'bav_totals': {
                p: {
                    'actual': totals[p],
                    'expected': _EXPECTED_TOTALS.get(p, '?'),
                    'match': totals[p] == _EXPECTED_TOTALS.get(p),
                }
                for p in _PLANETS_7
            },
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post('/sav',
             summary='Sarvashtakavarga — total bindus per sign (should equal 337)',
             description=(
                 'Returns the Sarvashtakavarga (SAV) — sum of all 7 planets\' BAV '
                 'per sign. Total across all 12 signs = 337 (Parashari standard). '
                 'Includes strength rating and transit recommendations.'
             ))
async def get_sav(body: BirthInput) -> dict:
    try:
        positions  = get_positions(body.date, body.time, body.timezone, body.latitude, body.longitude)
        lagna_sign = positions['LAGNA']['sign_index']
        all_bav    = compute_all_bav(positions)
        sav        = compute_sav(all_bav)
        total      = sum(sav.values())

        # Sort signs by strength
        sorted_by_strength = sorted(range(12), key=lambda i: sav[i], reverse=True)

        # House-wise SAV (from Lagna perspective)
        house_sav = {}
        for h in range(1, 13):
            h_sign = (lagna_sign + h - 1) % 12
            bindus = sav[h_sign]
            house_sav[str(h)] = {
                'sign': SIGNS[h_sign],
                'bindus': bindus,
                'strength': _sav_strength(bindus),
                'lord': SIGN_LORDS[h_sign],
            }

        return {
            'status': 'success',
            'input': {'date': body.date, 'time': body.time, 'timezone': body.timezone},
            'lagna': {'sign': SIGNS[lagna_sign], 'sign_index': lagna_sign},
            'sav_by_sign': {SIGNS[i]: {'bindus': sav[i], 'strength': _sav_strength(sav[i])} for i in range(12)},
            'sav_by_house': house_sav,
            'sav_total': total,
            'expected_total': 337,
            'total_matches': total == 337,
            'strongest_signs': [SIGNS[i] for i in sorted_by_strength[:4]],
            'weakest_signs':   [SIGNS[i] for i in sorted_by_strength[-4:]],
            'transit_recommendations': {
                'favourable_transits': [SIGNS[i] for i in range(12) if sav[i] > 28],
                'avoid_transits':      [SIGNS[i] for i in range(12) if sav[i] < 25],
                'note': 'Transit planets give best results when transiting signs with SAV > 28',
            },
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post('/shodhana',
             summary='Trikona + Ekadhipatya Shodhana — reduced Ashtakavarga',
             description=(
                 'Applies classical Shodhana (reduction) to the Ashtakavarga: '
                 '1) Trikona Shodhana — trine group reduction per planet BAV, '
                 '2) Ekadhipatya Shodhana — dual-lord sign reduction on Sodhya SAV. '
                 'Returns raw, intermediate, and final reduced values.'
             ))
async def get_shodhana(body: BirthInput) -> dict:
    try:
        positions  = get_positions(body.date, body.time, body.timezone, body.latitude, body.longitude)
        lagna_sign = positions['LAGNA']['sign_index']

        result = get_full_ashtakavarga(positions)

        # Add house context to final SAV
        final_sav_raw = {SIGNS[i]: result['after_ekadhipatya_shodhana']['sav'][SIGNS[i]]
                         for i in range(12)}
        house_final = {}
        for h in range(1, 13):
            h_sign = (lagna_sign + h - 1) % 12
            sign_name = SIGNS[h_sign]
            bindus = final_sav_raw[sign_name]
            house_final[str(h)] = {
                'sign': sign_name,
                'bindus': bindus,
                'strength': _sav_strength(bindus),
            }

        return {
            'status': 'success',
            'input': {'date': body.date, 'time': body.time, 'timezone': body.timezone},
            'lagna': {'sign': SIGNS[lagna_sign], 'sign_index': lagna_sign},
            'step_1_raw_sav': {
                'sav': result['raw']['sav'],
                'total': result['raw']['sav_total'],
                'note': 'Classical Parashari SAV — should total 337',
            },
            'step_2_trikona_shodhana': {
                'reduced_bav_per_planet': result['after_trikona_shodhana']['bav'],
                'sodhya_sav': result['after_trikona_shodhana']['sav'],
                'total': result['after_trikona_shodhana']['sav_total'],
                'explanation': (
                    'For each trine group (1-5-9, 2-6-10, 3-7-11, 4-8-12): '
                    'subtract the minimum bindu count from all three signs in each group.'
                ),
            },
            'step_3_ekadhipatya_shodhana': {
                'final_sav_by_sign': result['after_ekadhipatya_shodhana']['sav'],
                'final_sav_by_house': house_final,
                'total': result['after_ekadhipatya_shodhana']['sav_total'],
                'sav_strength': result['after_ekadhipatya_shodhana']['sav_strength'],
                'explanation': (
                    'For planets ruling two signs: if one sign is occupied and the other not, '
                    'zero the unoccupied sign. If neither occupied, zero the weaker sign.'
                ),
            },
            'insights': result['insights'],
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
