import type { PanchangData } from '../../../types/muhurtha.types';
import type { CategoryDefinition } from '../../../types/muhurtha.types';
import { BaseRule } from './baseRule';

export class TaraBalaTaraRule extends BaseRule {
  readonly ruleName = 'Tara Bala';
  readonly weight = 12;
  readonly description = 'Evaluates Tara Bala (lunar mansion strength relative to birth star)';

  execute(panchang: PanchangData, _category: CategoryDefinition) {
    const { taraBalance } = panchang;

    if (taraBalance === 'favorable') {
      return this.buildPositiveResult(
        {
          en: `Tara Bala is favorable — the Moon's nakshatra is in a positive Tara position relative to the birth star, enhancing personal luck and vitality`,
          ta: `தார பலம் சாதகமாக உள்ளது — சந்திரனின் நட்சத்திரம் பிறப்பு நட்சத்திரத்தை தொடர்பாக நேர்மறையான தார நிலையில் உள்ளது, தனிப்பட்ட அதிர்ஷ்டம் மற்றும் உயிர்த்தன்மையை மேம்படுத்துகிறது`,
        },
        88,
        {
          en: 'Tara Bala is calculated by counting the nakshatras from the birth star to the current moon nakshatra. Favorable Tara positions (Janma, Sampat, Kshema, Sadhana, Mitra, Parama Mitra) indicate personal harmony.',
          ta: 'தார பலம் பிறப்பு நட்சத்திரத்திலிருந்து தற்போதைய சந்திர நட்சத்திரம் வரை நட்சத்திரங்களை எண்ணுவதன் மூலம் கணக்கிடப்படுகிறது. சாதகமான தார நிலைகள் (ஜன்மா, சம்பத், க்ஷேம, சாதன, மித்ர, பரம மித்ர) தனிப்பட்ட நல்லிணக்கத்தை குறிக்கின்றன.',
        },
      );
    }

    if (taraBalance === 'unfavorable') {
      return this.buildNegativeResult(
        {
          en: 'Tara Bala is unfavorable — the Moon is in an adverse Tara position (Vipat, Pratyak, or Naidhana) creating personal obstacles',
          ta: 'தார பலம் சாதகமற்றது — சந்திரன் ஒரு எதிர்மறையான தார நிலையில் (விபத், பிரத்யக் அல்லது நைதன) உள்ளது, தனிப்பட்ட தடைகளை உருவாக்குகிறது',
        },
        82,
        {
          en: 'Naidhana (9th position) is the most severe adverse Tara. Vipat (3rd) and Pratyak (5th) also create challenges. A Puja or Tara Shanti can mitigate this.',
          ta: 'நைதன (9வது நிலை) மிகவும் கடுமையான எதிர்மறை தாரா. விபத் (3வது) மற்றும் பிரத்யக் (5வது) சவால்களையும் உருவாக்குகின்றன. ஒரு பூஜை அல்லது தார சாந்தி இதை குறைக்கலாம்.',
        },
      );
    }

    return this.buildNeutralResult({
      en: 'Tara Bala is neutral — moderate personal support for the muhurtha (birth nakshatra not provided for precise calculation)',
      ta: 'தார பலம் நடுநிலையில் உள்ளது — முகூர்த்தத்திற்கு மிதமான தனிப்பட்ட ஆதரவு (துல்லியமான கணக்கீட்டிற்கு பிறப்பு நட்சத்திரம் வழங்கப்படவில்லை)',
    });
  }
}

export class ChandraBalamRule extends BaseRule {
  readonly ruleName = 'Chandra Bala';
  readonly weight = 11;
  readonly description = 'Evaluates Moon strength (Chandra Bala) based on house position from lagna';

  execute(panchang: PanchangData, _category: CategoryDefinition) {
    const moonSign = Math.floor(panchang.moonLongitude / 30) + 1;
    const lagnaSign = panchang.lagna.sign;
    const moonFromLagna = ((moonSign - lagnaSign + 12) % 12) + 1;

    const strongPositions = [1, 3, 5, 7, 9, 11];
    const weakPositions = [6, 8, 12];

    if (strongPositions.includes(moonFromLagna)) {
      return this.buildPositiveResult(
        {
          en: `Moon is in the ${moonFromLagna}${this.ordinalSuffix(moonFromLagna)} house from Lagna — Chandra Bala is strong, bestowing emotional strength and prosperity`,
          ta: `சந்திரன் லக்னத்திலிருந்து ${moonFromLagna}வது வீட்டில் உள்ளது — சந்திர பலம் வலிமையானது, உணர்வு வலிமை மற்றும் செழிப்பை வழங்குகிறது`,
        },
        90,
        {
          en: `The Moon in the ${moonFromLagna}${this.ordinalSuffix(moonFromLagna)} house (${this.houseMeaning(moonFromLagna)}) strengthens ${this.houseTheme(moonFromLagna)} during this time.`,
          ta: `${moonFromLagna}வது வீட்டில் சந்திரன் (${this.houseMeaningTa(moonFromLagna)}) இந்த நேரத்தில் ${this.houseThemeTa(moonFromLagna)}ஐ வலுப்படுத்துகிறது.`,
        },
      );
    }

    if (weakPositions.includes(moonFromLagna)) {
      return this.buildNegativeResult(
        {
          en: `Moon is in the ${moonFromLagna}${this.ordinalSuffix(moonFromLagna)} house from Lagna — Chandra Bala is weak; emotional turbulence and obstacles possible`,
          ta: `சந்திரன் லக்னத்திலிருந்து ${moonFromLagna}வது வீட்டில் உள்ளது — சந்திர பலம் பலவீனமானது; உணர்ச்சி கொந்தளிப்பு மற்றும் தடைகள் சாத்தியம்`,
        },
        80,
      );
    }

    return this.buildNeutralResult({
      en: `Moon is in the ${moonFromLagna}${this.ordinalSuffix(moonFromLagna)} house from Lagna — Chandra Bala is moderate`,
      ta: `சந்திரன் லக்னத்திலிருந்து ${moonFromLagna}வது வீட்டில் உள்ளது — சந்திர பலம் மிதமானது`,
    });
  }

  private ordinalSuffix(n: number): string {
    if (n === 1) return 'st';
    if (n === 2) return 'nd';
    if (n === 3) return 'rd';
    return 'th';
  }

  private houseMeaning(n: number): string {
    const m: Record<number, string> = {
      1: 'Ascendant/Self', 3: 'Courage & Siblings', 5: 'Intelligence & Children',
      7: 'Partnership', 9: 'Fortune & Dharma', 11: 'Gains & Fulfillment',
      6: 'Enemies & Disease', 8: 'Obstacles & Hidden', 12: 'Loss & Sacrifice',
    };
    return m[n] ?? 'Standard Position';
  }

  private houseMeaningTa(n: number): string {
    const m: Record<number, string> = {
      1: 'லக்னம்/சுயம்', 3: 'தைரியம் & சகோதரர்கள்', 5: 'அறிவு & குழந்தைகள்',
      7: 'கூட்டாண்மை', 9: 'அதிர்ஷ்டம் & தர்மம்', 11: 'ஆதாயங்கள் & நிறைவேற்றம்',
      6: 'எதிரிகள் & நோய்', 8: 'தடைகள் & மறைந்தவை', 12: 'இழப்பு & தியாகம்',
    };
    return m[n] ?? 'நிலையான நிலை';
  }

  private houseTheme(n: number): string {
    const m: Record<number, string> = {
      1: 'self-confidence and personal power', 3: 'determination and courage',
      5: 'wisdom and creative abilities', 7: 'partnerships and harmonious bonds',
      9: 'dharma, luck, and blessings from elders', 11: 'material gains and wish fulfillment',
    };
    return m[n] ?? 'general well-being';
  }

  private houseThemeTa(n: number): string {
    const m: Record<number, string> = {
      1: 'தன்னம்பிக்கை மற்றும் தனிப்பட்ட சக்தி', 3: 'உறுதிப்பாடு மற்றும் தைரியம்',
      5: 'ஞானம் மற்றும் படைப்புத் திறன்கள்', 7: 'கூட்டாண்மை மற்றும் நல்லிணக்க பந்தங்கள்',
      9: 'தர்மம், அதிர்ஷ்டம் மற்றும் பெரியவர்களின் ஆசீர்வாதங்கள்', 11: 'பொருள் ஆதாயங்கள் மற்றும் ஆசை நிறைவேற்றம்',
    };
    return m[n] ?? 'பொது நலன்';
  }
}

export class ChandrashtamaRule extends BaseRule {
  readonly ruleName = 'Chandrashtama';
  readonly weight = 13;
  readonly description = 'Detects Chandrashtama dosha (Moon in 8th house from birth nakshatra rashi)';

  execute(panchang: PanchangData, _category: CategoryDefinition) {
    if (panchang.chandrashtama) {
      return this.buildNegativeResult(
        {
          en: 'CHANDRASHTAMA DOSHA: Moon is in the 8th sign from the birth nakshatra sign — this creates significant mental stress and is strictly avoided for all auspicious events',
          ta: 'சந்திராஷ்டம தோஷம்: பிறப்பு நட்சத்திர ராசியிலிருந்து 8வது ராசியில் சந்திரன் உள்ளது — இது குறிப்பிடத்தக்க மனச்சிரமத்தை உருவாக்குகிறது மற்றும் அனைத்து சுப நிகழ்வுகளுக்கும் கண்டிப்பாக தவிர்க்கப்படுகிறது',
        },
        100,
        {
          en: 'Chandrashtama occurs when the Moon transits the 8th house from the Janma Rashi (birth sign). During this 2.5-day period, one experiences heightened anxiety, poor decision-making, and unstable emotions. All important ceremonies should be postponed.',
          ta: 'ஜன்ம ராசியிலிருந்து (பிறப்பு ராசி) 8வது வீட்டில் சந்திரன் நடமாடும் போது சந்திராஷ்டமம் நிகழ்கிறது. இந்த 2.5 நாள் காலகட்டத்தில், கவலை அதிகரிப்பு, மோசமான முடிவெடுப்பு மற்றும் நிலையற்ற உணர்வுகளை அனுபவிக்கிறார். அனைத்து முக்கியமான சடங்குகளும் ஒத்திடப்படுவது சிறந்தது.',
        },
      );
    }

    return this.buildPositiveResult(
      {
        en: 'No Chandrashtama — Moon is in a harmonious position relative to the birth sign, supporting stable emotions and clear judgment',
        ta: 'சந்திராஷ்டமம் இல்லை — பிறப்பு ராசியை தொடர்பாக சந்திரன் நல்லிணக்கமான நிலையில் உள்ளது, நிலையான உணர்வுகளையும் தெளிவான தீர்ப்பையும் ஆதரிக்கிறது',
      },
      85,
    );
  }
}

export class LagnaStrengthRule extends BaseRule {
  readonly ruleName = 'Lagna Strength';
  readonly weight = 10;
  readonly description = 'Evaluates the strength and auspiciousness of the rising sign (Lagna)';

  private readonly beneficLagnas = [1, 2, 4, 5, 7, 9, 11, 12];
  private readonly maleficLagnas = [3, 6, 8, 10];

  execute(panchang: PanchangData, category: CategoryDefinition) {
    if (!category.requiresLagnaCheck) {
      return this.buildNeutralResult({
        en: `Lagna check not required for ${category.name}`,
        ta: `${category.nameTa}க்கு லக்ன சரிபார்ப்பு தேவையில்லை`,
      });
    }

    const lagnaSign = panchang.lagna.sign;

    if (this.beneficLagnas.includes(lagnaSign)) {
      const isExcellent = [1, 4, 5, 9].includes(lagnaSign);
      return this.buildPositiveResult(
        {
          en: `${panchang.lagna.name} (${lagnaSign}${this.ordinalSuffix(lagnaSign)} sign) is ${isExcellent ? 'an excellent' : 'a favorable'} Lagna for ${category.name}`,
          ta: `${panchang.lagna.nameTa} (${lagnaSign}வது ராசி) ${category.nameTa}க்கு ${isExcellent ? 'சிறந்த' : 'சாதகமான'} லக்னமாகும்`,
        },
        isExcellent ? 90 : 78,
        {
          en: `${panchang.lagna.name} Lagna, ruled by ${panchang.lagna.lord}, creates a powerful and stable foundation for ${category.name} ceremonies. The rising sign sets the tone for the entire event.`,
          ta: `${panchang.lagna.nameTa} லக்னம், ${panchang.lagna.lord} ஆட்சி, ${category.nameTa} சடங்குகளுக்கு சக்திவாய்ந்த மற்றும் நிலையான அடித்தளத்தை உருவாக்குகிறது. உதிக்கும் ராசி முழு நிகழ்வின் தொனியை அமைக்கிறது.`,
        },
      );
    }

    if (this.maleficLagnas.includes(lagnaSign)) {
      return this.buildNegativeResult(
        {
          en: `${panchang.lagna.name} (${lagnaSign}${this.ordinalSuffix(lagnaSign)} sign) Lagna is inauspicious for ${category.name} — consider timing adjustment`,
          ta: `${panchang.lagna.nameTa} (${lagnaSign}வது ராசி) லக்னம் ${category.nameTa}க்கு அசுபமானது — நேரம் சரிசெய்வதை கருத்தில் கொள்ளவும்`,
        },
        80,
      );
    }

    return this.buildNeutralResult({
      en: `${panchang.lagna.name} Lagna has a neutral effect for ${category.name}`,
      ta: `${panchang.lagna.nameTa} லக்னம் ${category.nameTa}க்கு நடுநிலை விளைவை கொண்டுள்ளது`,
    });
  }

  private ordinalSuffix(n: number): string {
    const s = ['th', 'st', 'nd', 'rd'];
    const v = n % 100;
    return s[(v - 20) % 10] ?? s[v] ?? s[0];
  }
}

export class BeneficInfluenceRule extends BaseRule {
  readonly ruleName = 'Benefic Planetary Influence';
  readonly weight = 8;
  readonly description = 'Evaluates the presence and strength of benefic planets (Jupiter, Venus, Mercury, Moon)';

  execute(panchang: PanchangData, _category: CategoryDefinition) {
    const moonDeg = panchang.moonLongitude;
    const sunDeg = panchang.sunLongitude;
    const moonPhase = ((moonDeg - sunDeg + 360) % 360) / 360;
    const moonIllumination = moonPhase <= 0.5 ? moonPhase * 2 : (1 - moonPhase) * 2;
    const isWaxing = moonPhase < 0.5;
    const isNearFull = moonIllumination > 0.75;
    const isNearNew = moonIllumination < 0.2;

    if (isNearFull && isWaxing) {
      return this.buildPositiveResult(
        {
          en: 'Moon is waxing and near full — benefic lunar energy is at peak strength, flooding the muhurtha with prosperity and abundance',
          ta: 'சந்திரன் வளர்ந்துவரும் மற்றும் பௌர்ணமிக்கு அருகில் உள்ளது — சுப சந்திர ஆற்றல் உச்ச வலிமையில் உள்ளது, முகூர்த்தத்தை செழிப்பு மற்றும் வளத்துடன் நிரப்புகிறது',
        },
        92,
      );
    }

    if (isNearNew) {
      return this.buildNegativeResult(
        {
          en: 'Moon is near new moon (Amavasya) phase — lunar energy is at minimum; emotional and creative vitality is reduced',
          ta: 'சந்திரன் அமாவாசை நிலைக்கு அருகில் உள்ளது — சந்திர ஆற்றல் குறைந்தபட்சத்தில் உள்ளது; உணர்வு மற்றும் படைப்பு உயிர்த்தன்மை குறைக்கப்படுகிறது',
        },
        75,
      );
    }

    if (isWaxing) {
      return this.buildPositiveResult(
        {
          en: `Moon is in Shukla Paksha (waxing phase, ${Math.round(moonIllumination * 100)}% illuminated) — growing lunar energy supports positive endeavors`,
          ta: `சந்திரன் சுக்ல பட்சத்தில் (வளர்பிறை, ${Math.round(moonIllumination * 100)}% வளர்ந்திருக்கிறது) — வளரும் சந்திர ஆற்றல் நேர்மறையான முயற்சிகளை ஆதரிக்கிறது`,
        },
        78,
      );
    }

    return this.buildNeutralResult({
      en: `Moon is in Krishna Paksha (waning phase, ${Math.round(moonIllumination * 100)}% illuminated) — subdued lunar energy`,
      ta: `சந்திரன் கிருஷ்ண பட்சத்தில் (தேய்பிறை, ${Math.round(moonIllumination * 100)}% வளர்ந்திருக்கிறது) — மந்தமான சந்திர ஆற்றல்`,
    });
  }
}

export const STRENGTH_RULES = () => [
  new TaraBalaTaraRule(),
  new ChandraBalamRule(),
  new ChandrashtamaRule(),
  new LagnaStrengthRule(),
  new BeneficInfluenceRule(),
];
