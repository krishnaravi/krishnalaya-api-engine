import { v4 as uuidv4 } from 'uuid';
import type {
  PanchangData,
  MuhurthaResult,
  MuhurthaWindow,
  TithiData,
  NakshatraData,
  YogaData,
  KaranaData,

  TimePeriod,
  LagnaData,
  BilingualText,
} from '../../../types/muhurtha.types';
import {
  TITHIS,
  NAKSHATRAS,
  YOGAS,
  KARANAS,
  VAARA,
  RAHU_KALAM_SLOTS,
  YAMAGANDAM_SLOTS,
  KULIGAI_SLOTS,
  MUHURTHA_CATEGORIES,
  ZODIAC_SIGNS,
  CHALDEAN_ORDER,
} from '../constants/muhurthaConstants';
import type { CategoryDefinition } from '../../../types/muhurtha.types';
import { PANCHANG_RULES } from '../rules/panchangRules';
import { DOSHA_RULES } from '../rules/doshaRules';
import { STRENGTH_RULES } from '../rules/strengthRules';
import { executeAllRules } from '../rules/baseRule';
import {
  aggregateRuleResults,
  generateVerdict,
} from '../utils/scoreCalculator';
import type { MuhurthaSearchInput } from '../validators/muhurthaValidator';

function dateToJulianDay(date: Date): number {
  const Y = date.getUTCFullYear();
  const M = date.getUTCMonth() + 1;
  const D =
    date.getUTCDate() +
    date.getUTCHours() / 24 +
    date.getUTCMinutes() / 1440 +
    date.getUTCSeconds() / 86400;
  const A = Math.floor(Y / 100);
  const B = 2 - A + Math.floor(A / 4);
  return (
    Math.floor(365.25 * (Y + 4716)) +
    Math.floor(30.6001 * (M > 2 ? M + 1 : M + 13)) +
    D +
    B -
    1524.5
  );
}

function getLahiriAyanamsa(jd: number): number {
  const T = (jd - 2451545.0) / 36525.0;
  return 23.85 + 0.013935 * (T * 36525) / 365.25;
}

function getSunTropicalLongitude(jd: number): number {
  const T = (jd - 2451545.0) / 36525.0;
  const L0 = (280.46646 + 36000.76983 * T + 0.0003032 * T * T) % 360;
  const M = ((357.52911 + 35999.05029 * T - 0.0001537 * T * T) % 360) * (Math.PI / 180);
  const C =
    (1.914602 - 0.004817 * T - 0.000014 * T * T) * Math.sin(M) +
    (0.019993 - 0.000101 * T) * Math.sin(2 * M) +
    0.000289 * Math.sin(3 * M);
  return (L0 + C + 360) % 360;
}

function getMoonTropicalLongitude(jd: number): number {
  const T = (jd - 2451545.0) / 36525.0;
  const L1 = (218.3165 + 481267.8813 * T) % 360;
  const M1 = ((134.9634 + 477198.8676 * T) % 360) * (Math.PI / 180);
  const M = ((357.5291 + 35999.0503 * T) % 360) * (Math.PI / 180);
  const D = ((297.8502 + 445267.1115 * T) % 360) * (Math.PI / 180);
  const F = ((93.272 + 483202.0175 * T) % 360) * (Math.PI / 180);

  const lon =
    L1 +
    6.2886 * Math.sin(M1) +
    1.2740 * Math.sin(2 * D - M1) +
    0.6583 * Math.sin(2 * D) +
    0.2136 * Math.sin(2 * M1) -
    0.1851 * Math.sin(M) -
    0.1143 * Math.sin(2 * F) +
    0.0588 * Math.sin(2 * D - 2 * M1) +
    0.0572 * Math.sin(2 * D - M - M1) +
    0.0533 * Math.sin(2 * D + M1);

  return (lon + 360) % 360;
}

function getSiderealLongitude(tropicalLon: number, ayanamsa: number): number {
  return (tropicalLon - ayanamsa + 360) % 360;
}

function getLagnaSign(date: Date, latitude: number, longitude: number, timezone: string): number {
  new Date(date.toLocaleString('en-US', { timeZone: timezone }));
  const lstHours =
    ((date.getUTCHours() + longitude / 15) % 24 + 24) % 24;
  const lstFraction = lstHours / 24;
  const lagnaSignFloat = (lstFraction * 12 + latitude / 30) % 12;
  return Math.floor(lagnaSignFloat) + 1;
}

function getHora(date: Date, dayLordIndex: number): { planet: string; planetTa: string; quality: 'benefic' | 'malefic' | 'neutral' } {
  const hourOfDay = date.getHours();
  const horaIndex = (dayLordIndex + hourOfDay) % 7;
  const planet = CHALDEAN_ORDER[horaIndex];
  const planetTaMap: Record<string, string> = {
    Saturn: 'சனி', Jupiter: 'குரு', Mars: 'செவ்வாய்', Sun: 'சூரியன்',
    Venus: 'சுக்கிரன்', Mercury: 'புதன்', Moon: 'சந்திரன்',
  };
  const qualityMap: Record<string, 'benefic' | 'malefic' | 'neutral'> = {
    Jupiter: 'benefic', Venus: 'benefic', Moon: 'benefic', Mercury: 'neutral',
    Sun: 'neutral', Mars: 'malefic', Saturn: 'malefic',
  };
  return {
    planet,
    planetTa: planetTaMap[planet] ?? planet,
    quality: qualityMap[planet] ?? 'neutral',
  };
}

function formatHour(decimal: number): string {
  const h = Math.floor(decimal);
  const m = Math.round((decimal - h) * 60);
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
}

function isTimeInSlot(
  currentHour: number,
  slot: [number, number],
): boolean {
  return currentHour >= slot[0] && currentHour < slot[1];
}

export function calculatePanchang(input: MuhurthaSearchInput): PanchangData {
  const [y, mo, d] = input.date.split('-').map(Number);
  const [hh, mm] = input.time.split(':').map(Number);

  const localDate = new Date(y, mo - 1, d, hh, mm, 0);
  const tzOffsetMs =
    new Date(
      localDate.toLocaleString('en-US', { timeZone: input.timezone }),
    ).getTime() -
    new Date(localDate.toLocaleString('en-US', { timeZone: 'UTC' })).getTime();
  const utcDate = new Date(localDate.getTime() - tzOffsetMs);

  const jd = dateToJulianDay(utcDate);
  const ayanamsa = getLahiriAyanamsa(jd);
  const sunTropical = getSunTropicalLongitude(jd);
  const moonTropical = getMoonTropicalLongitude(jd);
  const sunSidereal = getSiderealLongitude(sunTropical, ayanamsa);
  const moonSidereal = getSiderealLongitude(moonTropical, ayanamsa);

  const sunMoonDiff = (moonSidereal - sunSidereal + 360) % 360;
  const tithiFloat = sunMoonDiff / 12;
  const tithiNumber = Math.floor(tithiFloat) + 1;
  const tithiMeta =
    TITHIS.find((t) => t.number === tithiNumber) ?? TITHIS[0];

  const nakshatraIndex = Math.floor(moonSidereal / (360 / 27));
  const nakshatraMeta = NAKSHATRAS[nakshatraIndex] ?? NAKSHATRAS[0];

  const yogaSum = (sunSidereal + moonSidereal) % 360;
  const yogaIndex = Math.floor(yogaSum / (360 / 27));
  const yogaMeta = YOGAS[yogaIndex] ?? YOGAS[0];

  const karanaFloat = tithiFloat * 2;
  const karanaSequence = [
    1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1,
    2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2,
    3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
  ];
  const karanaSeqIndex = Math.floor(karanaFloat) % karanaSequence.length;
  const karanaNumber = karanaSequence[karanaSeqIndex] ?? 1;
  const karanaMeta = KARANAS.find((k) => k.number === karanaNumber) ?? KARANAS[0];

  const dayOfWeek = utcDate.getDay();
  const vaaraMeta = VAARA[dayOfWeek];

  const dayLordOrder: Record<number, number> = {
    0: 3, 1: 6, 2: 4, 3: 5, 4: 1, 5: 2, 6: 0,
  };
  const hora = getHora(utcDate, dayLordOrder[dayOfWeek] ?? 0);

  const currentHour = hh + mm / 60;
  const rahuSlot = RAHU_KALAM_SLOTS[dayOfWeek] ?? [0, 0];
  const yamSlot = YAMAGANDAM_SLOTS[dayOfWeek] ?? [0, 0];
  const kuliSlot = KULIGAI_SLOTS[dayOfWeek] ?? [0, 0];

  const rahuKalam: TimePeriod = {
    start: formatHour(rahuSlot[0]),
    end: formatHour(rahuSlot[1]),
    isActive: isTimeInSlot(currentHour, rahuSlot),
  };
  const yamagandam: TimePeriod = {
    start: formatHour(yamSlot[0]),
    end: formatHour(yamSlot[1]),
    isActive: isTimeInSlot(currentHour, yamSlot),
  };
  const kuligai: TimePeriod = {
    start: formatHour(kuliSlot[0]),
    end: formatHour(kuliSlot[1]),
    isActive: isTimeInSlot(currentHour, kuliSlot),
  };

  const midday = 12;
  const abhijitStart = midday - 0.4;
  const abhijitEnd = midday + 0.4;
  const abhijitMuhurtha: TimePeriod = {
    start: formatHour(abhijitStart),
    end: formatHour(abhijitEnd),
    isActive: currentHour >= abhijitStart && currentHour < abhijitEnd,
  };

  const lagnaSignNum = getLagnaSign(localDate, input.latitude, input.longitude, input.timezone);
  const lagnaSignMeta = ZODIAC_SIGNS[lagnaSignNum - 1] ?? ZODIAC_SIGNS[0];
  const lagna: LagnaData = {
    sign: lagnaSignNum,
    name: lagnaSignMeta.name,
    nameTa: lagnaSignMeta.nameTa,
    lord: lagnaSignMeta.lord,
  };

  let chandrashtama = false;
  if (input.birthNakshatra) {
    const birthIdx = NAKSHATRAS.findIndex((n) => n.name === input.birthNakshatra);
    if (birthIdx >= 0) {
      const birthSign = Math.floor((birthIdx * (360 / 27)) / 30) + 1;
      const moonSign = Math.floor(moonSidereal / 30) + 1;
      const houseDiff = ((moonSign - birthSign + 12) % 12) + 1;
      chandrashtama = houseDiff === 8;
    }
  }

  let taraBalance: 'favorable' | 'unfavorable' | 'neutral' = 'neutral';
  if (input.birthNakshatra) {
    const birthIdx = NAKSHATRAS.findIndex((n) => n.name === input.birthNakshatra);
    if (birthIdx >= 0) {
      const count = ((nakshatraIndex - birthIdx + 27) % 27) + 1;
      const taraNum = ((count - 1) % 9) + 1;
      const goodTaras = [1, 2, 4, 6, 8, 9];
      const badTaras = [3, 5, 7];
      taraBalance = goodTaras.includes(taraNum)
        ? 'favorable'
        : badTaras.includes(taraNum)
          ? 'unfavorable'
          : 'neutral';
    }
  }

  return {
    tithi: {
      number: tithiMeta.number,
      name: tithiMeta.name,
      nameTa: tithiMeta.nameTa,
      paksha: tithiMeta.paksha as TithiData['paksha'],
      quality: tithiMeta.quality as TithiData['quality'],
    },
    nakshatra: {
      number: nakshatraMeta.number,
      name: nakshatraMeta.name,
      nameTa: nakshatraMeta.nameTa,
      type: nakshatraMeta.type as NakshatraData['type'],
      lord: nakshatraMeta.lord,
      lordTa: nakshatraMeta.lordTa,
      degree: parseFloat(moonSidereal.toFixed(4)),
    },
    yoga: {
      number: yogaMeta.number,
      name: yogaMeta.name,
      nameTa: yogaMeta.nameTa,
      quality: yogaMeta.quality as YogaData['quality'],
    },
    karana: {
      number: karanaMeta.number,
      name: karanaMeta.name,
      nameTa: karanaMeta.nameTa,
      quality: karanaMeta.quality as KaranaData['quality'],
    },
    vaara: {
      number: vaaraMeta.number,
      name: vaaraMeta.name,
      nameTa: vaaraMeta.nameTa,
      lord: vaaraMeta.lord,
      lordTa: vaaraMeta.lordTa,
    },
    hora,
    rahuKalam,
    yamagandam,
    kuligai,
    abhijitMuhurtha,
    moonLongitude: parseFloat(moonSidereal.toFixed(4)),
    sunLongitude: parseFloat(sunSidereal.toFixed(4)),
    lagna,
    chandrashtama,
    taraBalance,
  };
}

export function calculateMuhurtha(input: MuhurthaSearchInput): MuhurthaResult {
  const category = MUHURTHA_CATEGORIES.find((c) => c.id === input.category);
  if (!category) {
    throw new Error(`Unknown category: ${input.category}`);
  }

  const panchang = calculatePanchang(input);

  const allRules = [
    ...PANCHANG_RULES(),
    ...DOSHA_RULES(),
    ...STRENGTH_RULES(),
  ];

  const ruleResults = executeAllRules(allRules, panchang, category);
  const aggregated = aggregateRuleResults(ruleResults);
  const verdict = generateVerdict(aggregated.normalizedScore);

  const positiveFactors: BilingualText[] = ruleResults
    .filter((r) => r.impact === 'positive')
    .map((r) => ({ en: r.reason.en, ta: r.reason.ta }));

  const negativeFactors: BilingualText[] = ruleResults
    .filter((r) => r.impact === 'negative')
    .map((r) => ({ en: r.reason.en, ta: r.reason.ta }));

  const windows = generateTimeWindows(input, category, panchang, aggregated.normalizedScore);

  const suitableTimes = windows
    .filter((w) => w.type === 'suitable')
    .map((w) => `${w.startTime}–${w.endTime}`);

  const avoidTimes = windows
    .filter((w) => w.type === 'avoid')
    .map((w) => `${w.startTime}–${w.endTime} (${w.label.en})`);

  return {
    requestId: uuidv4(),
    category: category.id,
    categoryNameTa: category.nameTa,
    date: input.date,
    time: input.time,
    score: aggregated.normalizedScore,
    stars: aggregated.stars,
    starDisplay: aggregated.starDisplay,
    verdict,
    panchang,
    windows,
    positiveFactors,
    negativeFactors,
    ruleResults,
    suitableTimes,
    avoidTimes,
    generatedAt: new Date().toISOString(),
  };
}

function generateTimeWindows(
  input: MuhurthaSearchInput,
  category: CategoryDefinition,
  panchang: PanchangData,
  baseScore: number,
): MuhurthaWindow[] {
  const dayOfWeek = new Date(input.date).getDay();
  const windows: MuhurthaWindow[] = [];

  const avoidSlots: Array<{ start: number; end: number; label: BilingualText }> = [
    {
      start: RAHU_KALAM_SLOTS[dayOfWeek][0],
      end: RAHU_KALAM_SLOTS[dayOfWeek][1],
      label: { en: 'Rahu Kalam — Strictly Avoid', ta: 'ராகு காலம் — கண்டிப்பாக தவிர்க்கவும்' },
    },
    {
      start: YAMAGANDAM_SLOTS[dayOfWeek][0],
      end: YAMAGANDAM_SLOTS[dayOfWeek][1],
      label: { en: 'Yamagandam — Avoid', ta: 'யமகண்டம் — தவிர்க்கவும்' },
    },
    {
      start: KULIGAI_SLOTS[dayOfWeek][0],
      end: KULIGAI_SLOTS[dayOfWeek][1],
      label: { en: 'Kuligai — Avoid', ta: 'குளிகை — தவிர்க்கவும்' },
    },
  ];

  for (const slot of avoidSlots) {
    windows.push({
      startTime: formatHour(slot.start),
      endTime: formatHour(slot.end),
      score: 15,
      stars: 1,
      label: slot.label,
      type: 'avoid',
    });
  }

  const abhijitStart = 11.8;
  const abhijitEnd = 12.6;
  const abhijitScore = Math.min(100, baseScore + 10);
  windows.push({
    startTime: formatHour(abhijitStart),
    endTime: formatHour(abhijitEnd),
    score: abhijitScore,
    stars: abhijitScore >= 88 ? 5 : abhijitScore >= 72 ? 4 : 3,
    label: {
      en: 'Abhijit Muhurtha — Highly Auspicious',
      ta: 'அபிஜித் முகூர்த்தம் — மிகவும் சுபமானது',
    },
    type: 'suitable',
  });

  const morningScore = baseScore >= 60 ? baseScore - 5 : baseScore;
  if (morningScore >= 50) {
    windows.push({
      startTime: '06:00',
      endTime: '07:30',
      score: morningScore,
      stars: morningScore >= 72 ? 4 : 3,
      label: { en: 'Morning Brahma Muhurtha Window', ta: 'காலை பிரம்ம முகூர்த்த சாளரம்' },
      type: morningScore >= 60 ? 'suitable' : 'neutral',
    });
  }

  const eveningStart = 17.0;
  const eveningEnd = 18.5;
  const rahuEnd = RAHU_KALAM_SLOTS[dayOfWeek][1];
  if (eveningStart > rahuEnd) {
    const eveningScore = baseScore >= 55 ? baseScore - 8 : baseScore;
    windows.push({
      startTime: formatHour(eveningStart),
      endTime: formatHour(eveningEnd),
      score: eveningScore,
      stars: eveningScore >= 72 ? 4 : eveningScore >= 52 ? 3 : 2,
      label: { en: 'Evening Sandhya Window', ta: 'மாலை சந்த்யா சாளரம்' },
      type: eveningScore >= 55 ? 'suitable' : 'neutral',
    });
  }

  windows.sort((a, b) => {
    const timeA = a.startTime.split(':').map(Number);
    const timeB = b.startTime.split(':').map(Number);
    return timeA[0] * 60 + timeA[1] - (timeB[0] * 60 + timeB[1]);
  });

  return windows;
}

export function getMuhurthaCategories() {
  return MUHURTHA_CATEGORIES.map((c) => ({
    id: c.id,
    name: c.name,
    nameTa: c.nameTa,
    description: c.description,
    descriptionTa: c.descriptionTa,
  }));
}
