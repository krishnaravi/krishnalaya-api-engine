export type ImpactType = 'positive' | 'negative' | 'neutral';
export type StarRating = 1 | 2 | 3 | 4 | 5;
export type NakshatraType = 'fixed' | 'soft' | 'sharp' | 'movable' | 'fierce' | 'mixed' | 'swift';
export type PakshaType = 'shukla' | 'krishna';

export interface BilingualText {
  en: string;
  ta: string;
}

export interface RuleResult {
  ruleName: string;
  impact: ImpactType;
  weight: number;
  contributedScore: number;
  reason: BilingualText;
  details?: BilingualText;
}

export interface TithiData {
  number: number;
  name: string;
  nameTa: string;
  paksha: PakshaType;
  quality: 'auspicious' | 'inauspicious' | 'neutral';
}

export interface NakshatraData {
  number: number;
  name: string;
  nameTa: string;
  type: NakshatraType;
  lord: string;
  lordTa: string;
  degree: number;
}

export interface YogaData {
  number: number;
  name: string;
  nameTa: string;
  quality: 'good' | 'bad' | 'neutral';
}

export interface KaranaData {
  number: number;
  name: string;
  nameTa: string;
  quality: 'good' | 'bad' | 'neutral';
}

export interface VaaraData {
  number: number;
  name: string;
  nameTa: string;
  lord: string;
  lordTa: string;
}

export interface HoraData {
  planet: string;
  planetTa: string;
  quality: 'benefic' | 'malefic' | 'neutral';
}

export interface TimePeriod {
  start: string;
  end: string;
  isActive: boolean;
}

export interface LagnaData {
  sign: number;
  name: string;
  nameTa: string;
  lord: string;
}

export interface PanchangData {
  tithi: TithiData;
  nakshatra: NakshatraData;
  yoga: YogaData;
  karana: KaranaData;
  vaara: VaaraData;
  hora: HoraData;
  rahuKalam: TimePeriod;
  yamagandam: TimePeriod;
  kuligai: TimePeriod;
  abhijitMuhurtha: TimePeriod;
  moonLongitude: number;
  sunLongitude: number;
  lagna: LagnaData;
  chandrashtama: boolean;
  taraBalance: 'favorable' | 'unfavorable' | 'neutral';
}

export interface MuhurthaSearchInput {
  date: string;
  time: string;
  latitude: number;
  longitude: number;
  timezone: string;
  category: string;
  birthNakshatra?: string;
}

export interface MuhurthaWindow {
  startTime: string;
  endTime: string;
  score: number;
  stars: StarRating;
  label: BilingualText;
  type: 'suitable' | 'avoid' | 'neutral';
}

export interface MuhurthaResult {
  requestId: string;
  category: string;
  categoryNameTa: string;
  date: string;
  time: string;
  score: number;
  stars: StarRating;
  starDisplay: string;
  verdict: BilingualText;
  panchang: PanchangData;
  windows: MuhurthaWindow[];
  positiveFactors: BilingualText[];
  negativeFactors: BilingualText[];
  ruleResults: RuleResult[];
  suitableTimes: string[];
  avoidTimes: string[];
  generatedAt: string;
}

export interface CategoryDefinition {
  id: string;
  name: string;
  nameTa: string;
  description: string;
  descriptionTa: string;
  goodTithis: number[];
  badTithis: number[];
  goodNakshatras: number[];
  badNakshatras: number[];
  goodDays: number[];
  badDays: number[];
  requiresLagnaCheck: boolean;
  avoidCombust: boolean;
  avoidEclipse: boolean;
}
