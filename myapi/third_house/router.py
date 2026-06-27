from __future__ import annotations
from datetime import date as Date, datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
import pytz

from .calculator import compute

router = APIRouter(prefix='/api/v1/houses', tags=['3rd House'])


class BirthInput(BaseModel):
    date:         str   = Field(..., examples=['1990-05-15'])
    time:         str   = Field(..., examples=['06:30:00'])
    latitude:     float = Field(..., ge=-90,  le=90,  examples=[13.0827])
    longitude:    float = Field(..., ge=-180, le=180, examples=[80.2707])
    timezone:     str   = Field(..., examples=['Asia/Kolkata'])
    place:        str   = Field('',  max_length=100)
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


@router.post('/third', summary='3rd House (Sahaja/Vikrama Bhava) analysis')
async def third_house(body: BirthInput) -> dict:
    """
    Full Vedic 3rd-house analysis:
    - D-1 / D-3 (Drekkana) / D-9 / D-24 (Siddhamsha) varga mapping
    - Ashtakavarga SAV + BAV of 3rd lord & Mars (karaka)
    - Vimshottari Dasha-Bhukti with 3rd-house relationship
    - Significations: siblings, courage, communication, journeys, skills/arts
    """
    try:
        return compute(
            date_str=body.date, time_str=body.time,
            latitude=body.latitude, longitude=body.longitude,
            timezone_str=body.timezone, place_name=body.place,
            current_date_str=body.current_date or Date.today().isoformat(),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
