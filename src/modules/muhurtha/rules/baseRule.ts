import type { RuleResult, PanchangData } from '../../../types/muhurtha.types';
import type { CategoryDefinition } from '../../../types/muhurtha.types';

export interface IMuhurthaRule {
  readonly ruleName: string;
  readonly weight: number;
  readonly description: string;

  execute(panchang: PanchangData, category: CategoryDefinition): RuleResult;
}

export abstract class BaseRule implements IMuhurthaRule {
  abstract readonly ruleName: string;
  abstract readonly weight: number;
  abstract readonly description: string;

  abstract execute(panchang: PanchangData, category: CategoryDefinition): RuleResult;

  protected buildPositiveResult(
    reason: { en: string; ta: string },
    strengthPercent = 100,
    details?: { en: string; ta: string },
  ): RuleResult {
    return {
      ruleName: this.ruleName,
      impact: 'positive',
      weight: this.weight,
      contributedScore: Math.round((strengthPercent / 100) * 100),
      reason,
      details,
    };
  }

  protected buildNegativeResult(
    reason: { en: string; ta: string },
    strengthPercent = 100,
    details?: { en: string; ta: string },
  ): RuleResult {
    return {
      ruleName: this.ruleName,
      impact: 'negative',
      weight: this.weight,
      contributedScore: Math.round((strengthPercent / 100) * 100),
      reason,
      details,
    };
  }

  protected buildNeutralResult(
    reason: { en: string; ta: string },
    details?: { en: string; ta: string },
  ): RuleResult {
    return {
      ruleName: this.ruleName,
      impact: 'neutral',
      weight: this.weight,
      contributedScore: 50,
      reason,
      details,
    };
  }
}

export function createRuleRegistry(rules: IMuhurthaRule[]): Map<string, IMuhurthaRule> {
  const registry = new Map<string, IMuhurthaRule>();
  for (const rule of rules) {
    if (registry.has(rule.ruleName)) {
      throw new Error(`Duplicate rule name detected: "${rule.ruleName}"`);
    }
    registry.set(rule.ruleName, rule);
  }
  return registry;
}

export function executeAllRules(
  rules: IMuhurthaRule[],
  panchang: PanchangData,
  category: CategoryDefinition,
): RuleResult[] {
  return rules.map((rule) => {
    try {
      return rule.execute(panchang, category);
    } catch (err) {
      return {
        ruleName: rule.ruleName,
        impact: 'neutral',
        weight: rule.weight,
        contributedScore: 50,
        reason: {
          en: `Rule "${rule.ruleName}" evaluation failed: ${(err as Error).message}`,
          ta: `"${rule.ruleName}" விதி மதிப்பீடு தோல்வியடைந்தது: ${(err as Error).message}`,
        },
      };
    }
  });
}
