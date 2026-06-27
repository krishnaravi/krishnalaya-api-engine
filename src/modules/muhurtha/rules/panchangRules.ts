import type { PanchangData } from '../../../types/muhurtha.types';
import type { CategoryDefinition } from '../../../types/muhurtha.types';
import type { RuleResult } from '../../../types/muhurtha.types';
import { BaseRule } from './baseRule';

export class TithiRule extends BaseRule {
  readonly ruleName = 'Tithi';
  readonly weight = 18;
  readonly description = 'Evaluates the lunar day (Tithi) auspiciousness for the selected category';

  execute(panchang: PanchangData, category: CategoryDefinition): RuleResult {
    const { tithi } = panchang;
    const tithiNum = tithi.number > 15 ? tithi.number - 15 : tithi.number;

    if (category.goodTithis.includes(tithiNum) || category.goodTithis.includes(tithi.number)) {
      return this.buildPositiveResult(
        {
          en: `${tithi.name} (Tithi ${tithi.number}) is an auspicious lunar day for ${category.name}`,
          ta: `${tithi.nameTa} (திதி ${tithi.number}) ${category.nameTa}க்கு சுப திதி ஆகும்`,
        },
        90,
        {
          en: `Tithi ${tithi.number} falls in ${tithi.paksha === 'shukla' ? 'Shukla Paksha (waxing moon)' : 'Krishna Paksha (waning moon)'} which is ${tithi.quality}.`,
          ta: `திதி ${tithi.number} ${tithi.paksha === 'shukla' ? 'சுக்ல பட்சம் (வளர்பிறை)' : 'கிருஷ்ண பட்சம் (தேய்பிறை)'}ல் வருகிறது, இது ${tithi.quality === 'auspicious' ? 'சுபமானது' : 'நடுநிலையானது'}.`,
        },
      );
    }

    if (category.badTithis.includes(tithiNum) || category.badTithis.includes(tithi.number)) {
      const isAmavasya = tithi.number === 30 || tithiNum === 30;
      const isChaturdashi = tithiNum === 14;
      let strength = 80;
      if (isAmavasya) strength = 100;
      if (isChaturdashi) strength = 90;

      return this.buildNegativeResult(
        {
          en: `${tithi.name} (Tithi ${tithi.number}) is inauspicious for ${category.name}${isAmavasya ? ' — Amavasya (New Moon) is strictly avoided' : ''}`,
          ta: `${tithi.nameTa} (திதி ${tithi.number}) ${category.nameTa}க்கு அசுபமான திதி ஆகும்${isAmavasya ? ' — அமாவாசை கண்டிப்பாக தவிர்க்கப்படுகிறது' : ''}`,
        },
        strength,
        {
          en: `This Tithi carries negative vibrations for ${category.name}. Traditional Vedic texts advise against performing this ceremony on ${tithi.name}.`,
          ta: `இந்த திதி ${category.nameTa}க்கு எதிர்மறை அதிர்வுகளை கொண்டுள்ளது. பாரம்பரிய வேத நூல்கள் ${tithi.nameTa}யில் இந்த சடங்கை செய்வதை அறிவுறுத்தவில்லை.`,
        },
      );
    }

    return this.buildNeutralResult(
      {
        en: `${tithi.name} (Tithi ${tithi.number}) is a neutral lunar day — neither specifically auspicious nor inauspicious for ${category.name}`,
        ta: `${tithi.nameTa} (திதி ${tithi.number}) ஒரு நடுநிலை திதி — ${category.nameTa}க்கு குறிப்பாக சுபமும் இல்லை, அசுபமும் இல்லை`,
      },
    );
  }
}

export class NakshatraRule extends BaseRule {
  readonly ruleName = 'Nakshatra';
  readonly weight = 22;
  readonly description = 'Evaluates Moon nakshatra suitability for the selected category';

  execute(panchang: PanchangData, category: CategoryDefinition): RuleResult {
    const { nakshatra } = panchang;

    if (category.goodNakshatras.includes(nakshatra.number)) {
      const isHighlyAuspicious = [4, 7, 8, 12, 13, 27].includes(nakshatra.number);
      return this.buildPositiveResult(
        {
          en: `${nakshatra.name} nakshatra is ${isHighlyAuspicious ? 'highly ' : ''}auspicious for ${category.name}`,
          ta: `${nakshatra.nameTa} நட்சத்திரம் ${category.nameTa}க்கு ${isHighlyAuspicious ? 'மிகவும் ' : ''}சுபமானது`,
        },
        isHighlyAuspicious ? 95 : 80,
        {
          en: `${nakshatra.name} is a ${nakshatra.type} nakshatra ruled by ${nakshatra.lord}. Its energy harmonizes well with ${category.name} activities.`,
          ta: `${nakshatra.nameTa} ஒரு ${this.translateType(nakshatra.type)} நட்சத்திரம், ${nakshatra.lordTa} ஆதிபத்தியம். இதன் ஆற்றல் ${category.nameTa} செயல்பாடுகளுடன் நன்றாக ஒத்துப்போகிறது.`,
        },
      );
    }

    if (category.badNakshatras.includes(nakshatra.number)) {
      const isCritical = [6, 9, 18, 19].includes(nakshatra.number);
      return this.buildNegativeResult(
        {
          en: `${nakshatra.name} nakshatra is ${isCritical ? 'strongly ' : ''}inauspicious for ${category.name}`,
          ta: `${nakshatra.nameTa} நட்சத்திரம் ${category.nameTa}க்கு ${isCritical ? 'மிகவும் ' : ''}அசுபமானது`,
        },
        isCritical ? 95 : 75,
        {
          en: `${nakshatra.name} is a ${nakshatra.type} nakshatra. Its ${isCritical ? 'sharp, malefic' : 'fierce'} nature creates obstacles for ${category.name}.`,
          ta: `${nakshatra.nameTa} ஒரு ${this.translateType(nakshatra.type)} நட்சத்திரம். இதன் ${isCritical ? 'கூரிய, தீய' : 'கோரமான'} தன்மை ${category.nameTa}க்கு தடைகளை உருவாக்குகிறது.`,
        },
      );
    }

    return this.buildNeutralResult({
      en: `${nakshatra.name} nakshatra has a neutral influence on ${category.name}`,
      ta: `${nakshatra.nameTa} நட்சத்திரம் ${category.nameTa}ல் நடுநிலை செல்வாக்கு கொண்டுள்ளது`,
    });
  }

  private translateType(type: string): string {
    const map: Record<string, string> = {
      fixed: 'நிலையான (ஸ்திர)',
      soft: 'மிருதுவான (மிருது)',
      sharp: 'கூரிய (திட்சண)',
      movable: 'நகரும் (சர)',
      fierce: 'கோரமான (உக்ர)',
      mixed: 'கலப்பான (சாதாரண)',
      swift: 'விரைவான (க்ஷிப்ர)',
    };
    return map[type] ?? type;
  }
}

export class YogaRule extends BaseRule {
  readonly ruleName = 'Yoga';
  readonly weight = 12;
  readonly description = 'Evaluates the Yoga (Sun+Moon combination) for the day';

  execute(panchang: PanchangData, _category: CategoryDefinition): RuleResult {
    const { yoga } = panchang;

    const highlyGoodYogas = [2, 3, 4, 5, 7, 8, 11, 12, 14, 16, 20, 21, 22, 23, 24, 25, 26];
    const highlyBadYogas = [1, 6, 9, 10, 13, 15, 17, 19, 27];

    if (highlyGoodYogas.includes(yoga.number)) {
      const isPrime = [16, 21, 22, 23].includes(yoga.number);
      return this.buildPositiveResult(
        {
          en: `${yoga.name} Yoga is ${isPrime ? 'an excellent' : 'a favorable'} yoga that enhances all auspicious activities`,
          ta: `${yoga.nameTa} யோகம் அனைத்து சுப செயல்பாடுகளையும் மேம்படுத்தும் ${isPrime ? 'சிறந்த' : 'சாதகமான'} யோகம்`,
        },
        isPrime ? 95 : 80,
        {
          en: `${yoga.name} (Yoga ${yoga.number}) is formed by the combined influence of Sun and Moon longitudes. This yoga promotes success and harmony.`,
          ta: `${yoga.nameTa} (யோகம் ${yoga.number}) சூரிய மற்றும் சந்திர தீர்க்கரேகைகளின் கூட்டு செல்வாக்கால் உருவாகிறது. இந்த யோகம் வெற்றி மற்றும் நல்லிணக்கத்தை ஊக்குவிக்கிறது.`,
        },
      );
    }

    if (highlyBadYogas.includes(yoga.number)) {
      const isCritical = [1, 17, 19, 27].includes(yoga.number);
      return this.buildNegativeResult(
        {
          en: `${yoga.name} Yoga is ${isCritical ? 'a highly malefic' : 'an inauspicious'} yoga — activities may face obstacles`,
          ta: `${yoga.nameTa} யோகம் ${isCritical ? 'மிகவும் தீமையான' : 'அசுபமான'} யோகம் — செயல்பாடுகளில் தடைகள் ஏற்படலாம்`,
        },
        isCritical ? 90 : 70,
        {
          en: `${yoga.name} is traditionally classified as a malefic yoga in Vedic astrology. It is best to postpone important ceremonies if possible.`,
          ta: `${yoga.nameTa} வேத ஜோதிடத்தில் பாரம்பரியமாக தீய யோகமாக வகைப்படுத்தப்படுகிறது. முடிந்தால் முக்கியமான சடங்குகளை ஒத்திடுவது சிறந்தது.`,
        },
      );
    }

    return this.buildNeutralResult({
      en: `${yoga.name} Yoga has a neutral to mildly favorable influence`,
      ta: `${yoga.nameTa} யோகம் நடுநிலையிலிருந்து லேசாக சாதகமான செல்வாக்கு கொண்டுள்ளது`,
    });
  }
}

export class KaranaRule extends BaseRule {
  readonly ruleName = 'Karana';
  readonly weight = 8;
  readonly description = 'Evaluates the Karana (half-tithi) for the time period';

  execute(panchang: PanchangData, _category: CategoryDefinition): RuleResult {
    const { karana } = panchang;

    if (karana.name === 'Vishti') {
      return this.buildNegativeResult(
        {
          en: 'Vishti (Bhadra) Karana is active — this is one of the most inauspicious karanas; all auspicious work should be strictly avoided',
          ta: 'விஷ்டி (பத்ரா) கரணம் செயலில் உள்ளது — இது மிகவும் அசுபமான கரணங்களில் ஒன்று; அனைத்து சுப பணிகளையும் கண்டிப்பாக தவிர்க்க வேண்டும்',
        },
        100,
        {
          en: 'Vishti Karana (also called Bhadra) is classically regarded as highly malefic. Even minor auspicious events are traditionally postponed during this period.',
          ta: 'விஷ்டி கரணம் (பத்ராவும் என்றும் அழைக்கப்படுகிறது) பாரம்பரியமாக மிகவும் தீமையானதாக கருதப்படுகிறது. இந்த காலகட்டத்தில் சிறிய சுப நிகழ்வுகளும் ஒத்திடப்படுகின்றன.',
        },
      );
    }

    if (karana.quality === 'good') {
      const isExcellent = ['Bava', 'Balava', 'Kaulava', 'Vanija'].includes(karana.name);
      return this.buildPositiveResult(
        {
          en: `${karana.name} Karana is ${isExcellent ? 'an excellent' : 'a favorable'} half-tithi period for auspicious activities`,
          ta: `${karana.nameTa} கரணம் சுப செயல்பாடுகளுக்கு ${isExcellent ? 'சிறந்த' : 'சாதகமான'} அரை-திதி காலம்`,
        },
        isExcellent ? 85 : 70,
      );
    }

    if (karana.quality === 'bad') {
      return this.buildNegativeResult(
        {
          en: `${karana.name} Karana is inauspicious — carries restrictive energy for important events`,
          ta: `${karana.nameTa} கரணம் அசுபமானது — முக்கியமான நிகழ்வுகளுக்கு கட்டுப்படுத்தும் ஆற்றலை கொண்டுள்ளது`,
        },
        65,
      );
    }

    return this.buildNeutralResult({
      en: `${karana.name} Karana has a neutral influence on activities`,
      ta: `${karana.nameTa} கரணம் செயல்பாடுகளில் நடுநிலை செல்வாக்கு கொண்டுள்ளது`,
    });
  }
}

export class VaaraRule extends BaseRule {
  readonly ruleName = 'Vaara';
  readonly weight = 14;
  readonly description = 'Evaluates the day of the week (Vaara) and its planetary lord';

  execute(panchang: PanchangData, category: CategoryDefinition): RuleResult {
    const { vaara } = panchang;

    if (category.goodDays.includes(vaara.number)) {
      const isGuru = vaara.number === 4;
      const isShukra = vaara.number === 5;
      let strength = 75;
      if (isGuru) strength = 95;
      if (isShukra) strength = 88;

      const special = isGuru
        ? 'Guru (Jupiter) rules Thursday, making it the most auspicious day for all sacred activities'
        : isShukra
          ? 'Shukra (Venus) rules Friday, ideal for marriage and harmonious events'
          : '';

      return this.buildPositiveResult(
        {
          en: `${vaara.name} (${vaara.lord}'s day) is auspicious for ${category.name}${special ? ` — ${special}` : ''}`,
          ta: `${vaara.nameTa} (${vaara.lordTa}ன் நாள்) ${category.nameTa}க்கு சுபமானது${special ? ` — ${vaara.number === 4 ? 'குரு (வியாழன்) வியாழக்கிழமையை ஆட்சி செய்கிறார், இது அனைத்து புனித செயல்பாடுகளுக்கும் மிகவும் சுப நாளாகும்' : 'சுக்கிரன் (வெள்ளி) வெள்ளிக்கிழமையை ஆட்சி செய்கிறார், திருமணம் மற்றும் நல்லிணக்க நிகழ்வுகளுக்கு ஏற்றது'}` : ''}`,
        },
        strength,
      );
    }

    if (category.badDays.includes(vaara.number)) {
      const isSani = vaara.number === 6;
      const isMangal = vaara.number === 2;
      let strength = 75;
      if (isSani) strength = 85;
      if (isMangal) strength = 90;

      return this.buildNegativeResult(
        {
          en: `${vaara.name} (${vaara.lord}'s day) is inauspicious for ${category.name}${isMangal ? ' — Mars rules Tuesday, which carries aggressive energy unsuitable for auspicious rites' : isSani ? ' — Saturn rules Saturday, creating delays and obstacles' : ''}`,
          ta: `${vaara.nameTa} (${vaara.lordTa}ன் நாள்) ${category.nameTa}க்கு அசுபமானது${isMangal ? ' — செவ்வாய் செவ்வாய்க்கிழமையை ஆட்சி செய்கிறார், இது சுப சடங்குகளுக்கு பொருத்தமற்ற ஆக்ரோஷமான ஆற்றலை கொண்டுள்ளது' : isSani ? ' — சனி சனிக்கிழமையை ஆட்சி செய்கிறார், தாமதங்களும் தடைகளும் உருவாக்குகிறார்' : ''}`,
        },
        strength,
      );
    }

    return this.buildNeutralResult({
      en: `${vaara.name} (${vaara.lord}'s day) is a neutral day for ${category.name}`,
      ta: `${vaara.nameTa} (${vaara.lordTa}ன் நாள்) ${category.nameTa}க்கு நடுநிலை நாளாகும்`,
    });
  }
}

export class HoraRule extends BaseRule {
  readonly ruleName = 'Hora';
  readonly weight = 8;
  readonly description = 'Evaluates the planetary hour (Hora) at the requested time';

  execute(panchang: PanchangData, _category: CategoryDefinition): RuleResult {
    const { hora } = panchang;

    if (hora.quality === 'benefic') {
      const isJupiterOrVenus = ['Jupiter', 'Venus'].includes(hora.planet);
      return this.buildPositiveResult(
        {
          en: `${hora.planet} Hora is active — a benefic planetary hour favoring positive outcomes`,
          ta: `${hora.planetTa} ஹோரை செயலில் உள்ளது — சாதகமான கிரக நேரம், நேர்மறையான முடிவுகளை ஆதரிக்கிறது`,
        },
        isJupiterOrVenus ? 90 : 75,
        {
          en: `During ${hora.planet} Hora, the cosmic energy is aligned with ${hora.planet}'s qualities of ${hora.planet === 'Jupiter' ? 'wisdom, expansion, and blessings' : hora.planet === 'Venus' ? 'love, beauty, and harmony' : hora.planet === 'Moon' ? 'emotions, intuition, and fertility' : 'communication and intelligence'}.`,
          ta: `${hora.planetTa} ஹோரையில், ${hora.planet === 'Jupiter' ? 'ஞானம், விரிவாக்கம் மற்றும் ஆசீர்வாதங்கள்' : hora.planet === 'Venus' ? 'அன்பு, அழகு மற்றும் நல்லிணக்கம்' : 'உணர்வுகள் மற்றும் உள்ளுணர்வு'} போன்ற பண்புகளுடன் பிரபஞ்ச ஆற்றல் சீரமைக்கப்பட்டுள்ளது.`,
        },
      );
    }

    if (hora.quality === 'malefic') {
      return this.buildNegativeResult(
        {
          en: `${hora.planet} Hora is active — a malefic planetary hour; timing may create friction for auspicious events`,
          ta: `${hora.planetTa} ஹோரை செயலில் உள்ளது — தீய கிரக நேரம்; நேரம் சுப நிகழ்வுகளில் உராய்வை உருவாக்கலாம்`,
        },
        70,
      );
    }

    return this.buildNeutralResult({
      en: `${hora.planet} Hora has a mixed or neutral influence during this time`,
      ta: `${hora.planetTa} ஹோரை இந்த நேரத்தில் கலவையான அல்லது நடுநிலை செல்வாக்கு கொண்டுள்ளது`,
    });
  }
}

export class AbhijitMuhurthaRule extends BaseRule {
  readonly ruleName = 'Abhijit Muhurtha';
  readonly weight = 10;
  readonly description = 'Checks if the requested time falls within the auspicious Abhijit Muhurtha window';

  execute(panchang: PanchangData, _category: CategoryDefinition): RuleResult {
    const { abhijitMuhurtha } = panchang;

    if (abhijitMuhurtha.isActive) {
      return this.buildPositiveResult(
        {
          en: `Time falls within Abhijit Muhurtha (${abhijitMuhurtha.start}–${abhijitMuhurtha.end}) — the most powerful natural muhurtha of the day that overrides minor doshas`,
          ta: `நேரம் அபிஜித் முகூர்த்தத்தில் (${abhijitMuhurtha.start}–${abhijitMuhurtha.end}) வருகிறது — சிறிய தோஷங்களை நீக்கும் நாளின் மிகவும் சக்திவாய்ந்த இயற்கை முகூர்த்தம்`,
        },
        100,
        {
          en: 'Abhijit Muhurtha occurs at midday and is considered self-sufficient in auspiciousness. Even when other elements are unfavorable, Abhijit Muhurtha grants its own blessings.',
          ta: 'அபிஜித் முகூர்த்தம் நண்பகலில் நிகழ்கிறது மற்றும் அதிர்ஷ்டத்தில் சுயமாக போதுமானதாக கருதப்படுகிறது. மற்ற கூறுகள் சாதகமாக இல்லாத போதும், அபிஜித் முகூர்த்தம் தனதே ஆசீர்வாதங்களை வழங்குகிறது.',
        },
      );
    }

    return this.buildNeutralResult({
      en: `Time is outside Abhijit Muhurtha window (${abhijitMuhurtha.start}–${abhijitMuhurtha.end})`,
      ta: `நேரம் அபிஜித் முகூர்த்த சாளரத்திற்கு வெளியே உள்ளது (${abhijitMuhurtha.start}–${abhijitMuhurtha.end})`,
    });
  }
}

export class WeekdayCompatibilityRule extends BaseRule {
  readonly ruleName = 'Weekday-Nakshatra Compatibility';
  readonly weight = 6;
  readonly description = 'Checks Vedic compatibility between the weekday and nakshatra';

  private readonly compatibilityMatrix: Record<number, number[]> = {
    0: [1, 8, 9, 12, 22, 27],
    1: [4, 7, 13, 22, 23, 24],
    2: [5, 14, 19, 20, 25],
    3: [3, 6, 9, 15, 18],
    4: [7, 16, 17, 21, 26],
    5: [2, 11, 12, 14, 27],
    6: [10, 17, 23, 24, 26],
  };

  execute(panchang: PanchangData, _category: CategoryDefinition): RuleResult {
    const dayNum = panchang.vaara.number;
    const nakshatraNum = panchang.nakshatra.number;
    const compatibleNakshatras = this.compatibilityMatrix[dayNum] ?? [];

    if (compatibleNakshatras.includes(nakshatraNum)) {
      return this.buildPositiveResult(
        {
          en: `${panchang.vaara.name} and ${panchang.nakshatra.name} form a compatible and harmonious Vedic combination`,
          ta: `${panchang.vaara.nameTa} மற்றும் ${panchang.nakshatra.nameTa} ஒரு இணக்கமான மற்றும் நல்லிணக்கமான வேத கலவையை உருவாக்குகின்றன`,
        },
        80,
      );
    }

    return this.buildNeutralResult({
      en: `${panchang.vaara.name} and ${panchang.nakshatra.name} — standard compatibility, no special synergy noted`,
      ta: `${panchang.vaara.nameTa} மற்றும் ${panchang.nakshatra.nameTa} — நிலையான இணக்கம், சிறப்பு ஒத்திசைவு இல்லை`,
    });
  }
}

export const PANCHANG_RULES: () => Array<typeof BaseRule['prototype']> = () => [
  new TithiRule(),
  new NakshatraRule(),
  new YogaRule(),
  new KaranaRule(),
  new VaaraRule(),
  new HoraRule(),
  new AbhijitMuhurthaRule(),
  new WeekdayCompatibilityRule(),
];
