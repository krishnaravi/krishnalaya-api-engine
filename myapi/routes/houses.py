"""
Houses router — POST /api/v1/houses/{house_number}
Dispatches 1-12 to the corresponding house module.
"""
from __future__ import annotations
from datetime import date as Date
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
import pytz

from houses import (house_1, house_2, house_3, house_4, house_5, house_6,
                    house_7, house_8, house_9, house_10, house_11, house_12)

router = APIRouter(prefix='/api/v1/houses', tags=['Houses'])

_MODULES = {
    1: house_1, 2: house_2,   3: house_3,  4: house_4,
    5: house_5, 6: house_6,   7: house_7,  8: house_8,
    9: house_9, 10: house_10, 11: house_11, 12: house_12,
}

_HOUSE_NAMES = {
    1: 'Tanu Bhava — Self, Body, Personality',
    2: 'Dhana Bhava — Wealth, Speech, Family',
    3: 'Sahaja Bhava — Siblings, Courage, Communication',
    4: 'Sukha Bhava — Mother, Happiness, Property',
    5: 'Putra Bhava — Children, Intelligence, Creativity',
    6: 'Ari Bhava — Enemies, Disease, Service',
    7: 'Kalatra Bhava — Spouse, Partnerships, Desire',
    8: 'Randhra Bhava — Longevity, Occult, Transformation',
    9: 'Dharma Bhava — Father, Luck, Higher Wisdom',
    10: 'Karma Bhava — Career, Status, Public Life',
    11: 'Labha Bhava — Gains, Wishes, Elder Siblings',
    12: 'Vyaya Bhava — Loss, Foreign, Liberation',
}


class BirthInput(BaseModel):
    date:         str   = Field(..., examples=['1990-05-15'])
    time:         str   = Field(..., examples=['06:30:00'])
    latitude:     float = Field(..., ge=-90,  le=90,  examples=[13.0827])
    longitude:    float = Field(..., ge=-180, le=180, examples=[80.2707])
    timezone:     str   = Field(..., examples=['Asia/Kolkata'])
    place:        str   = Field('', max_length=100)
    current_date: str | None = Field(None, examples=['2026-06-27'])

    @field_validator('date')
    @classmethod
    def _vdate(cls, v: str) -> str:
        datetime.strptime(v, '%Y-%m-%d'); return v

    @field_validator('time')
    @classmethod
    def _vtime(cls, v: str) -> str:
        datetime.strptime(v, '%H:%M:%S'); return v

    @field_validator('current_date')
    @classmethod
    def _vcdate(cls, v: str | None) -> str | None:
        if v: datetime.strptime(v, '%Y-%m-%d')
        return v

    @field_validator('timezone')
    @classmethod
    def _vtz(cls, v: str) -> str:
        if v not in pytz.all_timezones_set:
            raise ValueError(f'Unknown timezone: {v}')
        return v


@router.get('/catalogue', summary='List all 12 house endpoints')
async def list_houses() -> dict:
    return {
        'houses': [
            {'number': n, 'description': desc, 'endpoint': f'/api/v1/houses/{n}'}
            for n, desc in _HOUSE_NAMES.items()
        ]
    }


@router.post('/{house_number}',
             summary='Full Vedic analysis for any house (1-12)',
             description=(
                 'POST birth data to analyse any of the 12 Bhavas. '
                 'Returns lord position, occupants, aspects, Ashtakavarga, '
                 'Varga Bala, Dasha-Bhukti activation, and house-specific karakatwa analysis.'
             ))
async def analyze_house(house_number: int, body: BirthInput) -> dict:
    module = _MODULES.get(house_number)
    if module is None:
        raise HTTPException(
            status_code=404,
            detail=f'House {house_number} not found. Valid range: 1-12.'
        )
    try:
        return module.compute(
            date_str=body.date,
            time_str=body.time,
            latitude=body.latitude,
            longitude=body.longitude,
            timezone_str=body.timezone,
            place_name=body.place,
            current_date_str=body.current_date or Date.today().isoformat(),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
