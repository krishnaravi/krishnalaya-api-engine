export interface CategoryItem {
  id: string;
  name: string;
  nameTa: string;
  description: string;
  descriptionTa: string;
}

export interface BilingualText {
  en: string;
  ta: string;
}

export interface TimePeriod {
  start: string;
  end: string;
  isActive: boolean;
}

export interface TithiInfo {
  number: number;
  name: string;
  nameTa: string;
  paksha: string;
  quality: string;
}

export interface NakshatraInfo {
  number: number;
  name: string;
  nameTa: string;
  type: string;
  lord: string;
  lordTa: string;
  degree: number;
}

export interface PanchangInfo {
  tithi: TithiInfo;
  nakshatra: NakshatraInfo;
  yoga: { number: number; name: string; nameTa: string; quality: string };
  karana: { number: number; name: string; nameTa: string; quality: string };
  vaara: { number: number; name: string; nameTa: string; lord: string };
  hora: { planet: string; planetTa: string; quality: string };
  rahuKalam: TimePeriod;
  yamagandam: TimePeriod;
  kuligai: TimePeriod;
  abhijitMuhurtha: TimePeriod;
  moonLongitude: number;
  sunLongitude: number;
  lagna: { sign: number; name: string; nameTa: string; lord: string };
  chandrashtama: boolean;
  taraBalance: string;
}

export interface MuhurthaWindow {
  startTime: string;
  endTime: string;
  score: number;
  stars: number;
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
  stars: 1 | 2 | 3 | 4 | 5;
  starDisplay: string;
  verdict: BilingualText;
  panchang: PanchangInfo;
  windows: MuhurthaWindow[];
  positiveFactors: BilingualText[];
  negativeFactors: BilingualText[];
  suitableTimes: string[];
  avoidTimes: string[];
  generatedAt: string;
}

export interface SearchFormValues {
  date: string;
  time: string;
  latitude: string;
  longitude: string;
  timezone: string;
  category: string;
  birthNakshatra: string;
}

export type Language = 'en' | 'ta';
