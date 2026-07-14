SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

SIGN_LORDS = {
    0: 'Mars',    1: 'Venus',   2: 'Mercury', 3: 'Moon',
    4: 'Sun',     5: 'Mercury', 6: 'Venus',   7: 'Mars',
    8: 'Jupiter', 9: 'Saturn',  10: 'Saturn', 11: 'Jupiter'
}

SIGN_ELEMENTS = {
    0: 'Fire', 1: 'Earth', 2: 'Air',   3: 'Water',
    4: 'Fire', 5: 'Earth', 6: 'Air',   7: 'Water',
    8: 'Fire', 9: 'Earth', 10: 'Air',  11: 'Water'
}

SIGN_MODALITY = {
    0: 'Movable', 1: 'Fixed', 2: 'Dual',    3: 'Movable',
    4: 'Fixed',   5: 'Dual',  6: 'Movable', 7: 'Fixed',
    8: 'Dual',    9: 'Movable', 10: 'Fixed', 11: 'Dual'
}

NAKSHATRA_NAMES = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni',
    'Uttara Phalguni', 'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha',
    'Jyeshtha', 'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana',
    'Dhanishtha', 'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

# Nakshatra lords cycle (repeats 3×): Ketu Venus Sun Moon Mars Rahu Jupiter Saturn Mercury
NAKSHATRA_LORDS = [
    'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'
]

DASHA_ORDER = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']

DASHA_YEARS: dict[str, int] = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6,  'Moon': 10, 'Mars': 7,
    'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17
}

TOTAL_DASHA_YEARS = 120
DAYS_PER_YEAR = 365.25

PLANET_KEY_MAP = {
    'Sun': 'SUN', 'Moon': 'MOON', 'Mars': 'MARS', 'Mercury': 'MERCURY',
    'Jupiter': 'JUPITER', 'Venus': 'VENUS', 'Saturn': 'SATURN',
    'Rahu': 'RAHU', 'Ketu': 'KETU'
}

EXALTATION = {
    'Sun': 0, 'Moon': 1, 'Mars': 9, 'Mercury': 5,
    'Jupiter': 3, 'Venus': 11, 'Saturn': 6
}

DEBILITATION = {
    'Sun': 6, 'Moon': 7, 'Mars': 3, 'Mercury': 11,
    'Jupiter': 9, 'Venus': 5, 'Saturn': 0
}

OWN_SIGNS = {
    'Sun': [4],    'Moon': [3],    'Mars': [0, 7], 'Mercury': [2, 5],
    'Jupiter': [8, 11], 'Venus': [1, 6], 'Saturn': [9, 10]
}

# ── Ashtakavarga benefic bindu tables (Parashari) ──────────────────────────
# Key: target planet → reference point → list of benefic house-positions (1-indexed,
# counted from the reference point's sign).
BAV_TABLES: dict[str, dict[str, list[int]]] = {
    'Sun': {
        'Sun':     [1, 2, 4, 7, 8, 9, 10, 11],
        'Moon':    [3, 6, 10, 11],
        'Mars':    [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [5, 6, 9, 11],
        'Venus':   [6, 7, 12],
        'Saturn':  [1, 2, 4, 7, 8, 9, 10, 11],
        'Lagna':   [3, 4, 6, 10, 11, 12],
    },
    'Moon': {
        'Sun':     [3, 6, 7, 8, 10, 11],
        'Moon':    [1, 3, 6, 7, 10, 11],
        'Mars':    [2, 3, 5, 6, 9, 10, 11],
        'Mercury': [1, 3, 4, 5, 7, 8, 10, 11],
        'Jupiter': [1, 4, 7, 8, 10, 11, 12],
        'Venus':   [3, 4, 5, 7, 9, 10, 11],
        'Saturn':  [3, 5, 6, 11],
        'Lagna':   [3, 6, 10, 11],
    },
    'Mars': {
        'Sun':     [3, 5, 6, 10, 11],
        'Moon':    [3, 6, 11],
        'Mars':    [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [3, 5, 6, 11],
        'Jupiter': [6, 10, 11, 12],
        'Venus':   [6, 8, 11, 12],
        'Saturn':  [3, 5, 6, 11],               # BPHS Ch.66 — total 39
        'Lagna':   [1, 2, 4, 7, 8, 9, 10, 11],  # BPHS Ch.66
    },
    'Mercury': {
        'Sun':     [5, 6, 9, 11, 12],
        'Moon':    [2, 4, 6, 8, 10, 11],
        'Mars':    [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [1, 3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [6, 8, 11, 12],
        'Venus':   [1, 2, 3, 4, 5, 8, 9, 11],
        'Saturn':  [1, 2, 4, 7, 8, 9, 10, 11],
        'Lagna':   [1, 2, 4, 6, 8, 10, 11],
    },
    'Jupiter': {
        'Sun':     [1, 2, 3, 4, 7, 8, 9, 10, 11],
        'Moon':    [2, 5, 7, 9, 11],
        'Mars':    [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [1, 2, 4, 5, 6, 9, 10, 11],
        'Jupiter': [1, 2, 3, 4, 7, 8, 10, 11],
        'Venus':   [2, 5, 6, 9, 10, 11],
        'Saturn':  [3, 5, 6, 12],
        'Lagna':   [1, 2, 4, 5, 6, 7, 9, 10, 11],
    },
    'Venus': {
        'Sun':     [8, 11, 12],
        'Moon':    [1, 2, 3, 4, 5, 8, 9, 11, 12],
        'Mars':    [3, 4, 6, 9, 11, 12],
        'Mercury': [3, 5, 6, 9, 11],
        'Jupiter': [5, 8, 9, 10, 11],
        'Venus':   [1, 2, 3, 4, 5, 8, 9, 10, 11],
        'Saturn':  [3, 4, 5, 8, 9, 10, 11],
        'Lagna':   [1, 2, 3, 4, 5, 8, 9, 11],
    },
    'Saturn': {
        'Sun':     [1, 2, 4, 7, 8, 10, 11],
        'Moon':    [3, 6, 11],
        'Mars':    [3, 5, 6, 10, 11, 12],
        'Mercury': [6, 8, 9, 10, 11, 12],
        'Jupiter': [5, 6, 11, 12],
        'Venus':   [6, 11, 12],
        'Saturn':  [3, 5, 6, 11],
        'Lagna':   [1, 3, 4, 6, 10, 11],
    },
}

# ── Moolatrikona signs (planet → sign index) ──────────────────────────────
MOOLATRIKONA = {
    'Sun': 4, 'Moon': 1, 'Mars': 0, 'Mercury': 5,
    'Jupiter': 8, 'Venus': 6, 'Saturn': 10,
}

# ── Natural friendships (planet → set of natural friends) ─────────────────
NATURAL_FRIENDS: dict[str, list[str]] = {
    'Sun':     ['Moon', 'Mars', 'Jupiter'],
    'Moon':    ['Sun', 'Mercury'],
    'Mars':    ['Sun', 'Moon', 'Jupiter'],
    'Mercury': ['Sun', 'Venus'],
    'Jupiter': ['Sun', 'Moon', 'Mars'],
    'Venus':   ['Mercury', 'Saturn'],
    'Saturn':  ['Mercury', 'Venus'],
}

NATURAL_ENEMIES: dict[str, list[str]] = {
    'Sun':     ['Venus', 'Saturn'],
    'Moon':    [],
    'Mars':    ['Mercury'],
    'Mercury': ['Moon'],
    'Jupiter': ['Mercury', 'Venus'],
    'Venus':   ['Sun', 'Moon'],
    'Saturn':  ['Sun', 'Moon', 'Mars'],
}

# ── House metadata (1-indexed) ─────────────────────────────────────────────
HOUSE_NAMES = {
    1:  ('Tanu Bhava',    'House of Self',         'Sun'),
    2:  ('Dhana Bhava',   'House of Wealth',       'Jupiter'),
    3:  ('Sahaja Bhava',  'House of Siblings',     'Mars'),
    4:  ('Sukha Bhava',   'House of Happiness',    'Moon'),
    5:  ('Putra Bhava',   'House of Children',     'Jupiter'),
    6:  ('Ari Bhava',     'House of Enemies',      'Mars'),
    7:  ('Kalatra Bhava', 'House of Spouse',       'Venus'),
    8:  ('Randhra Bhava', 'House of Longevity',    'Saturn'),
    9:  ('Dharma Bhava',  'House of Dharma',       'Jupiter'),
    10: ('Karma Bhava',   'House of Career',       'Sun'),
    11: ('Labha Bhava',   'House of Gains',        'Jupiter'),
    12: ('Vyaya Bhava',   'House of Liberation',   'Saturn'),
}

HOUSE_TYPES: dict[int, list[str]] = {
    1:  ['Kendra', 'Trikona'],
    2:  ['Panapara', 'Maraka'],
    3:  ['Apoklima', 'Upachaya'],
    4:  ['Kendra'],
    5:  ['Panapara', 'Trikona'],
    6:  ['Apoklima', 'Upachaya', 'Dusthana'],
    7:  ['Kendra', 'Maraka'],
    8:  ['Dusthana'],
    9:  ['Apoklima', 'Trikona'],
    10: ['Kendra', 'Upachaya'],
    11: ['Panapara', 'Upachaya'],
    12: ['Apoklima', 'Dusthana'],
}
