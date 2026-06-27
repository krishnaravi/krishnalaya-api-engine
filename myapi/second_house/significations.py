"""
2nd House karakatwa (signification) analysis engine.

Covers:
  1. Wealth/Income (Varuvai & Valarchi)
  2. Speech-based Profession (Vaakinaal Thozhil)
  3. Childbirth/Family Expansion (Kuzhandhai Peru)
  4. Maraka (Maranam) risk
"""
from __future__ import annotations
from .constants import SIGNS, SIGN_LORDS, PLANET_KEY_MAP


def _pkey(name: str) -> str:
    return PLANET_KEY_MAP.get(name, name.upper())


def _planet_house(name: str, positions: dict, lagna_sign: int) -> int:
    sign = positions.get(_pkey(name), {}).get('sign_index', 0)
    return (sign - lagna_sign) % 12 + 1


def _planet_sign(name: str, positions: dict) -> int:
    return positions.get(_pkey(name), {}).get('sign_index', 0)


def _score_label(score: int) -> str:
    if score >= 70:  return 'Strong'
    if score >= 45:  return 'Moderate'
    return 'Weak'


# ── 1. Wealth / Income ────────────────────────────────────────────────────


def analyze_wealth(positions: dict, lagna_sign: int,
                   ashtakavarga: dict, d2: dict) -> dict:
    second_lord = SIGN_LORDS[(lagna_sign + 1) % 12]
    score = 50
    indicators: list[str] = []

    # SAV contribution
    sav = ashtakavarga['sav']['bindus']
    sav_str = ashtakavarga['sav']['strength']
    if sav_str == 'Strong':
        score += 15
        indicators.append(f'SAV {sav} bindus in 2nd house — excellent wealth capacity')
    elif sav_str == 'Moderate':
        score += 5
        indicators.append(f'SAV {sav} bindus — steady income growth expected')
    else:
        score -= 10
        indicators.append(f'SAV {sav} bindus — wealth accumulation requires effort')

    # 2nd lord BAV
    lord_bav = ashtakavarga['bav_second_lord']['bindus_in_second_house']
    lord_str  = ashtakavarga['bav_second_lord']['strength']
    if lord_str == 'Strong':
        score += 15
        indicators.append(f'2nd lord {second_lord} BAV {lord_bav} — lord actively promotes wealth')
    elif lord_str == 'Moderate':
        score += 5
        indicators.append(f'2nd lord {second_lord} BAV {lord_bav} — consistent income')
    else:
        score -= 5
        indicators.append(f'2nd lord {second_lord} BAV {lord_bav} — income may fluctuate')

    # Jupiter BAV (Dhana karaka)
    jup_bav = ashtakavarga['bav_jupiter']['bindus_in_second_house']
    jup_str  = ashtakavarga['bav_jupiter']['strength']
    if jup_str == 'Strong':
        score += 15
        indicators.append(f'Jupiter BAV {jup_bav} in 2nd sign — strong Dhana karaka blessing')
    elif jup_str == 'Moderate':
        score += 5
        indicators.append(f'Jupiter BAV {jup_bav} — adequate financial support')
    else:
        score -= 5
        indicators.append(f'Jupiter BAV {jup_bav} — karaka weak; remedies advised')

    # D-2 Hora analysis
    d2_lord_house  = d2.get('second_lord_house', 0)
    d2_lord_dignity = d2.get('second_lord_dignity', 'Neutral')
    if d2_lord_dignity == 'Exalted':
        score += 10
        indicators.append('2nd lord exalted in D-2 Hora — exceptional wealth accumulation')
    elif d2_lord_dignity == 'Own Sign':
        score += 7
        indicators.append('2nd lord in own sign in D-2 Hora — strong wealth foundation')
    elif d2_lord_dignity == 'Debilitated':
        score -= 10
        indicators.append('2nd lord debilitated in D-2 Hora — hidden obstacles to wealth')

    if d2_lord_house in (1, 2, 5, 9, 11):
        score += 5
        indicators.append(f'2nd lord in {d2_lord_house}th house of D-2 — positive Hora placement')
    elif d2_lord_house in (6, 8, 12):
        score -= 5
        indicators.append(f'2nd lord in {d2_lord_house}th house of D-2 — wealth faces obstruction')

    # Jupiter house in D-1
    jup_house = _planet_house('Jupiter', positions, lagna_sign)
    if jup_house in (1, 2, 5, 9, 11):
        score += 5
        indicators.append(f'Jupiter in {jup_house}th house — Dhana yoga potential')

    score = max(0, min(100, score))
    return {
        'score': score,
        'strength': _score_label(score),
        'sav_bindus': sav,
        'second_lord_bav': lord_bav,
        'jupiter_bav_in_2nd': jup_bav,
        'd2_lord_dignity': d2_lord_dignity,
        'd2_lord_house': d2_lord_house,
        'indicators': indicators,
        'prediction': (
            f'Strong financial growth likely. {second_lord} as 2nd lord with SAV {sav} '
            f'and Jupiter BAV {jup_bav} support significant wealth accumulation.'
            if score >= 70 else
            f'Moderate financial potential. Steady income with occasional fluctuations. '
            f'Strengthen {second_lord} through remedies for better results.'
            if score >= 45 else
            f'Wealth accumulation requires sustained effort. Remedies for {second_lord} '
            f'and Jupiter recommended.'
        ),
    }


# ── 2. Speech-based Profession ────────────────────────────────────────────


def analyze_speech_profession(positions: dict, lagna_sign: int) -> dict:
    second_house_sign = (lagna_sign + 1) % 12
    second_lord = SIGN_LORDS[second_house_sign]
    tenth_house_sign  = (lagna_sign + 9) % 12
    tenth_lord  = SIGN_LORDS[tenth_house_sign]

    merc_sign  = _planet_sign('Mercury', positions)
    merc_house = (merc_sign - lagna_sign) % 12 + 1
    is_merc_retro = positions.get('MERCURY', {}).get('is_retrograde', False)

    second_lord_house = _planet_house(second_lord, positions, lagna_sign)
    tenth_lord_house  = _planet_house(tenth_lord,  positions, lagna_sign)

    # Mercury 7th-aspect sign
    merc_7th_sign = (merc_sign + 6) % 12

    score = 40
    indicators: list[str] = []

    if merc_house == 2:
        score += 20
        indicators.append('Mercury in 2nd house — natural communicator; wealth through speech/writing')
    if merc_7th_sign == second_house_sign:
        score += 10
        indicators.append('Mercury aspects 2nd house — communication enhances income')
    if second_lord == 'Mercury':
        score += 15
        indicators.append('Mercury is the 2nd lord — wealth inherently tied to communication skills')
    if second_lord_house == 10:
        score += 20
        indicators.append(f'2nd lord {second_lord} in 10th — speech/communication-based career')
    if tenth_lord_house == 2:
        score += 20
        indicators.append(f'10th lord {tenth_lord} in 2nd — profession directly governs wealth through speech')
    if merc_house == 10:
        score += 15
        indicators.append('Mercury in 10th — career in communication, media, or counseling')

    # Conjunction of 2nd lord & Mercury
    second_lord_sign = _planet_sign(second_lord, positions)
    if second_lord_sign == merc_sign and second_lord != 'Mercury':
        score += 10
        indicators.append(f'2nd lord {second_lord} conjunct Mercury — powerful speech-wealth yoga')

    if is_merc_retro:
        score -= 5
        indicators.append('Mercury retrograde — communication gifts may express unconventionally')

    # Mercury aspects 10th house from its position
    merc_10th_aspect = (merc_sign + 8) % 12  # 9th from Merc = trine
    if merc_10th_aspect == tenth_house_sign:
        score += 5
        indicators.append('Mercury trines 10th house — supports speech-linked career')

    score = max(0, min(100, score))
    return {
        'score': score,
        'strength': _score_label(score),
        'mercury_house': merc_house,
        'mercury_sign': SIGNS[merc_sign],
        'mercury_retrograde': is_merc_retro,
        'second_lord_house': second_lord_house,
        'tenth_lord_house': tenth_lord_house,
        'mercury_in_2nd': merc_house == 2,
        'second_lord_in_10th': second_lord_house == 10,
        'tenth_lord_in_2nd': tenth_lord_house == 2,
        'mercury_is_second_lord': second_lord == 'Mercury',
        'indicators': indicators,
        'prediction': (
            f'Strong aptitude for speech-based profession. Mercury in {merc_house}th '
            'house supports careers in teaching, law, media, counseling, or sales.'
            if score >= 70 else
            'Moderate speech-career potential. Communication skills support income '
            'but may not be the sole driver.'
            if score >= 45 else
            'Limited speech-career indicators. Developing Mercury through education '
            'and practice will activate this potential.'
        ),
    }


# ── 3. Childbirth / Family Expansion ────────────────────────────────────


def analyze_childbirth_family(positions: dict, lagna_sign: int) -> dict:
    second_house_sign = (lagna_sign + 1) % 12
    second_lord = SIGN_LORDS[second_house_sign]
    fifth_house_sign  = (lagna_sign + 4) % 12
    fifth_lord  = SIGN_LORDS[fifth_house_sign]
    tenth_house_sign  = (lagna_sign + 9) % 12

    # 2nd house is the 5th from the 10th (family expansion through social status)
    fifth_from_10th = (tenth_house_sign + 4) % 12
    is_2nd_fifth_from_10th = fifth_from_10th == second_house_sign

    jup_sign  = _planet_sign('Jupiter', positions)
    jup_house = (jup_sign - lagna_sign) % 12 + 1
    # Jupiter's special aspects: 5th, 7th, 9th
    jup_aspect_signs = {(jup_sign + 4) % 12, (jup_sign + 6) % 12, (jup_sign + 8) % 12}
    jup_aspects_2nd = second_house_sign in jup_aspect_signs

    fifth_lord_house  = _planet_house(fifth_lord,  positions, lagna_sign)
    second_lord_house = _planet_house(second_lord, positions, lagna_sign)
    moon_house        = _planet_house('Moon',       positions, lagna_sign)

    planets_in_5th = [
        p for p, d in positions.items()
        if p != 'LAGNA' and (d['sign_index'] - lagna_sign) % 12 + 1 == 5
    ]

    score = 40
    indicators: list[str] = []

    if jup_house == 2:
        score += 20
        indicators.append('Jupiter in 2nd house — strong blessings for family expansion')
    elif jup_aspects_2nd:
        score += 15
        indicators.append('Jupiter aspects 2nd house — favorable timing for childbirth')

    if jup_house == 5:
        score += 15
        indicators.append('Jupiter in 5th house (Putra Bhava) — prime fertility indicator')

    if fifth_lord_house == 2:
        score += 20
        indicators.append(f'5th lord {fifth_lord} in 2nd — children bring family wealth/growth')

    if second_lord_house == 5:
        score += 15
        indicators.append(f'2nd lord {second_lord} in 5th — strong 2nd-5th yoga for progeny')

    if moon_house == 2:
        score += 10
        indicators.append('Moon in 2nd — maternal/emotional focus; family-centred wealth')

    if is_2nd_fifth_from_10th:
        score += 8
        indicators.append('2nd house is 5th from 10th — family expansion linked to career success')

    if planets_in_5th:
        score += 5
        indicators.append(f'Planets {planets_in_5th} activate 5th house (Putra Bhava)')

    score = max(0, min(100, score))
    return {
        'score': score,
        'strength': _score_label(score),
        'jupiter_house': jup_house,
        'jupiter_aspects_2nd': jup_aspects_2nd,
        '5th_lord': fifth_lord,
        '5th_lord_house': fifth_lord_house,
        '2nd_lord_in_5th': second_lord_house == 5,
        '5th_from_10th_matches_2nd': is_2nd_fifth_from_10th,
        'planets_in_5th': planets_in_5th,
        'indicators': indicators,
        'prediction': (
            "Strong indicators for family expansion. Jupiter's involvement suggests "
            'blessings in childbirth and family matters.'
            if score >= 70 else
            'Moderate family expansion potential. Timing depends on current dasha-bhukti.'
            if score >= 45 else
            'Family expansion requires patience. Strengthen Jupiter through remedies '
            'and avoid major decisions during adverse dasha periods.'
        ),
    }


# ── 4. Maraka Analysis ────────────────────────────────────────────────────


def analyze_maraka(positions: dict, lagna_sign: int, dasha_bhukti: dict) -> dict:
    second_house_sign  = (lagna_sign + 1) % 12
    seventh_house_sign = (lagna_sign + 6) % 12
    second_lord  = SIGN_LORDS[second_house_sign]
    seventh_lord = SIGN_LORDS[seventh_house_sign]
    maraka_lords = list({second_lord, seventh_lord})

    maha_lord   = dasha_bhukti['mahadasha']['lord']
    bhukti_lord = dasha_bhukti['bhukti']['lord']
    maha_maraka   = maha_lord   in maraka_lords
    bhukti_maraka = bhukti_lord in maraka_lords

    indicators: list[str] = []
    risk = 0

    if maha_maraka and bhukti_maraka:
        risk = 80
        indicators.append(
            f'HIGH ALERT: both {maha_lord} (Maha) and {bhukti_lord} (Bhukti) '
            'are Maraka lords — heightened risk period')
    elif maha_maraka:
        risk = 50
        indicators.append(f'Mahadasha lord {maha_lord} is a Maraka (2nd/7th lord)')
    elif bhukti_maraka:
        risk = 40
        indicators.append(f'Bhukti lord {bhukti_lord} is a Maraka — monitor health in this sub-period')
    else:
        risk = 10
        indicators.append('Current period lords are not Maraka lords — no acute concern')

    # Saturn in 2nd or 7th amplifies Maraka
    saturn_house = _planet_house('Saturn', positions, lagna_sign)
    if saturn_house in (2, 7):
        risk += 10
        indicators.append(f'Saturn in {saturn_house}th house amplifies Maraka potential')

    # Malefics in 2nd
    malefic_keys = ('SUN', 'MARS', 'SATURN', 'RAHU', 'KETU')
    malefics_in_2nd = [
        k for k in malefic_keys
        if (positions.get(k, {}).get('sign_index', -1) - lagna_sign) % 12 + 1 == 2
    ]
    if malefics_in_2nd:
        risk += 5
        indicators.append(f'Malefics {malefics_in_2nd} in 2nd house add Maraka pressure')

    risk = min(100, risk)
    risk_level = 'High' if risk >= 60 else 'Moderate' if risk >= 30 else 'Low'

    return {
        'second_lord': second_lord,
        'seventh_lord': seventh_lord,
        'maraka_lords': maraka_lords,
        'current_mahadasha_is_maraka': maha_maraka,
        'current_bhukti_is_maraka': bhukti_maraka,
        'saturn_house': saturn_house,
        'malefics_in_2nd': malefics_in_2nd,
        'risk_score': risk,
        'risk_level': risk_level,
        'indicators': indicators,
        'analysis': (
            f'Critical Maraka period. {maha_lord}/{bhukti_lord} are both Maraka lords. '
            'Health vigilance essential; consult medical professionals for any persistent symptoms.'
            if risk_level == 'High' else
            f'Moderate Maraka influence. One period lord ({maha_lord}/{bhukti_lord}) is a '
            'Maraka. Monitor health indicators but no acute crisis unless malefic transits activate.'
            if risk_level == 'Moderate' else
            f'Low Maraka risk. Natural Maraka lords ({", ".join(maraka_lords)}) are not '
            'active in current Dasha-Bhukti. Health outlook is generally stable.'
        ),
    }
