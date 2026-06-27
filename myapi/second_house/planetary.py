"""
Planetary position engine using pyswisseph with Lahiri ayanamsha (sidereal).
Ephemeris path: /root/swisseph/ephe
"""
from __future__ import annotations

import swisseph as swe
import pytz
from datetime import datetime
from typing import Any

from .constants import SIGNS, SIGN_LORDS, NAKSHATRA_NAMES

EPHE_PATH = '/root/swisseph/ephe'

SWE_PLANET_IDS: dict[str, int] = {
    'SUN':     swe.SUN,
    'MOON':    swe.MOON,
    'MERCURY': swe.MERCURY,
    'VENUS':   swe.VENUS,
    'MARS':    swe.MARS,
    'JUPITER': swe.JUPITER,
    'SATURN':  swe.SATURN,
    'RAHU':    swe.TRUE_NODE,
}

_SWE_FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED


def _init_swe() -> None:
    swe.set_ephe_path(EPHE_PATH)
    swe.set_sid_mode(swe.SIDM_LAHIRI)


def _to_jd(date_str: str, time_str: str, tz_str: str) -> float:
    local_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    tz = pytz.timezone(tz_str)
    utc_dt = tz.localize(local_dt).astimezone(pytz.utc)
    hour = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, hour)


def _calc_planet(jd: float, swe_id: int) -> tuple[float, float]:
    """Returns (sidereal_longitude, speed_longitude).

    pyswisseph 2.x: calc_ut returns ((lon,lat,dist,spd_lon,spd_lat,spd_dist), retcode)
    """
    result = swe.calc_ut(jd, swe_id, _SWE_FLAGS)
    # result[0] is the 6-value tuple; result[1] is the int return code
    xx = result[0] if isinstance(result[0], (list, tuple)) else result
    lon   = float(xx[0]) % 360
    speed = float(xx[3])
    return lon, speed


def _nak_pada(lon: float) -> tuple[int, int, str]:
    nak_span = 360.0 / 27
    nak_idx = int(lon / nak_span)
    pada = int((lon % nak_span) / (nak_span / 4)) + 1
    return nak_idx, pada, NAKSHATRA_NAMES[nak_idx]


def _planet_dict(lon: float, speed: float) -> dict[str, Any]:
    sign_idx = int(lon / 30) % 12
    deg_in_sign = lon % 30
    nak_idx, pada, nak_name = _nak_pada(lon)
    return {
        'longitude': round(lon, 4),
        'sign_index': sign_idx,
        'sign': SIGNS[sign_idx],
        'degree_in_sign': round(deg_in_sign, 4),
        'nakshatra_index': nak_idx,
        'nakshatra': nak_name,
        'pada': pada,
        'speed': round(speed, 4),
        'is_retrograde': speed < 0,
        'sign_lord': SIGN_LORDS[sign_idx],
    }


def get_positions(date_str: str, time_str: str, tz_str: str,
                  latitude: float, longitude: float) -> dict[str, dict]:
    """
    Return sidereal positions for all 9 grahas + Lagna.
    Keys: SUN MOON MERCURY VENUS MARS JUPITER SATURN RAHU KETU LAGNA
    """
    _init_swe()
    jd = _to_jd(date_str, time_str, tz_str)

    positions: dict[str, dict] = {}

    for key, swe_id in SWE_PLANET_IDS.items():
        lon, speed = _calc_planet(jd, swe_id)
        positions[key] = _planet_dict(lon, speed)

    # Ketu = Rahu + 180°
    rahu_lon = positions['RAHU']['longitude']
    ketu_lon = (rahu_lon + 180.0) % 360
    positions['KETU'] = _planet_dict(ketu_lon, -positions['RAHU']['speed'])
    positions['KETU']['is_retrograde'] = True

    # Sidereal Ascendant
    ayanamsha = swe.get_ayanamsa_ut(jd)
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')   # Placidus, tropical
    asc_sid = (ascmc[0] - ayanamsha) % 360
    positions['LAGNA'] = _planet_dict(asc_sid, 0.0)
    positions['LAGNA']['is_retrograde'] = False

    return positions
