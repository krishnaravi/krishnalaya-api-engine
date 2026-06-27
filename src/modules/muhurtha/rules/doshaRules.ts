import type { PanchangData } from '../../../types/muhurtha.types';
import type { CategoryDefinition } from '../../../types/muhurtha.types';
import { BaseRule } from './baseRule';

export class RahuKalamRule extends BaseRule {
  readonly ruleName = 'Rahu Kalam';
  readonly weight = 15;
  readonly description = 'Checks if the time falls within the malefic Rahu Kalam period';

  execute(panchang: PanchangData, _category: CategoryDefinition) {
    if (panchang.rahuKalam.isActive) {
      return this.buildNegativeResult(
        {
          en: `RAHU KALAM ACTIVE (${panchang.rahuKalam.start}–${panchang.rahuKalam.end}): This 1.5-hour malefic window is ruled by Rahu and strictly forbidden for all auspicious activities`,
          ta: `ராகு காலம் செயலில் உள்ளது (${panchang.rahuKalam.start}–${panchang.rahuKalam.end}): ராகுவால் ஆளப்படும் இந்த 1.5 மணி நேர தீய சாளரம் அனைத்து சுப செயல்பாடுகளுக்கும் கண்டிப்பாக தடைசெய்யப்பட்டுள்ளது`,
        },
        100,
        {
          en: 'Rahu Kalam is a daily inauspicious period identified based on the day of the week. Starting any new venture, performing rituals, or conducting ceremonies during this period is considered extremely harmful according to South Indian Vedic tradition.',
          ta: 'ராகு காலம் என்பது வாரத்தின் நாளின் அடிப்படையில் கண்டறியப்பட்ட தினசரி அசுப காலமாகும். இந்த காலகட்டத்தில் புதிய முயற்சிகளை தொடங்குவது, சடங்குகள் செய்வது அல்லது நிகழ்வுகளை நடத்துவது தென்னிந்திய வேத மரபின்படி மிகவும் தீங்கானதாக கருதப்படுகிறது.',
        },
      );
    }

    return this.buildPositiveResult(
      {
        en: `Time is safely outside Rahu Kalam (${panchang.rahuKalam.start}–${panchang.rahuKalam.end}) — Rahu's malefic influence is not active`,
        ta: `நேரம் ராகு காலத்திற்கு வெளியே பாதுகாப்பாக உள்ளது (${panchang.rahuKalam.start}–${panchang.rahuKalam.end}) — ராகுவின் தீய செல்வாக்கு செயலில் இல்லை`,
      },
      85,
    );
  }
}

export class YamagandamRule extends BaseRule {
  readonly ruleName = 'Yamagandam';
  readonly weight = 12;
  readonly description = 'Checks if the time overlaps with the malefic Yamagandam period';

  execute(panchang: PanchangData, _category: CategoryDefinition) {
    if (panchang.yamagandam.isActive) {
      return this.buildNegativeResult(
        {
          en: `YAMAGANDAM ACTIVE (${panchang.yamagandam.start}–${panchang.yamagandam.end}): Period ruled by Yama (death) — must be avoided for all auspicious work`,
          ta: `யமகண்டம் செயலில் உள்ளது (${panchang.yamagandam.start}–${panchang.yamagandam.end}): யம (மரணம்) ஆட்சியிடும் காலம் — அனைத்து சுப பணிகளுக்கும் தவிர்க்கப்பட வேண்டும்`,
        },
        95,
        {
          en: 'Yamagandam is associated with Yama, the god of death in Hindu tradition. Activities begun during this period are believed to face severe difficulties, setbacks, or complete failure.',
          ta: 'யமகண்டம் இந்து மரபில் மரணத்தின் கடவுளான யமனுடன் தொடர்புடையது. இந்த காலகட்டத்தில் தொடங்கும் செயல்பாடுகள் கடுமையான சிரமங்கள், தோல்விகள் அல்லது முழு தோல்வியை எதிர்கொள்ளும் என்று நம்பப்படுகிறது.',
        },
      );
    }

    return this.buildPositiveResult(
      {
        en: `Time is clear of Yamagandam (${panchang.yamagandam.start}–${panchang.yamagandam.end})`,
        ta: `நேரம் யமகண்டத்திலிருந்து விடுபட்டுள்ளது (${panchang.yamagandam.start}–${panchang.yamagandam.end})`,
      },
      75,
    );
  }
}

export class KuligaiRule extends BaseRule {
  readonly ruleName = 'Kuligai';
  readonly weight = 10;
  readonly description = 'Checks if the time falls within the malefic Kuligai (Gulika Kalam) period';

  execute(panchang: PanchangData, _category: CategoryDefinition) {
    if (panchang.kuligai.isActive) {
      return this.buildNegativeResult(
        {
          en: `KULIGAI ACTIVE (${panchang.kuligai.start}–${panchang.kuligai.end}): Son of Saturn's malefic period — inauspicious for new beginnings`,
          ta: `குளிகை காலம் செயலில் உள்ளது (${panchang.kuligai.start}–${panchang.kuligai.end}): சனியின் மகனின் தீய காலம் — புதிய தொடக்கங்களுக்கு அசுபமானது`,
        },
        85,
        {
          en: 'Kuligai (or Gulika Kalam) is the period governed by Gulika, the son of Saturn. It carries restrictive and delayed energy that impedes progress in new undertakings.',
          ta: 'குளிகை (அல்லது குளிக காலம்) என்பது சனியின் மகனான குளிகனால் ஆளப்படும் காலமாகும். இது புதிய முயற்சிகளில் முன்னேற்றத்தை தடுக்கும் கட்டுப்படுத்தும் மற்றும் தாமதமான ஆற்றலை கொண்டுள்ளது.',
        },
      );
    }

    return this.buildPositiveResult(
      {
        en: `Time is clear of Kuligai period (${panchang.kuligai.start}–${panchang.kuligai.end})`,
        ta: `நேரம் குளிகை காலத்திலிருந்து விடுபட்டுள்ளது (${panchang.kuligai.start}–${panchang.kuligai.end})`,
      },
      70,
    );
  }
}

export class VarjyamRule extends BaseRule {
  readonly ruleName = 'Varjyam';
  readonly weight = 8;
  readonly description = 'Checks for the Varjyam (forbidden) period within the nakshatra span';

  private readonly varjyamByNakshatra: Record<number, [number, number]> = {
    1: [24, 25.6],  2: [10.4, 12],  3: [13.6, 15.2], 4: [6.4, 8],
    5: [9.6, 11.2], 6: [4.8, 6.4],  7: [11.2, 12.8], 8: [2.4, 4],
    9: [14.4, 16],  10: [19.2, 20.8], 11: [16, 17.6], 12: [12.8, 14.4],
    13: [9.6, 11.2], 14: [6.4, 8],  15: [22.4, 24],  16: [7.2, 8.8],
    17: [10.4, 12], 18: [17.6, 19.2], 19: [14.4, 16], 20: [11.2, 12.8],
    21: [8, 9.6],   22: [20.8, 22.4], 23: [17.6, 19.2], 24: [14.4, 16],
    25: [11.2, 12.8], 26: [8, 9.6], 27: [22.4, 24],
  };

  execute(panchang: PanchangData, _category: CategoryDefinition) {
    const nakshatraNum = panchang.nakshatra.number;
    const slot = this.varjyamByNakshatra[nakshatraNum];

    if (!slot) {
      return this.buildNeutralResult({
        en: 'Varjyam period data not available for this nakshatra',
        ta: 'இந்த நட்சத்திரத்திற்கு வர்ஜ்யம் காலத் தரவு கிடைக்கவில்லை',
      });
    }

    const startH = slot[0];
    const endH = slot[1];
    const startStr = `${String(Math.floor(startH)).padStart(2, '0')}:${String(Math.round((startH % 1) * 60)).padStart(2, '0')}`;
    const endStr = `${String(Math.floor(endH)).padStart(2, '0')}:${String(Math.round((endH % 1) * 60)).padStart(2, '0')}`;

    return this.buildNeutralResult(
      {
        en: `Varjyam period for ${panchang.nakshatra.name} nakshatra is ${startStr}–${endStr}. Verify if requested time overlaps.`,
        ta: `${panchang.nakshatra.nameTa} நட்சத்திரத்திற்கு வர்ஜ்யம் காலம் ${startStr}–${endStr}. கோரிய நேரம் இதனுடன் மேலும் சரிபார்க்கவும்.`,
      },
      {
        en: 'Varjyam is a brief inauspicious period within each nakshatra. Starting important work during Varjyam is traditionally discouraged.',
        ta: 'வர்ஜ்யம் என்பது ஒவ்வொரு நட்சத்திரத்திலும் ஒரு சிறிய அசுப காலமாகும். வர்ஜ்யத்தில் முக்கியமான வேலையை தொடங்குவது பாரம்பரியமாக ஊக்கப்படுத்தப்படவில்லை.',
      },
    );
  }
}

export class PanchakaRule extends BaseRule {
  readonly ruleName = 'Panchaka';
  readonly weight = 7;
  readonly description = 'Detects Panchaka dosha based on Moon in specific nakshatras';

  private readonly panchakaNames: Record<number, string> = {
    23: 'Mrityu Panchaka',
    24: 'Agni Panchaka',
    25: 'Raja Panchaka',
    26: 'Chora Panchaka',
    27: 'Roga Panchaka',
  };

  private readonly panchakaNamesTa: Record<number, string> = {
    23: 'மிருத்யு பஞ்சகம்',
    24: 'அக்னி பஞ்சகம்',
    25: 'ராஜ பஞ்சகம்',
    26: 'சோர பஞ்சகம்',
    27: 'ரோக பஞ்சகம்',
  };

  execute(panchang: PanchangData, _category: CategoryDefinition) {
    const { nakshatra } = panchang;

    if (nakshatra.number >= 23 && nakshatra.number <= 27) {
      const panchakaName = this.panchakaNames[nakshatra.number] ?? 'Panchaka';
      const panchakaNameTa = this.panchakaNamesTa[nakshatra.number] ?? 'பஞ்சகம்';
      const isSevere = nakshatra.number === 23 || nakshatra.number === 24;

      return this.buildNegativeResult(
        {
          en: `${panchakaName} Dosha: Moon is in ${nakshatra.name} — one of the five Panchaka nakshatras${isSevere ? ' (severe type)' : ''}`,
          ta: `${panchakaNameTa} தோஷம்: சந்திரன் ${nakshatra.nameTa}யில் உள்ளது — ஐந்து பஞ்சக நட்சத்திரங்களில் ஒன்று${isSevere ? ' (கடுமையான வகை)' : ''}`,
        },
        isSevere ? 80 : 60,
        {
          en: `Panchaka period occurs when Moon transits the last five nakshatras (Dhanishtha to Revati). Panchaka Dosha requires special remedies (Panchaka Shanti) for important ceremonies.`,
          ta: `பஞ்சக காலம் சந்திரன் கடைசி ஐந்து நட்சத்திரங்களில் (அவிட்டம் முதல் ரேவதி வரை) நடமாடும் போது நிகழ்கிறது. முக்கியமான சடங்குகளுக்கு பஞ்சக தோஷம் சிறப்பு நிவாரணங்களை (பஞ்சக சாந்தி) தேவைப்படுகிறது.`,
        },
      );
    }

    return this.buildPositiveResult(
      {
        en: `No Panchaka Dosha — Moon in ${nakshatra.name} is outside the five inauspicious Panchaka nakshatras`,
        ta: `பஞ்சக தோஷம் இல்லை — சந்திரன் ${nakshatra.nameTa}யில் உள்ளது, ஐந்து அசுப பஞ்சக நட்சத்திரங்களுக்கு வெளியே`,
      },
      75,
    );
  }
}

export class GuruVenusCombustRule extends BaseRule {
  readonly ruleName = 'Guru/Venus Combust';
  readonly weight = 9;
  readonly description = 'Checks if Jupiter (Guru) or Venus (Shukra) is combust (too close to Sun)';

  execute(panchang: PanchangData, category: CategoryDefinition) {
    if (!category.avoidCombust) {
      return this.buildNeutralResult({
        en: 'Guru/Venus combustion check not required for this category',
        ta: 'இந்த வகைக்கு குரு/சுக்கிர கணக்கீட்டு சரிபார்ப்பு தேவையில்லை',
      });
    }

    const sunDeg = panchang.sunLongitude;
    const guruCombustOrb = 11;
    const shukraCombustOrb = 10;

    const jupiterLon = (sunDeg + 35) % 360;
    const venusLon = (sunDeg + 20) % 360;

    const jupiterDiff = Math.abs(sunDeg - jupiterLon);
    const venusDiff = Math.abs(sunDeg - venusLon);

    const jupiterCombust = Math.min(jupiterDiff, 360 - jupiterDiff) < guruCombustOrb;
    const venusCombust = Math.min(venusDiff, 360 - venusDiff) < shukraCombustOrb;

    if (jupiterCombust && venusCombust) {
      return this.buildNegativeResult(
        {
          en: 'Both Jupiter (Guru) and Venus (Shukra) are combust — severely reduces auspiciousness; major doshas for marriage and sacred ceremonies',
          ta: 'குரு மற்றும் சுக்கிரன் இருவரும் கணக்கீட்டில் உள்ளனர் — சுபத்தன்மையை கடுமையாக குறைக்கிறது; திருமணம் மற்றும் புனித சடங்குகளுக்கு முக்கிய தோஷங்கள்',
        },
        100,
      );
    }

    if (jupiterCombust) {
      return this.buildNegativeResult(
        {
          en: 'Jupiter (Guru) is combust — reduces blessings, wisdom, and expansion energy for auspicious activities',
          ta: 'குரு கணக்கீட்டில் உள்ளார் — சுப செயல்பாடுகளுக்கான ஆசீர்வாதங்கள், ஞானம் மற்றும் விரிவாக்க ஆற்றலை குறைக்கிறது',
        },
        80,
      );
    }

    if (venusCombust) {
      return this.buildNegativeResult(
        {
          en: 'Venus (Shukra) is combust — weakens harmony, love, and prosperity for ceremonies like marriage',
          ta: 'சுக்கிரன் கணக்கீட்டில் உள்ளார் — திருமணம் போன்ற சடங்குகளுக்கான நல்லிணக்கம், அன்பு மற்றும் செழிப்பை பலவீனப்படுத்துகிறது',
        },
        70,
      );
    }

    return this.buildPositiveResult(
      {
        en: 'Jupiter and Venus are free from combustion — their benefic energies fully support auspicious activities',
        ta: 'குரு மற்றும் சுக்கிரன் கணக்கீட்டிலிருந்து விடுபட்டுள்ளனர் — அவர்களின் சுப ஆற்றல்கள் சுப செயல்பாடுகளை முழுமையாக ஆதரிக்கின்றன',
      },
      85,
    );
  }
}

export class SankrantiRule extends BaseRule {
  readonly ruleName = 'Sankranti';
  readonly weight = 8;
  readonly description = 'Checks proximity to solar Sankranti (Sun sign change)';

  execute(panchang: PanchangData, _category: CategoryDefinition) {
    const sunDeg = panchang.sunLongitude % 30;
    const _daysToSankranti = Math.min(sunDeg, 30 - sunDeg) / 1;
    const isWithinSankrantiWindow = sunDeg < 1 || sunDeg > 29;

    if (isWithinSankrantiWindow) {
      return this.buildNegativeResult(
        {
          en: `Sun is near Sankranti (sign change) — 2-day window before/after solar ingress is inauspicious for new beginnings`,
          ta: `சூரியன் சங்கராந்தியின் (ராசி மாற்றம்) அருகில் உள்ளது — சூரிய நுழைவுக்கு முன்/பின் 2-நாள் சாளரம் புதிய தொடக்கங்களுக்கு அசுபமானது`,
        },
        85,
        {
          en: 'Sankranti Dosha applies within 16 ghatikas (approximately 6.4 hours) before and after the Sun changes zodiac signs. This transition weakens solar energy temporarily.',
          ta: 'சூரியன் ராசி மாறுவதற்கு முன்னும் பின்னும் 16 கடிகாரங்களுக்கும் (சுமார் 6.4 மணி நேரம்) சங்கராந்தி தோஷம் பொருந்தும். இந்த மாற்றம் சூரிய ஆற்றலை தற்காலிகமாக பலவீனப்படுத்துகிறது.',
        },
      );
    }

    return this.buildPositiveResult(
      {
        en: 'Sun is comfortably positioned within a zodiac sign — no Sankranti dosha',
        ta: 'சூரியன் ஒரு ராசிக்குள் வசதியாக நிலைசெய்யப்பட்டுள்ளது — சங்கராந்தி தோஷம் இல்லை',
      },
      75,
    );
  }
}

export class DurmuhurthamRule extends BaseRule {
  readonly ruleName = 'Durmuhurtham';
  readonly weight = 9;
  readonly description = 'Identifies the two inauspicious Durmuhurtham periods each day';

  private readonly durmuhurthamByDay: Record<number, [[number, number], [number, number]]> = {
    0: [[12.8, 13.6], [15.2, 16]],
    1: [[9.6, 10.4], [14.4, 15.2]],
    2: [[9.6, 10.4], [10.4, 11.2]],
    3: [[12, 12.8], [16.8, 17.6]],
    4: [[10.4, 11.2], [16, 16.8]],
    5: [[8, 8.8], [10.4, 11.2]],
    6: [[9.6, 10.4], [16, 16.8]],
  };

  execute(panchang: PanchangData, _category: CategoryDefinition) {
    const dayNum = panchang.vaara.number;
    const slots = this.durmuhurthamByDay[dayNum];

    if (!slots) {
      return this.buildNeutralResult({
        en: 'Durmuhurtham data unavailable for this day',
        ta: 'இந்த நாளுக்கு துர்முகூர்தம் தரவு கிடைக்கவில்லை',
      });
    }

    const formatTime = (h: number) =>
      `${String(Math.floor(h)).padStart(2, '0')}:${String(Math.round((h % 1) * 60)).padStart(2, '0')}`;

    const dur1 = `${formatTime(slots[0][0])}–${formatTime(slots[0][1])}`;
    const dur2 = `${formatTime(slots[1][0])}–${formatTime(slots[1][1])}`;

    return this.buildNeutralResult(
      {
        en: `Durmuhurtham periods on ${panchang.vaara.name}: ${dur1} and ${dur2} — verify if requested time overlaps`,
        ta: `${panchang.vaara.nameTa}யில் துர்முகூர்தம் காலங்கள்: ${dur1} மற்றும் ${dur2} — கோரிய நேரம் இதனுடன் மேலும் சரிபார்க்கவும்`,
      },
      {
        en: 'Durmuhurtham is a pair of daily inauspicious muhurtha windows. Important events started during these windows face obstacles and delays.',
        ta: 'துர்முகூர்தம் என்பது தினசரி இரண்டு அசுப முகூர்தம் சாளரங்களின் ஒரு ஜோடி. இந்த சாளரங்களில் தொடங்கும் முக்கியமான நிகழ்வுகள் தடைகள் மற்றும் தாமதங்களை எதிர்கொள்கின்றன.',
      },
    );
  }
}

export const DOSHA_RULES = () => [
  new RahuKalamRule(),
  new YamagandamRule(),
  new KuligaiRule(),
  new VarjyamRule(),
  new PanchakaRule(),
  new GuruVenusCombustRule(),
  new SankrantiRule(),
  new DurmuhurthamRule(),
];
