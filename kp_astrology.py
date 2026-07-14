import sys
import json
import swisseph as swe

def calculate_kp_astrology(year, month, day, hour, minute, lat, lon):
    swe.set_ephe_path('/root/swisseph')
    dec_hour = hour + (minute / 60.0)
    jd = swe.julday(year, month, day, dec_hour)
    
    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI, 0, 0)
    ayanamsa = swe.get_ayanamsa_ut(jd)
    
    planets = {
        "Suriyan (Sun)": swe.SUN,
        "Chandran (Moon)": swe.MOON,
        "Sevvai (Mars)": swe.MARS,
        "Budhan (Mercury)": swe.MERCURY,
        "Guru (Jupiter)": swe.JUPITER,
        "Sukran (Venus)": swe.VENUS,
        "Sani (Saturn)": swe.SATURN,
        "Rahu": swe.TRUE_NODE
    }
    
    planet_data = {}
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    
    for p_name, p_id in planets.items():
        res = swe.calc_ut(jd, p_id, flags)
        longitude = res[0][0] if isinstance(res[0], (tuple, list)) else res[0]
        
        planet_data[p_name] = {
            "total_degree": round(longitude, 4),
            "rashi_id": int(longitude / 30),
            "rashi_degree": round(longitude % 30, 4)
        }
        
    rahu_long = planet_data["Rahu"]["total_degree"]
    kethu_long = (rahu_long + 180.0) % 360.0
    planet_data["Kethu"] = {
        "total_degree": round(kethu_long, 4),
        "rashi_id": int(kethu_long / 30),
        "rashi_degree": round(kethu_long % 30, 4)
    }
        
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P')
    house_data = {}
    for idx in range(12):
        house_long = cusps[idx]
        house_data[f"House_{idx + 1}"] = {
            "total_degree": round(house_long, 4),
            "rashi_id": int(house_long / 30),
            "rashi_degree": round(house_long % 30, 4)
        }
        
    output = {
        "metadata": {"julian_day": jd, "kp_ayanamsa": round(ayanamsa, 4), "lagna_degree": round(ascmc[0], 4)},
        "planets": planet_data,
        "kp_houses": house_data
    }
    return json.dumps(output, ensure_ascii=False)

if __name__ == "__main__":
    try:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        day = int(sys.argv[3])
        hour = int(sys.argv[4])
        minute = int(sys.argv[5])
        lat = float(sys.argv[6])
        lon = float(sys.argv[7])
        
        print(calculate_kp_astrology(year, month, day, hour, minute, lat, lon))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
