"""
FastAPI router for POST /api/v1/houses/second
"""
from __future__ import annotations
from datetime import date as Date, datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from .calculator import compute

router = APIRouter(prefix='/api/v1/houses', tags=['2nd House'])


class BirthInput(BaseModel):
    date: str = Field(..., examples=['1990-05-15'],
                      description='Birth date YYYY-MM-DD')
    time: str = Field(..., examples=['06:30:00'],
                      description='Birth time HH:MM:SS (local)')
    latitude:  float = Field(..., ge=-90, le=90,  examples=[13.0827])
    longitude: float = Field(..., ge=-180, le=180, examples=[80.2707])
    timezone:  str   = Field(..., examples=['Asia/Kolkata'])
    place:     str   = Field('', max_length=100, examples=['Chennai'])
    current_date: str | None = Field(
        None, examples=['2026-06-27'],
        description='Date for dasha calculation (defaults to today)')

    @field_validator('date')
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('date must be YYYY-MM-DD')
        return v

    @field_validator('time')
    @classmethod
    def validate_time(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%H:%M:%S')
        except ValueError:
            raise ValueError('time must be HH:MM:SS')
        return v

    @field_validator('current_date')
    @classmethod
    def validate_current_date(cls, v: str | None) -> str | None:
        if v is None:
            return None
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('current_date must be YYYY-MM-DD')
        return v

    @field_validator('timezone')
    @classmethod
    def validate_tz(cls, v: str) -> str:
        import pytz
        if v not in pytz.all_timezones_set:
            raise ValueError(f'Unknown timezone: {v}')
        return v


@router.post('/second', summary='2nd House (Dhana/Vak Sthana) analysis')
async def second_house(body: BirthInput) -> dict:
    """
    Full Vedic 2nd-house analysis including:
    - D1/D2/D9/D16 varga mapping
    - Ashtakavarga (SAV + BAV of 2nd lord & Jupiter)
    - Vimshottari Dasha-Bhukti with 2nd-house relationship
    - Significations: wealth, speech-career, childbirth, Maraka
    """
    try:
        result = compute(
            date_str=body.date,
            time_str=body.time,
            latitude=body.latitude,
            longitude=body.longitude,
            timezone_str=body.timezone,
            place_name=body.place,
            current_date_str=body.current_date or Date.today().isoformat(),
        )
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
