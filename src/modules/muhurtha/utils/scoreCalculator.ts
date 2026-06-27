import type { RuleResult, StarRating } from '../../../types/muhurtha.types';
import { SCORE_THRESHOLDS, STAR_DISPLAY } from '../constants/muhurthaConstants';

export interface AggregatedScore {
  totalScore: number;
  normalizedScore: number;
  stars: StarRating;
  starDisplay: string;
  positiveWeight: number;
  negativeWeight: number;
  neutralWeight: number;
  breakdown: ScoreBreakdown[];
}

export interface ScoreBreakdown {
  ruleName: string;
  rawContribution: number;
  normalizedContribution: number;
  impact: 'positive' | 'negative' | 'neutral';
}

export function aggregateRuleResults(results: RuleResult[]): AggregatedScore {
  let positiveSum = 0;
  let negativeSum = 0;
  let totalWeight = 0;
  const breakdown: ScoreBreakdown[] = [];

  for (const result of results) {
    totalWeight += result.weight;
    const contribution = result.contributedScore * (result.weight / 100);

    if (result.impact === 'positive') {
      positiveSum += Math.abs(contribution);
    } else if (result.impact === 'negative') {
      negativeSum += Math.abs(contribution);
    }

    breakdown.push({
      ruleName: result.ruleName,
      rawContribution: result.contributedScore,
      normalizedContribution: contribution,
      impact: result.impact,
    });
  }

  const positiveWeight = results
    .filter((r) => r.impact === 'positive')
    .reduce((acc, r) => acc + r.weight, 0);

  const negativeWeight = results
    .filter((r) => r.impact === 'negative')
    .reduce((acc, r) => acc + r.weight, 0);

  const neutralWeight = results
    .filter((r) => r.impact === 'neutral')
    .reduce((acc, r) => acc + r.weight, 0);

  const maxPossiblePositive = totalWeight > 0 ? (positiveWeight / totalWeight) * 100 : 0;
  const baseScore = 50;
  const positiveContribution = maxPossiblePositive > 0
    ? (positiveSum / maxPossiblePositive) * 45
    : 0;
  const negativeDeduction = totalWeight > 0
    ? (negativeSum / totalWeight) * 50
    : 0;

  const rawScore = baseScore + positiveContribution - negativeDeduction;
  const normalizedScore = Math.min(100, Math.max(0, Math.round(rawScore)));

  const stars = mapScoreToStars(normalizedScore);
  const starDisplay = STAR_DISPLAY[stars];

  return {
    totalScore: Math.round(rawScore),
    normalizedScore,
    stars,
    starDisplay,
    positiveWeight,
    negativeWeight,
    neutralWeight,
    breakdown,
  };
}

export function mapScoreToStars(score: number): StarRating {
  if (score >= SCORE_THRESHOLDS.FIVE_STAR) return 5;
  if (score >= SCORE_THRESHOLDS.FOUR_STAR) return 4;
  if (score >= SCORE_THRESHOLDS.THREE_STAR) return 3;
  if (score >= SCORE_THRESHOLDS.TWO_STAR) return 2;
  return 1;
}

export function generateVerdict(score: number): { en: string; ta: string } {
  if (score >= SCORE_THRESHOLDS.FIVE_STAR) {
    return {
      en: 'Highly Auspicious — Excellent muhurtha for proceeding with full confidence',
      ta: 'மிகவும் சுப முகூர்த்தம் — முழு நம்பிக்கையுடன் தொடர சிறந்த முகூர்த்தம்',
    };
  }
  if (score >= SCORE_THRESHOLDS.FOUR_STAR) {
    return {
      en: 'Auspicious — Good muhurtha with minor cautionary factors',
      ta: 'சுப முகூர்த்தம் — சிறிய எச்சரிக்கை காரணிகளுடன் நல்ல முகூர்த்தம்',
    };
  }
  if (score >= SCORE_THRESHOLDS.THREE_STAR) {
    return {
      en: 'Moderate — Average muhurtha, proceed with precautions',
      ta: 'மிதமான முகூர்த்தம் — சராசரி முகூர்த்தம், எச்சரிக்கையுடன் தொடரவும்',
    };
  }
  if (score >= SCORE_THRESHOLDS.TWO_STAR) {
    return {
      en: 'Inauspicious — Several doshas present; consider alternative timing',
      ta: 'அசுப முகூர்த்தம் — பல தோஷங்கள் உள்ளன; மாற்று நேரம் கருத்தில் கொள்ளவும்',
    };
  }
  return {
    en: 'Highly Inauspicious — Strong doshas; strongly recommended to avoid this time',
    ta: 'மிகவும் அசுப முகூர்த்தம் — வலுவான தோஷங்கள்; இந்த நேரத்தை தவிர்க்க கட்டாயமாக பரிந்துரைக்கப்படுகிறது',
  };
}

export function calculateRuleContributedScore(
  isPositive: boolean,
  strength: number,
  maxScore = 100,
): number {
  const clamped = Math.min(100, Math.max(0, strength));
  return isPositive ? (clamped / 100) * maxScore : (clamped / 100) * maxScore;
}

export function weightedAverage(
  values: Array<{ value: number; weight: number }>,
): number {
  const totalWeight = values.reduce((sum, v) => sum + v.weight, 0);
  if (totalWeight === 0) return 0;
  const weightedSum = values.reduce((sum, v) => sum + v.value * v.weight, 0);
  return weightedSum / totalWeight;
}
