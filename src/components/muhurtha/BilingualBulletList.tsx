import React from 'react';
import type { BilingualText, Language } from './types';

interface BilingualBulletListProps {
  positiveFactors: BilingualText[];
  negativeFactors: BilingualText[];
  language?: Language;
  showBothLanguages?: boolean;
}

function FactorBullet({
  text,
  type,
  index,
}: {
  text: BilingualText;
  type: 'positive' | 'negative';
  index: number;
  language: Language;
}) {
  const isPositive = type === 'positive';

  return (
    <li
      className={[
        'flex items-start gap-3 p-3 rounded-lg border transition-colors duration-150',
        isPositive
          ? 'bg-emerald-50 border-emerald-100 hover:bg-emerald-100'
          : 'bg-red-50 border-red-100 hover:bg-red-100',
      ].join(' ')}
      style={{ animationDelay: `${index * 50}ms` }}
    >
      <span
        className={[
          'mt-0.5 flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold',
          isPositive
            ? 'bg-emerald-500 text-white'
            : 'bg-red-500 text-white',
        ].join(' ')}
        aria-hidden="true"
      >
        {isPositive ? '✓' : '✗'}
      </span>

      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-gray-800 leading-snug">{text.en}</p>
        <p className="text-xs text-gray-600 mt-1 font-medium leading-snug">{text.ta}</p>
      </div>
    </li>
  );
}

export function BilingualBulletList({
  positiveFactors,
  negativeFactors,
  language = 'en',
  showBothLanguages = true,
}: BilingualBulletListProps) {
  const effectiveLang = showBothLanguages ? 'both' : language;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="space-y-3">
        <div className="flex items-center gap-2 mb-3">
          <div className="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center">
            <span className="text-emerald-600 text-lg font-bold">+</span>
          </div>
          <div>
            <h3 className="font-bold text-gray-800 text-sm">
              {effectiveLang === 'ta'
                ? 'சுப காரணிகள்'
                : effectiveLang === 'both'
                  ? 'Positive Factors / சுப காரணிகள்'
                  : 'Positive Factors'}
            </h3>
            <p className="text-xs text-gray-500">
              {positiveFactors.length}{' '}
              {effectiveLang === 'ta' ? 'சாதகமான அம்சங்கள்' : 'favorable aspects'}
            </p>
          </div>
        </div>

        {positiveFactors.length === 0 ? (
          <div className="flex items-center justify-center h-24 rounded-lg border-2 border-dashed border-gray-200 bg-gray-50">
            <p className="text-sm text-gray-400">
              {effectiveLang === 'ta' ? 'சுப காரணிகள் இல்லை' : 'No positive factors identified'}
            </p>
          </div>
        ) : (
          <ul className="space-y-2">
            {positiveFactors.map((factor, idx) => (
              <FactorBullet
                key={idx}
                text={factor}
                type="positive"
                index={idx}
                language={effectiveLang === 'ta' ? 'ta' : 'en'}
              />
            ))}
          </ul>
        )}
      </div>

      <div className="space-y-3">
        <div className="flex items-center gap-2 mb-3">
          <div className="w-8 h-8 rounded-full bg-red-100 flex items-center justify-center">
            <span className="text-red-600 text-lg font-bold">−</span>
          </div>
          <div>
            <h3 className="font-bold text-gray-800 text-sm">
              {effectiveLang === 'ta'
                ? 'அசுப தோஷங்கள்'
                : effectiveLang === 'both'
                  ? 'Negative Doshas / அசுப தோஷங்கள்'
                  : 'Negative Doshas'}
            </h3>
            <p className="text-xs text-gray-500">
              {negativeFactors.length}{' '}
              {effectiveLang === 'ta' ? 'எதிர்மறை அம்சங்கள்' : 'adverse factors'}
            </p>
          </div>
        </div>

        {negativeFactors.length === 0 ? (
          <div className="flex items-center justify-center h-24 rounded-lg border-2 border-dashed border-emerald-200 bg-emerald-50">
            <p className="text-sm text-emerald-600 font-medium">
              {effectiveLang === 'ta'
                ? 'தோஷங்கள் இல்லை — சுத்தமான முகூர்த்தம்!'
                : 'No doshas detected — Clean muhurtha!'}
            </p>
          </div>
        ) : (
          <ul className="space-y-2">
            {negativeFactors.map((factor, idx) => (
              <FactorBullet
                key={idx}
                text={factor}
                type="negative"
                index={idx}
                language={effectiveLang === 'ta' ? 'ta' : 'en'}
              />
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

interface Dosha {
  name: string;
  active: boolean;
  severity: 'critical' | 'moderate' | 'low';
}

interface DoshaBadgesProps {
  doshas: Dosha[];
  language?: Language;
}

export function DoshaBadges({ doshas, language = 'en' }: DoshaBadgesProps) {
  const activeDoshas = doshas.filter((d) => d.active);
  if (activeDoshas.length === 0) return null;

  const severityConfig = {
    critical: { color: 'bg-red-100 text-red-800 border-red-200', icon: '🔴' },
    moderate: { color: 'bg-orange-100 text-orange-800 border-orange-200', icon: '🟠' },
    low:      { color: 'bg-yellow-100 text-yellow-800 border-yellow-200', icon: '🟡' },
  };

  return (
    <div className="mt-4">
      <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
        {language === 'ta' ? 'செயலில் உள்ள தோஷங்கள்' : 'Active Doshas'}
      </p>
      <div className="flex flex-wrap gap-2">
        {activeDoshas.map((dosha, idx) => {
          const config = severityConfig[dosha.severity];
          return (
            <span
              key={idx}
              className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${config.color}`}
            >
              <span>{config.icon}</span>
              {dosha.name}
            </span>
          );
        })}
      </div>
    </div>
  );
}
