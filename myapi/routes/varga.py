"""
Varga (Divisional Chart) router — POST /api/v1/varga/{chart_type}
Returns a full divisional chart with all 12 houses and planetary positions.

Supported chart types: d1, d2, d3, d9, d10, d12, d16, d24, d60
"""
from __future__ import annotations
from datetime import date as Date, datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
import pytz

from core.planetary import get_positions
from core.varga import get_full_varga_chart, compute_varga_bala, get_varga_sign, _VARGA_LABELS, _VARGA_THEMES

router = APIRouter(prefix='/api/v1/varga', tags=['Varga Charts'])

_VARGA_MAP: dict[str, int] = {
    'd1': 1, 'd2': 2, 'd3': 3, 'd9': 9, 'd10': 10,
    'd12': 12, 'd16': 16, 'd24': 24, 'd60': 60,
}

_PLANETS_9 = ['SUN', 'MOON', 'MARS', 'MERCURY', 'JUPITER', 'VENUS', 'SATURN', 'RAHU', 'KETU']
_PLANETS_7 = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']


class BirthInput(BaseModel):
    date:         str   = Field(..., examples=['1990-05-15'])
    time:         str   = Field(..., examples=['06:30:00'])
    latitude:     float = Field(..., ge=-90,  le=90,  examples=[13.0827])
    longitude:    float = Field(..., ge=-180, le=180, examples=[80.2707])
    timezone:     str   = Field(..., examples=['Asia/Kolkata'])
    place:        str   = Field('', max_length=100)
    current_date: str | None = Field(None)

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


@router.get('/catalogue', summary='List all supported divisional charts')
async def list_vargas() -> dict:
    return {
        'supported_charts': [
            {
                'key': k,
                'varga_number': v,
                'label': _VARGA_LABELS.get(v, f'D-{v}'),
                'theme': _VARGA_THEMES.get(v, ''),
                'endpoint': f'/api/v1/varga/{k}',
            }
            for k, v in _VARGA_MAP.items()
        ]
    }


@router.post('/{chart_type}',
             summary='Full divisional chart (D-1 through D-60)',
             description=(
                 'Returns the complete varga chart: Lagna, all 12 houses with lords and '
                 'occupants, planetary positions, dignity, and Varga Bala for all 7 planets.'
             ))
async def get_varga_chart(chart_type: str, body: BirthInput) -> dict:
    varga_num = _VARGA_MAP.get(chart_type.lower())
    if varga_num is None:
        raise HTTPException(
            status_code=404,
            detail=f'Chart type "{chart_type}" not supported. Valid options: {list(_VARGA_MAP.keys())}'
        )
    try:
        positions  = get_positions(body.date, body.time, body.timezone, body.latitude, body.longitude)
        lagna_sign = positions['LAGNA']['sign_index']

        chart = get_full_varga_chart(positions, lagna_sign, varga_num)

        # Varga Bala for all 7 planets in this specific varga
        varga_bala = {
            p: compute_varga_bala(p, positions, [varga_num])
            for p in _PLANETS_7
        }

        return {
            'status': 'success',
            'input': {
                'date': body.date, 'time': body.time,
                'latitude': body.latitude, 'longitude': body.longitude,
                'timezone': body.timezone, 'place': body.place,
            },
            'chart_type': chart_type.upper(),
            'varga_number': varga_num,
            'label': _VARGA_LABELS.get(varga_num, f'D-{varga_num}'),
            'theme': _VARGA_THEMES.get(varga_num, ''),
            'chart': chart,
            'varga_bala_in_this_chart': varga_bala,
            'd1_reference': {
                p: {
                    'sign': positions[p]['sign'],
                    'longitude': round(positions[p]['longitude'], 4),
                }
                for p in _PLANETS_9 + ['LAGNA']
                if p in positions
            },
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post('/all/summary',
             summary='All 9 varga charts for one birth data',
             description='Returns a summary of D-1, D-9, D-10, D-12, D-24, D-60 positions for all planets.')
async def all_vargas_summary(body: BirthInput) -> dict:
    try:
        positions  = get_positions(body.date, body.time, body.timezone, body.latitude, body.longitude)
        lagna_sign = positions['LAGNA']['sign_index']

        from core.constants import SIGNS
        summaries: dict[str, dict] = {}

        for key, v_num in _VARGA_MAP.items():
            try:
                chart = get_full_varga_chart(positions, lagna_sign, v_num)
                summaries[key] = {
                    'label': _VARGA_LABELS.get(v_num, f'D-{v_num}'),
                    'theme': _VARGA_THEMES.get(v_num, ''),
                    'lagna': chart['lagna'],
                    'planet_positions': chart['planet_positions'],
                }
            except Exception:
                pass

        # Overall Varga Bala across all supported vargas
        overall_bala = {
            p: compute_varga_bala(p, positions, list(_VARGA_MAP.values()))
            for p in _PLANETS_7
        }

        return {
            'status': 'success',
            'input': {
                'date': body.date, 'time': body.time,
                'timezone': body.timezone,
            },
            'd1_lagna': SIGNS[lagna_sign],
            'varga_summaries': summaries,
            'overall_varga_bala': overall_bala,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
