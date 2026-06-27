"""
3rd House (Sahaja/Vikrama Bhava) signification analysis engine.

Karakatwas:
  1. Siblings / Co-borns (Sahodara)
  2. Courage & Initiative (Parakrama / Vikrama)
  3. Communication, Writing & Media (Sanchar / Lekhana)
  4. Short Journeys (Laghu Yatra)
  5. Skills & Performing Arts (Kala / Shilpa)

Karakas: Mars (primary — courage & siblings), Mercury (communication)
"""
from __future__ import annotations
from core.constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP, SIGN_MODALITY


def _pkey(name: str) -> str:
    return PLANET_KEY_MAP.get(name, name.upper())


def _planet_house(name: str, positions: dict, lagna_sign: int) -> int:
    sign = positions.get(_pkey(name), {}).get('sign_index', 0)
    return (sign - lagna_sign) % 12 + 1


def _planet_sign(name: str, positions: dict) -> int:
    return positions.get(_pkey(name), {}).get('sign_index', 0)


def _score_label(score: int) -> str:
    if score >= 70: return 'Strong'
    if score >= 45: return 'Moderate'
    return 'Weak'


def _aspects_planet_on_sign(planet_key: str, positions: dict, target_sign: int) -> bool:
    """Check if a specific planet aspects the target sign (Vedic aspects)."""
    SPECIAL = {
        'MARS': [4, 8], 'JUPITER': [5, 9],
        'SATURN': [3, 10], 'RAHU': [5, 9], 'KETU': [5, 9],
    }
    ps = positions.get(planet_key, {}).get('sign_index', -1)
    if ps < 0 or ps == target_sign:
        return False
    offsets = [7] + SPECIAL.get(planet_key, [])
    return any((ps + off - 1) % 12 == target_sign for off in offsets)


# ── 1. Siblings / Co-borns ────────────────────────────────────────────────


def analyze_siblings(positions: dict, lagna_sign: int,
                     d3_analysis: dict, ashtakavarga: dict) -> dict:
    """
    Factors: Mars (karaka), 3rd lord strength, D-3 Drekkana,
    benefics/malefics in 3rd, BAV of 3rd lord and Mars.
    """
    third_house_sign = (lagna_sign + 2) % 12
    third_lord = SIGN_LORDS[third_house_sign]

    mars_house  = _planet_house('Mars',    positions, lagna_sign)
    mars_sign   = _planet_sign('Mars',     positions)
    mars_in_3rd = mars_house == 3

    third_lord_house    = _planet_house(third_lord, positions, lagna_sign)
    third_lord_sign     = _planet_sign(third_lord, positions)
    mars_aspects_3rd    = _aspects_planet_on_sign('MARS', positions, third_house_sign)

    # Planets in 3rd house
    planets_in_3rd = [
        p for p, d in positions.items()
        if p != 'LAGNA' and (d['sign_index'] - lagna_sign) % 12 + 1 == 3
    ]

    BENEFICS  = {'JUPITER', 'VENUS', 'MERCURY', 'MOON'}
    MALEFICS  = {'MARS', 'SATURN', 'SUN', 'RAHU', 'KETU'}
    benefics_in_3rd = [p for p in planets_in_3rd if p in BENEFICS]
    malefics_in_3rd = [p for p in planets_in_3rd if p in MALEFICS]

    score = 50
    indicators: list[str] = []

    # Mars karaka analysis
    if mars_in_3rd:
        score += 15
        indicators.append('Mars in 3rd house (own karaka position) — strong courage, competitive siblings')
    elif mars_aspects_3rd:
        score += 10
        indicators.append('Mars aspects 3rd house — protective influence on siblings and courage')
    elif mars_house in (1, 5, 9):
        score += 8
        indicators.append(f'Mars in {mars_house}th (trine) — benign influence on sibling significations')

    # 3rd lord placement
    if third_lord_house in (1, 2, 4, 5, 7, 9, 10, 11):
        score += 12
        indicators.append(f'3rd lord {third_lord} in {third_lord_house}th — supportive placement for siblings')
    elif third_lord_house in (6, 8, 12):
        score -= 12
        indicators.append(f'3rd lord {third_lord} in {third_lord_house}th (dusthana) — challenges or separation from siblings')

    if positions.get(_pkey(third_lord), {}).get('is_retrograde'):
        score -= 5
        indicators.append(f'3rd lord {third_lord} retrograde — sibling relationships may be complex or delayed')

    # D-3 Drekkana analysis
    d3_lord_house    = d3_analysis.get('lord_house', 0)
    d3_lord_dignity  = d3_analysis.get('lord_dignity', 'Neutral')
    if d3_lord_dignity == 'Exalted':
        score += 12
        indicators.append('3rd lord exalted in D-3 Drekkana — excellent sibling prosperity')
    elif d3_lord_dignity == 'Own Sign':
        score += 8
        indicators.append('3rd lord in own sign in D-3 — siblings thrive')
    elif d3_lord_dignity == 'Debilitated':
        score -= 10
        indicators.append('3rd lord debilitated in D-3 — sibling hardships or conflicts')

    if d3_lord_house in (1, 2, 4, 5, 9, 10, 11):
        score += 5
        indicators.append(f'3rd lord in {d3_lord_house}th of D-3 — favourable sibling karma')
    elif d3_lord_house in (6, 8, 12):
        score -= 5
        indicators.append(f'3rd lord in {d3_lord_house}th of D-3 — sibling adversity indicated')

    # Benefics vs malefics in 3rd
    if benefics_in_3rd:
        score += len(benefics_in_3rd) * 5
        indicators.append(f'Benefics {benefics_in_3rd} in 3rd — harmonious sibling bonds')
    if malefics_in_3rd and 'MARS' not in malefics_in_3rd:
        score -= len(malefics_in_3rd) * 3
        indicators.append(f'Malefics {malefics_in_3rd} in 3rd — possible friction with siblings')

    # BAV of 3rd lord in 3rd sign
    lord_bav  = ashtakavarga['bav_third_lord']['bindus_in_third_house']
    mars_bav  = ashtakavarga['bav_mars']['bindus_in_third_house']
    if lord_bav >= 5:
        score += 8
        indicators.append(f'3rd lord BAV {lord_bav} (strong) — lord well-supported in 3rd house sign')
    elif lord_bav < 4:
        score -= 5
        indicators.append(f'3rd lord BAV {lord_bav} (weak) — reduced sibling support indicated')

    score = max(0, min(100, score))
    return {
        'score': score,
        'strength': _score_label(score),
        'mars_house': mars_house,
        'mars_in_3rd': mars_in_3rd,
        'mars_aspects_3rd': mars_aspects_3rd,
        'third_lord': third_lord,
        'third_lord_house': third_lord_house,
        'd3_lord_dignity': d3_lord_dignity,
        'd3_lord_house': d3_lord_house,
        'benefics_in_3rd': benefics_in_3rd,
        'malefics_in_3rd': malefics_in_3rd,
        'third_lord_bav': lord_bav,
        'mars_bav_in_3rd': mars_bav,
        'indicators': indicators,
        'prediction': (
            'Strong sibling bonds indicated. Mars and 3rd lord well-placed suggest '
            'supportive, prosperous co-borns and cooperative relationships.'
            if score >= 70 else
            'Moderate sibling dynamics. Relationships are generally supportive but '
            'may need conscious effort to maintain harmony.'
            if score >= 45 else
            'Sibling relationships may face challenges. Strengthen Mars through '
            'remedies. D-3 Drekkana suggests karmic complexities with co-borns.'
        ),
    }


# ── 2. Courage & Initiative (Parakrama) ──────────────────────────────────


def analyze_courage(positions: dict, lagna_sign: int, ashtakavarga: dict) -> dict:
    third_house_sign = (lagna_sign + 2) % 12
    third_lord = SIGN_LORDS[third_house_sign]

    mars_house      = _planet_house('Mars', positions, lagna_sign)
    sun_house       = _planet_house('Sun',  positions, lagna_sign)
    third_lord_house = _planet_house(third_lord, positions, lagna_sign)
    mars_aspects_3rd = _aspects_planet_on_sign('MARS', positions, third_house_sign)
    sun_aspects_3rd  = _aspects_planet_on_sign('SUN',  positions, third_house_sign)

    sav      = ashtakavarga['sav']['bindus']
    mars_bav = ashtakavarga['bav_mars']['bindus_in_third_house']

    score = 45
    indicators: list[str] = []

    # Mars in 3rd: raw courage, warrior spirit
    if mars_house == 3:
        score += 20
        indicators.append('Mars in 3rd house — exceptional courage and fighting spirit (Vikrama Yoga)')
    elif mars_aspects_3rd:
        score += 12
        indicators.append('Mars aspects 3rd house — bold, assertive initiative')

    # Mars in kendra/trikona
    if mars_house in (1, 4, 7, 10):
        score += 8
        indicators.append(f'Mars in {mars_house}th (kendra) — steady, reliable courage')
    elif mars_house in (5, 9):
        score += 8
        indicators.append(f'Mars in {mars_house}th (trikona) — dharmic, purposeful courage')

    # Sun in 3rd (royal courage, leadership initiative)
    if sun_house == 3:
        score += 12
        indicators.append('Sun in 3rd — strong willpower, leadership through courage')
    elif sun_aspects_3rd:
        score += 6
        indicators.append('Sun aspects 3rd — solar vitality reinforces initiative')

    # 3rd lord placement
    if third_lord_house in (1, 3, 6, 10, 11):
        score += 10
        indicators.append(f'3rd lord {third_lord} in {third_lord_house}th — courageous, action-oriented')
    elif third_lord_house in (8, 12):
        score -= 8
        indicators.append(f'3rd lord {third_lord} in {third_lord_house}th — courage may be inwardly directed or suppressed')

    # 3rd lord as Mars itself
    if third_lord == 'Mars':
        score += 10
        indicators.append('Mars is the 3rd lord — natural Parakrama Yoga; inherent fearlessness')

    # Ashtakavarga
    if mars_bav >= 5:
        score += 8
        indicators.append(f'Mars BAV {mars_bav} in 3rd sign — Mars well-supported; bold actions succeed')
    elif mars_bav < 4:
        score -= 5
        indicators.append(f'Mars BAV {mars_bav} — courage indicators need strengthening')

    if sav >= 29:
        score += 5
        indicators.append(f'Strong SAV ({sav}) in 3rd — overall house well-energised for initiatives')

    score = max(0, min(100, score))
    return {
        'score': score,
        'strength': _score_label(score),
        'mars_house': mars_house,
        'sun_house': sun_house,
        'third_lord_house': third_lord_house,
        'mars_in_3rd': mars_house == 3,
        'mars_aspects_3rd': mars_aspects_3rd,
        'mars_bav_in_3rd': mars_bav,
        'sav_bindus': sav,
        'indicators': indicators,
        'prediction': (
            'Exceptional courage and initiative. Mars strongly placed with high BAV '
            'supports bold ventures, entrepreneurship, and physical feats.'
            if score >= 70 else
            'Moderate courage and initiative. Capable of taking calculated risks. '
            'Strengthen Mars to activate full Parakrama potential.'
            if score >= 45 else
            'Courage indicators are limited. Tendency to hesitate before major decisions. '
            'Mars remedies and physical activity will help activate 3rd house energy.'
        ),
    }


# ── 3. Communication, Writing & Media ────────────────────────────────────


def analyze_communication(positions: dict, lagna_sign: int,
                           d3_analysis: dict) -> dict:
    third_house_sign = (lagna_sign + 2) % 12
    third_lord  = SIGN_LORDS[third_house_sign]
    tenth_lord  = SIGN_LORDS[(lagna_sign + 9) % 12]

    merc_sign  = _planet_sign('Mercury', positions)
    merc_house = (merc_sign - lagna_sign) % 12 + 1
    merc_retro = positions.get('MERCURY', {}).get('is_retrograde', False)

    third_lord_house = _planet_house(third_lord,  positions, lagna_sign)
    tenth_lord_house = _planet_house(tenth_lord,  positions, lagna_sign)

    merc_aspects_3rd = _aspects_planet_on_sign('MERCURY', positions, third_house_sign)
    third_lord_sign  = _planet_sign(third_lord, positions)

    score = 40
    indicators: list[str] = []

    # Mercury in 3rd — most powerful placement
    if merc_house == 3:
        score += 25
        indicators.append('Mercury in 3rd house — exceptional writer, communicator, or media personality')

    # Mercury aspects 3rd
    if merc_aspects_3rd:
        score += 12
        indicators.append('Mercury aspects 3rd — communication talent influences house strongly')

    # Mercury is the 3rd lord
    if third_lord == 'Mercury':
        score += 15
        indicators.append('Mercury is the 3rd lord — natural gift for communication and writing')

    # 3rd lord in 10th (career in communication)
    if third_lord_house == 10:
        score += 18
        indicators.append(f'3rd lord {third_lord} in 10th — communication-based career (journalism, media, writing)')

    # 10th lord in 3rd (profession brought into communication)
    if tenth_lord_house == 3:
        score += 15
        indicators.append(f'10th lord {tenth_lord} in 3rd — profession rooted in communication and effort')

    # Mercury in good houses for career
    if merc_house in (1, 2, 10, 11):
        score += 10
        indicators.append(f'Mercury in {merc_house}th — communication skills directly support wealth/career')

    # Conjunction Mercury + 3rd lord
    if third_lord_sign == merc_sign and third_lord != 'Mercury':
        score += 10
        indicators.append(f'3rd lord {third_lord} conjunct Mercury — powerful communication yoga')

    # D-3 Mercury position
    d3_positions = d3_analysis.get('all_positions', {})
    merc_d3_sign = d3_positions.get('MERCURY', {}).get('sign_index', -1)
    merc_d3_house = (merc_d3_sign - d3_analysis.get('lagna_sign_index', 0)) % 12 + 1 if merc_d3_sign >= 0 else 0
    if merc_d3_house in (1, 3, 5, 9, 10, 11):
        score += 8
        indicators.append(f'Mercury in {merc_d3_house}th of D-3 Drekkana — communication karma is strong')

    if merc_retro:
        score -= 5
        indicators.append('Mercury retrograde — communication style may be introspective or unconventional')

    score = max(0, min(100, score))
    return {
        'score': score,
        'strength': _score_label(score),
        'mercury_house': merc_house,
        'mercury_sign': SIGNS[merc_sign],
        'mercury_retrograde': merc_retro,
        'third_lord_house': third_lord_house,
        'mercury_is_third_lord': third_lord == 'Mercury',
        'third_lord_in_10th': third_lord_house == 10,
        'tenth_lord_in_3rd': tenth_lord_house == 3,
        'mercury_d3_house': merc_d3_house,
        'indicators': indicators,
        'prediction': (
            'Outstanding communication talent. Strong Mercury-3rd house connection '
            'supports careers in journalism, writing, media, teaching, or content creation.'
            if score >= 70 else
            'Good communication skills. Mercury supports articulate expression. '
            'Developing writing and public speaking will enhance results.'
            if score >= 45 else
            'Communication potential is present but underdeveloped. Mercury remedies '
            'and consistent writing/speaking practice will activate 3rd house gifts.'
        ),
    }


# ── 4. Short Journeys (Laghu Yatra) ──────────────────────────────────────


def analyze_short_journeys(positions: dict, lagna_sign: int) -> dict:
    third_house_sign = (lagna_sign + 2) % 12
    third_lord = SIGN_LORDS[third_house_sign]

    third_lord_house    = _planet_house(third_lord, positions, lagna_sign)
    third_lord_sign_idx = _planet_sign(third_lord, positions)
    moon_house          = _planet_house('Moon', positions, lagna_sign)
    moon_sign           = _planet_sign('Moon', positions)

    is_3rd_movable    = SIGN_MODALITY[third_house_sign]  == 'Movable'
    is_lord_movable   = SIGN_MODALITY[third_lord_sign_idx] == 'Movable'

    score = 40
    indicators: list[str] = []

    # Movable sign on 3rd cusp
    if is_3rd_movable:
        score += 15
        indicators.append(f'Movable sign {SIGNS[third_house_sign]} on 3rd cusp — frequent short travel')

    # 3rd lord in movable sign
    if is_lord_movable:
        score += 12
        indicators.append(f'3rd lord {third_lord} in movable sign — active traveller by nature')

    # 3rd lord in upachaya (3, 6, 10, 11)
    if third_lord_house in (3, 6, 10, 11):
        score += 10
        indicators.append(f'3rd lord {third_lord} in {third_lord_house}th (upachaya) — travel brings gains')

    # Moon in 3rd (wandering mind, frequent movement)
    if moon_house == 3:
        score += 15
        indicators.append('Moon in 3rd — restless nature, frequent short journeys, close neighbourhood connections')

    # Moon in movable sign
    if SIGN_MODALITY[moon_sign] == 'Movable':
        score += 8
        indicators.append('Moon in movable sign — emotionally driven movement; travel for comfort')

    # 3rd lord in 12th (journeys end in distant or foreign places)
    if third_lord_house == 12:
        score += 5
        indicators.append('3rd lord in 12th — short journeys may extend to distant or foreign locations')

    # Saturn in 3rd — restricts easy travel but gives endurance for long hauls
    saturn_house = _planet_house('Saturn', positions, lagna_sign)
    if saturn_house == 3:
        score -= 5
        indicators.append('Saturn in 3rd — travel may be delayed, restricted, or related to duty/work')

    # Rahu in 3rd — unconventional, long-distance trips disguised as short
    rahu_house = _planet_house('Rahu', positions, lagna_sign)
    if rahu_house == 3:
        score += 8
        indicators.append('Rahu in 3rd — unusual, foreign or technology-enabled journeys')

    score = max(0, min(100, score))
    return {
        'score': score,
        'strength': _score_label(score),
        'third_house_modality': SIGN_MODALITY[third_house_sign],
        'third_lord': third_lord,
        'third_lord_house': third_lord_house,
        'third_lord_sign_modality': SIGN_MODALITY[third_lord_sign_idx],
        'moon_house': moon_house,
        'moon_sign_modality': SIGN_MODALITY[moon_sign],
        'indicators': indicators,
        'prediction': (
            'Highly active traveller. Movable sign influences and strong 3rd lord '
            'indicate frequent, fruitful short journeys and local networking.'
            if score >= 70 else
            'Moderate travel activity. Journeys are purposeful but not extremely frequent. '
            'Travel during favourable Dasha periods will be productive.'
            if score >= 45 else
            'Short journeys may be infrequent or face obstacles. Fixed sign influences '
            'suggest a preference for stability. Travel when 3rd lord is activated by Dasha.'
        ),
    }


# ── 5. Skills & Performing Arts (Kala / Shilpa) ──────────────────────────


def analyze_skills_arts(positions: dict, lagna_sign: int,
                         d24_analysis: dict) -> dict:
    third_house_sign = (lagna_sign + 2) % 12
    third_lord = SIGN_LORDS[third_house_sign]

    venus_house      = _planet_house('Venus',   positions, lagna_sign)
    mercury_house    = _planet_house('Mercury', positions, lagna_sign)
    third_lord_house = _planet_house(third_lord, positions, lagna_sign)

    venus_in_3rd   = venus_house == 3
    venus_sign     = _planet_sign('Venus', positions)
    venus_aspects_3rd = _aspects_planet_on_sign('VENUS', positions, third_house_sign)

    score = 40
    indicators: list[str] = []

    # Venus in 3rd — music, arts, creative communication
    if venus_in_3rd:
        score += 22
        indicators.append('Venus in 3rd — exceptional artistic talent; music, dance, visual arts, or crafts')
    elif venus_aspects_3rd:
        score += 12
        indicators.append('Venus aspects 3rd house — artistic sensibility infused into communication')

    # Venus in good houses
    if venus_house in (1, 2, 4, 5, 7, 9, 10, 11):
        score += 8
        indicators.append(f'Venus in {venus_house}th — artistic gifts well-supported')

    # Mercury in 3rd (writing, technical skills)
    if mercury_house == 3:
        score += 15
        indicators.append('Mercury in 3rd — technical skills, writing craft, linguistic arts')
    elif mercury_house in (1, 2, 5, 10, 11):
        score += 6
        indicators.append(f'Mercury in {mercury_house}th — sharp learning ability supports skill development')

    # 3rd lord + Venus conjunction
    third_lord_sign = _planet_sign(third_lord, positions)
    if third_lord_sign == venus_sign:
        score += 10
        indicators.append(f'3rd lord {third_lord} conjunct Venus — strong arts-courage combination')

    # Venus is 3rd lord
    if third_lord == 'Venus':
        score += 12
        indicators.append('Venus is the 3rd lord — innate artistic identity; skills are a core life theme')

    # D-24 Siddhamsha analysis (education and skill mastery)
    d24_lord_house    = d24_analysis.get('lord_house', 0)
    d24_lord_dignity  = d24_analysis.get('lord_dignity', 'Neutral')
    if d24_lord_dignity == 'Exalted':
        score += 12
        indicators.append('3rd lord exalted in D-24 Siddhamsha — mastery-level skill potential')
    elif d24_lord_dignity == 'Own Sign':
        score += 8
        indicators.append('3rd lord in own sign D-24 — natural, well-developed skills')
    elif d24_lord_dignity == 'Debilitated':
        score -= 8
        indicators.append('3rd lord debilitated in D-24 — skill development requires extra effort')

    if d24_lord_house in (1, 3, 5, 9, 10, 11):
        score += 6
        indicators.append(f'3rd lord in {d24_lord_house}th of D-24 — skills find public expression')

    # Jupiter in 3rd (teaching skills, wisdom in communication)
    jup_house = _planet_house('Jupiter', positions, lagna_sign)
    if jup_house == 3:
        score += 8
        indicators.append('Jupiter in 3rd — teaching, philosophical writing, wisdom-based skills')

    score = max(0, min(100, score))
    return {
        'score': score,
        'strength': _score_label(score),
        'venus_house': venus_house,
        'venus_in_3rd': venus_in_3rd,
        'venus_aspects_3rd': venus_aspects_3rd,
        'mercury_house': mercury_house,
        'third_lord_house': third_lord_house,
        'venus_is_third_lord': third_lord == 'Venus',
        'd24_lord_dignity': d24_lord_dignity,
        'd24_lord_house': d24_lord_house,
        'indicators': indicators,
        'prediction': (
            'Exceptional artistic or technical talent. Venus-Mercury-3rd house connection '
            'supports careers in music, dance, writing, design, or performing arts.'
            if score >= 70 else
            'Good skill potential. Talents are present and can be developed with '
            'consistent practice. Favourable D-24 indicates mastery is achievable.'
            if score >= 45 else
            'Skill development requires dedicated effort. Strengthen Venus and Mercury '
            'through remedies. D-24 Siddhamsha guidance recommended for learning path.'
        ),
    }
