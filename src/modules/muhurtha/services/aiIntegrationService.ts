import type { MuhurthaResult } from '../../../types/muhurtha.types';
import type { MuhurthaAiInput } from '../validators/muhurthaValidator';
import { calculateMuhurtha } from './muhurthaService';

export interface AiMuhurthaPayload {
  schema_version: string;
  request_id: string;
  generated_at: string;
  query: {
    date: string;
    time: string;
    location: { latitude: number; longitude: number; timezone: string };
    category: { id: string; name: string; name_ta: string };
    birth_nakshatra?: string;
  };
  result: {
    score: number;
    max_score: number;
    stars: number;
    star_display: string;
    verdict_en: string;
    verdict_ta: string;
    window_type: 'suitable' | 'avoid' | 'neutral';
  };
  panchang: {
    tithi: { number: number; name: string; name_ta: string; paksha: string; quality: string };
    nakshatra: { number: number; name: string; name_ta: string; type: string; lord: string };
    yoga: { number: number; name: string; name_ta: string; quality: string };
    karana: { number: number; name: string; name_ta: string; quality: string };
    vaara: { name: string; name_ta: string; lord: string };
    hora: { planet: string; quality: string };
    rahu_kalam: string;
    yamagandam: string;
    kuligai: string;
    abhijit_muhurtha: string;
    moon_longitude_deg: number;
    sun_longitude_deg: number;
    lagna: { sign: number; name: string; name_ta: string; lord: string };
    chandrashtama: boolean;
    tara_bala: string;
  };
  doshas: Array<{ name: string; active: boolean; severity: 'critical' | 'moderate' | 'low' }>;
  positive_factors: Array<{ en: string; ta: string }>;
  negative_factors: Array<{ en: string; ta: string }>;
  suitable_windows: Array<{ start: string; end: string; score: number; stars: number }>;
  avoid_windows: Array<{ start: string; end: string; reason_en: string; reason_ta: string }>;
  recommendations: {
    proceed: boolean;
    caution_level: 'none' | 'low' | 'medium' | 'high' | 'critical';
    en: string;
    ta: string;
    remedies?: string[];
  };
  rule_breakdown: Array<{
    rule: string;
    impact: 'positive' | 'negative' | 'neutral';
    weight: number;
    score: number;
    reason_en: string;
    reason_ta: string;
  }>;
  token_hints: {
    total_positive_count: number;
    total_negative_count: number;
    dominant_dosha?: string;
    primary_auspicious_factor?: string;
  };
}

export function buildAiPayload(
  input: MuhurthaAiInput,
  result: MuhurthaResult,
): AiMuhurthaPayload {
  const panchang = result.panchang;

  const doshas: AiMuhurthaPayload['doshas'] = [];

  if (panchang.rahuKalam.isActive) {
    doshas.push({ name: 'Rahu Kalam', active: true, severity: 'critical' });
  }
  if (panchang.yamagandam.isActive) {
    doshas.push({ name: 'Yamagandam', active: true, severity: 'critical' });
  }
  if (panchang.kuligai.isActive) {
    doshas.push({ name: 'Kuligai', active: true, severity: 'moderate' });
  }
  if (panchang.chandrashtama) {
    doshas.push({ name: 'Chandrashtama', active: true, severity: 'critical' });
  }
  if (panchang.tithi.quality === 'inauspicious') {
    doshas.push({ name: `Inauspicious Tithi (${panchang.tithi.name})`, active: true, severity: 'moderate' });
  }
  if (panchang.yoga.quality === 'bad') {
    doshas.push({ name: `Malefic Yoga (${panchang.yoga.name})`, active: true, severity: 'moderate' });
  }
  if (panchang.karana.name === 'Vishti') {
    doshas.push({ name: 'Vishti (Bhadra) Karana', active: true, severity: 'critical' });
  }
  if ([23, 24, 25, 26, 27].includes(panchang.nakshatra.number)) {
    doshas.push({ name: `Panchaka (${panchang.nakshatra.name})`, active: true, severity: 'low' });
  }

  const suitableWindows = result.windows
    .filter((w) => w.type === 'suitable')
    .map((w) => ({
      start: w.startTime,
      end: w.endTime,
      score: w.score,
      stars: w.stars,
    }));

  const avoidWindows = result.windows
    .filter((w) => w.type === 'avoid')
    .map((w) => ({
      start: w.startTime,
      end: w.endTime,
      reason_en: w.label.en,
      reason_ta: w.label.ta,
    }));

  const hasCriticalDosha = doshas.some((d) => d.severity === 'critical');
  const hasModerateDoshas = doshas.filter((d) => d.severity !== 'low').length >= 3;

  const cautionLevel = hasCriticalDosha
    ? 'critical'
    : hasModerateDoshas
      ? 'high'
      : result.score < 40
        ? 'medium'
        : result.score < 60
          ? 'low'
          : 'none';

  const proceed = result.score >= 55 && !hasCriticalDosha;

  const remedies: string[] = [];
  if (panchang.rahuKalam.isActive) {
    remedies.push('Perform Rahu Kalam Shanti — chant Rahu beeja mantra "Om Bhram Bhreem Bhroum Sah Rahave Namah" 18 times');
  }
  if (panchang.chandrashtama) {
    remedies.push('Avoid all new beginnings; if unavoidable, perform a special Chandrashtama Shanti pooja');
  }
  if (panchang.karana.name === 'Vishti') {
    remedies.push('Wait for Vishti Karana to pass; perform Vishti Shanti if cannot postpone');
  }
  if ([23, 24, 25, 26, 27].includes(panchang.nakshatra.number)) {
    remedies.push('Perform Panchaka Shanti — specific ritual to neutralize Panchaka dosha');
  }
  if (result.score >= 80) {
    remedies.push('Light a ghee lamp (Nanda Deepa) before starting the ceremony for additional blessings');
    remedies.push('Chant "Om Gam Ganapataye Namah" 108 times to invoke auspicious beginnings');
  }

  const dominantDosha = doshas
    .filter((d) => d.active && d.severity === 'critical')
    .map((d) => d.name)[0];

  const primaryAuspiciousRule = result.ruleResults
    .filter((r) => r.impact === 'positive')
    .sort((a, b) => b.contributedScore * b.weight - a.contributedScore * a.weight)[0];

  const ruleBreakdown = result.ruleResults.map((r) => ({
    rule: r.ruleName,
    impact: r.impact,
    weight: r.weight,
    score: r.contributedScore,
    reason_en: r.reason.en,
    reason_ta: r.reason.ta,
  }));

  return {
    schema_version: '1.0.0',
    request_id: result.requestId,
    generated_at: result.generatedAt,
    query: {
      date: input.date,
      time: input.time,
      location: {
        latitude: input.latitude,
        longitude: input.longitude,
        timezone: input.timezone,
      },
      category: {
        id: result.category,
        name: result.category,
        name_ta: result.categoryNameTa,
      },
      birth_nakshatra: input.birthNakshatra,
    },
    result: {
      score: result.score,
      max_score: 100,
      stars: result.stars,
      star_display: result.starDisplay,
      verdict_en: result.verdict.en,
      verdict_ta: result.verdict.ta,
      window_type: result.score >= 72 ? 'suitable' : result.score < 40 ? 'avoid' : 'neutral',
    },
    panchang: {
      tithi: {
        number: panchang.tithi.number,
        name: panchang.tithi.name,
        name_ta: panchang.tithi.nameTa,
        paksha: panchang.tithi.paksha,
        quality: panchang.tithi.quality,
      },
      nakshatra: {
        number: panchang.nakshatra.number,
        name: panchang.nakshatra.name,
        name_ta: panchang.nakshatra.nameTa,
        type: panchang.nakshatra.type,
        lord: panchang.nakshatra.lord,
      },
      yoga: {
        number: panchang.yoga.number,
        name: panchang.yoga.name,
        name_ta: panchang.yoga.nameTa,
        quality: panchang.yoga.quality,
      },
      karana: {
        number: panchang.karana.number,
        name: panchang.karana.name,
        name_ta: panchang.karana.nameTa,
        quality: panchang.karana.quality,
      },
      vaara: {
        name: panchang.vaara.name,
        name_ta: panchang.vaara.nameTa,
        lord: panchang.vaara.lord,
      },
      hora: {
        planet: panchang.hora.planet,
        quality: panchang.hora.quality,
      },
      rahu_kalam: `${panchang.rahuKalam.start}–${panchang.rahuKalam.end}${panchang.rahuKalam.isActive ? ' [ACTIVE]' : ''}`,
      yamagandam: `${panchang.yamagandam.start}–${panchang.yamagandam.end}${panchang.yamagandam.isActive ? ' [ACTIVE]' : ''}`,
      kuligai: `${panchang.kuligai.start}–${panchang.kuligai.end}${panchang.kuligai.isActive ? ' [ACTIVE]' : ''}`,
      abhijit_muhurtha: `${panchang.abhijitMuhurtha.start}–${panchang.abhijitMuhurtha.end}${panchang.abhijitMuhurtha.isActive ? ' [ACTIVE]' : ''}`,
      moon_longitude_deg: panchang.moonLongitude,
      sun_longitude_deg: panchang.sunLongitude,
      lagna: {
        sign: panchang.lagna.sign,
        name: panchang.lagna.name,
        name_ta: panchang.lagna.nameTa,
        lord: panchang.lagna.lord,
      },
      chandrashtama: panchang.chandrashtama,
      tara_bala: panchang.taraBalance,
    },
    doshas,
    positive_factors: result.positiveFactors.map((f) => ({ en: f.en, ta: f.ta })),
    negative_factors: result.negativeFactors.map((f) => ({ en: f.en, ta: f.ta })),
    suitable_windows: suitableWindows,
    avoid_windows: avoidWindows,
    recommendations: {
      proceed,
      caution_level: cautionLevel,
      en: proceed
        ? `This muhurtha is ${result.stars >= 4 ? 'highly ' : ''}auspicious for ${result.category}. Score: ${result.score}/100. ${result.verdict.en}`
        : `This time is NOT recommended for ${result.category}. ${result.verdict.en} Consider rescheduling to one of the suitable windows listed.`,
      ta: proceed
        ? `இந்த முகூர்த்தம் ${result.categoryNameTa}க்கு ${result.stars >= 4 ? 'மிகவும் ' : ''}சுபமானது. மதிப்பெண்: ${result.score}/100. ${result.verdict.ta}`
        : `இந்த நேரம் ${result.categoryNameTa}க்கு பரிந்துரைக்கப்படவில்லை. ${result.verdict.ta} பட்டியலிடப்பட்ட பொருத்தமான நேர சாளரங்களில் ஒன்றுக்கு மாற்றி திட்டமிடுவதை கருத்தில் கொள்ளவும்.`,
      remedies: remedies.length > 0 ? remedies : undefined,
    },
    rule_breakdown: ruleBreakdown,
    token_hints: {
      total_positive_count: result.positiveFactors.length,
      total_negative_count: result.negativeFactors.length,
      dominant_dosha: dominantDosha,
      primary_auspicious_factor: primaryAuspiciousRule?.ruleName,
    },
  };
}

export function generateAiResponse(input: MuhurthaAiInput): AiMuhurthaPayload {
  const searchInput = {
    date: input.date,
    time: input.time,
    latitude: input.latitude,
    longitude: input.longitude,
    timezone: input.timezone,
    category: input.category,
    birthNakshatra: input.birthNakshatra,
  };

  const result = calculateMuhurtha(searchInput);
  return buildAiPayload(input, result);
}
