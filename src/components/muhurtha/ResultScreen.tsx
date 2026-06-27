import React from 'react';
import type { MuhurthaResult, MuhurthaWindow, Language } from './types';
import { BilingualBulletList } from './BilingualBulletList';

interface ScoreGaugeProps {
  score: number;
  stars: number;
  starDisplay: string;
  language?: Language;
}

function ScoreGauge({ score, stars, starDisplay, language = 'en' }: ScoreGaugeProps) {
  const isTa = language === 'ta';
  const radius = 52;
  const circumference = 2 * Math.PI * radius;
  const dashOffset = circumference - (score / 100) * circumference;

  const scoreColor =
    score >= 88 ? '#10b981' :
    score >= 72 ? '#3b82f6' :
    score >= 52 ? '#f59e0b' :
    score >= 32 ? '#f97316' :
    '#ef4444';

  const bgColor =
    score >= 88 ? 'from-emerald-50 to-emerald-100' :
    score >= 72 ? 'from-blue-50 to-blue-100' :
    score >= 52 ? 'from-amber-50 to-amber-100' :
    score >= 32 ? 'from-orange-50 to-orange-100' :
    'from-red-50 to-red-100';

  const label =
    score >= 88 ? (isTa ? 'மிகவும் சுபமானது' : 'Highly Auspicious') :
    score >= 72 ? (isTa ? 'சுபமானது' : 'Auspicious') :
    score >= 52 ? (isTa ? 'சராசரி' : 'Moderate') :
    score >= 32 ? (isTa ? 'அசுபமானது' : 'Inauspicious') :
    (isTa ? 'மிகவும் அசுபமானது' : 'Highly Inauspicious');

  return (
    <div className={`relative bg-gradient-to-br ${bgColor} rounded-2xl p-6 flex flex-col items-center`}>
      <div className="relative w-36 h-36">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
          <circle
            cx="60" cy="60" r={radius}
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="10"
          />
          <circle
            cx="60" cy="60" r={radius}
            fill="none"
            stroke={scoreColor}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={dashOffset}
            strokeLinecap="round"
            className="transition-all duration-700 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-3xl font-black" style={{ color: scoreColor }}>{score}</span>
          <span className="text-xs text-gray-500 font-medium">{isTa ? 'மதிப்பெண்' : 'Score'}</span>
        </div>
      </div>

      <div className="mt-3 text-center">
        <div className="text-2xl tracking-widest" title={`${stars} stars`}>{starDisplay}</div>
        <div className="text-sm font-bold mt-1" style={{ color: scoreColor }}>{label}</div>
        <div className="text-xs text-gray-500 mt-0.5">
          {stars} {isTa ? 'நட்சத்திர மதிப்பீடு' : 'Star Rating'}
        </div>
      </div>
    </div>
  );
}

interface TimelineProps {
  windows: MuhurthaWindow[];
  language?: Language;
}

function TimelineBar({ windows, language = 'en' }: TimelineProps) {
  const isTa = language === 'ta';
  const sorted = [...windows].sort((a, b) => {
    const toMin = (t: string) => { const [h, m] = t.split(':').map(Number); return h * 60 + m; };
    return toMin(a.startTime) - toMin(b.startTime);
  });

  return (
    <div className="w-full">
      <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
        {isTa ? 'நாளின் நேர சாளரங்கள்' : "Today's Time Windows"}
      </h4>
      <div className="space-y-2">
        {sorted.map((window, idx) => {
          const colorConfig = {
            suitable: { bar: 'bg-emerald-500', bg: 'bg-emerald-50', border: 'border-emerald-200', text: 'text-emerald-700', badge: 'bg-emerald-100 text-emerald-800' },
            avoid:    { bar: 'bg-red-500',     bg: 'bg-red-50',     border: 'border-red-200',     text: 'text-red-700',     badge: 'bg-red-100 text-red-800'     },
            neutral:  { bar: 'bg-gray-400',    bg: 'bg-gray-50',    border: 'border-gray-200',    text: 'text-gray-600',    badge: 'bg-gray-100 text-gray-700'   },
          }[window.type];

          const widthPercent = Math.max(8, window.score);
          const typeLabel = window.type === 'suitable'
            ? (isTa ? 'பொருத்தமான' : 'Suitable')
            : window.type === 'avoid'
              ? (isTa ? 'தவிர்க்கவும்' : 'Avoid')
              : (isTa ? 'நடுநிலை' : 'Neutral');

          return (
            <div key={idx} className={`rounded-lg border ${colorConfig.bg} ${colorConfig.border} p-3`}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${colorConfig.badge}`}>
                    {typeLabel}
                  </span>
                  <span className="text-sm font-semibold text-gray-800">
                    {window.startTime} – {window.endTime}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-500">{window.score}/100</span>
                  <span className="text-sm">{['★★★★★','★★★★☆','★★★☆☆','★★☆☆☆','★☆☆☆☆'][5 - window.stars]}</span>
                </div>
              </div>

              <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className={`h-full ${colorConfig.bar} rounded-full transition-all duration-500`}
                  style={{ width: `${widthPercent}%` }}
                />
              </div>

              <p className={`text-xs mt-1.5 font-medium ${colorConfig.text}`}>
                {isTa ? window.label.ta : window.label.en}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

interface PanchangCardProps {
  panchang: MuhurthaResult['panchang'];
  language?: Language;
}

function PanchangCard({ panchang, language = 'en' }: PanchangCardProps) {
  const isTa = language === 'ta';

  const rows = [
    { icon: '🌙', label: isTa ? 'திதி' : 'Tithi', value: isTa ? `${panchang.tithi.nameTa} (${panchang.tithi.number})` : `${panchang.tithi.name} (${panchang.tithi.number})`, quality: panchang.tithi.quality },
    { icon: '⭐', label: isTa ? 'நட்சத்திரம்' : 'Nakshatra', value: isTa ? panchang.nakshatra.nameTa : panchang.nakshatra.name, quality: 'neutral' },
    { icon: '🔮', label: isTa ? 'யோகம்' : 'Yoga', value: isTa ? panchang.yoga.nameTa : panchang.yoga.name, quality: panchang.yoga.quality },
    { icon: '📿', label: isTa ? 'கரணம்' : 'Karana', value: isTa ? panchang.karana.nameTa : panchang.karana.name, quality: panchang.karana.quality },
    { icon: '📅', label: isTa ? 'வாரம்' : 'Vaara', value: isTa ? panchang.vaara.nameTa : panchang.vaara.name, quality: 'neutral' },
    { icon: '🕐', label: isTa ? 'ஹோரை' : 'Hora', value: isTa ? panchang.hora.planetTa : panchang.hora.planet, quality: panchang.hora.quality === 'benefic' ? 'auspicious' : panchang.hora.quality === 'malefic' ? 'inauspicious' : 'neutral' },
    { icon: '♈', label: isTa ? 'லக்னம்' : 'Lagna', value: isTa ? panchang.lagna.nameTa : panchang.lagna.name, quality: 'neutral' },
  ];

  const qualityDot: Record<string, string> = {
    auspicious: 'bg-emerald-400',
    good: 'bg-emerald-400',
    inauspicious: 'bg-red-400',
    bad: 'bg-red-400',
    neutral: 'bg-gray-300',
    benefic: 'bg-emerald-400',
    malefic: 'bg-red-400',
  };

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-4 py-3">
        <h3 className="text-white font-bold text-sm">
          {isTa ? '🗓 பஞ்சாங்க விவரங்கள்' : '🗓 Panchang Details'}
        </h3>
      </div>
      <div className="divide-y divide-gray-50">
        {rows.map((row, idx) => (
          <div key={idx} className="flex items-center justify-between px-4 py-2.5 hover:bg-gray-50">
            <span className="flex items-center gap-2 text-xs text-gray-500 font-medium w-24">
              <span>{row.icon}</span>
              {row.label}
            </span>
            <span className="flex items-center gap-2">
              <span className={`w-2 h-2 rounded-full ${qualityDot[row.quality] ?? 'bg-gray-300'}`} />
              <span className="text-sm font-semibold text-gray-800">{row.value}</span>
            </span>
          </div>
        ))}
      </div>

      <div className="px-4 py-3 bg-gray-50 space-y-1.5">
        <TimeBadge
          label={isTa ? 'ராகு காலம்' : 'Rahu Kalam'}
          time={`${panchang.rahuKalam.start}–${panchang.rahuKalam.end}`}
          isActive={panchang.rahuKalam.isActive}
          severity="critical"
        />
        <TimeBadge
          label={isTa ? 'யமகண்டம்' : 'Yamagandam'}
          time={`${panchang.yamagandam.start}–${panchang.yamagandam.end}`}
          isActive={panchang.yamagandam.isActive}
          severity="critical"
        />
        <TimeBadge
          label={isTa ? 'குளிகை' : 'Kuligai'}
          time={`${panchang.kuligai.start}–${panchang.kuligai.end}`}
          isActive={panchang.kuligai.isActive}
          severity="moderate"
        />
        <TimeBadge
          label={isTa ? 'அபிஜித் முகூர்த்தம்' : 'Abhijit Muhurtha'}
          time={`${panchang.abhijitMuhurtha.start}–${panchang.abhijitMuhurtha.end}`}
          isActive={panchang.abhijitMuhurtha.isActive}
          severity="good"
        />
      </div>
    </div>
  );
}

function TimeBadge({ label, time, isActive, severity }: {
  label: string; time: string; isActive: boolean; severity: 'critical' | 'moderate' | 'good';
}) {
  const config = {
    critical: { active: 'bg-red-100 text-red-800 border-red-200', inactive: 'bg-gray-50 text-gray-500 border-gray-200' },
    moderate: { active: 'bg-orange-100 text-orange-800 border-orange-200', inactive: 'bg-gray-50 text-gray-500 border-gray-200' },
    good:     { active: 'bg-emerald-100 text-emerald-800 border-emerald-200', inactive: 'bg-gray-50 text-gray-500 border-gray-200' },
  }[severity];

  return (
    <div className={`flex items-center justify-between rounded-lg border px-3 py-1.5 text-xs font-medium ${isActive ? config.active : config.inactive}`}>
      <span>{label}</span>
      <span className="font-mono">{time}{isActive ? ' ⚠️' : ''}</span>
    </div>
  );
}

interface ResultScreenProps {
  result: MuhurthaResult;
  language?: Language;
  onReset?: () => void;
}

export function ResultScreen({ result, language = 'en', onReset }: ResultScreenProps) {
  const isTa = language === 'ta';

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-black text-gray-900">
            {isTa ? 'முகூர்த்த மதிப்பீடு முடிவு' : 'Muhurtha Evaluation Result'}
          </h2>
          <p className="text-xs text-gray-400 mt-0.5">
            {isTa ? 'கோரிக்கை ID:' : 'Request ID:'} {result.requestId.slice(0, 8)}...
          </p>
        </div>
        {onReset && (
          <button
            onClick={onReset}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-gray-200 text-sm text-gray-600 hover:bg-gray-50 font-medium"
          >
            ← {isTa ? 'புதிய தேடல்' : 'New Search'}
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <div className="lg:col-span-1">
          <ScoreGauge
            score={result.score}
            stars={result.stars}
            starDisplay={result.starDisplay}
            language={language}
          />

          <div className="mt-4 bg-indigo-50 rounded-xl p-4 border border-indigo-100">
            <p className="text-xs font-semibold text-indigo-600 uppercase tracking-wider mb-1">
              {isTa ? 'தீர்ப்பு' : 'Verdict'}
            </p>
            <p className="text-sm text-gray-800 font-medium leading-relaxed">
              {isTa ? result.verdict.ta : result.verdict.en}
            </p>
          </div>
        </div>

        <div className="lg:col-span-2">
          <PanchangCard panchang={result.panchang} language={language} />
        </div>
      </div>

      <TimelineBar windows={result.windows} language={language} />

      <div>
        <h3 className="text-sm font-bold text-gray-700 mb-3 uppercase tracking-wider">
          {isTa ? 'சுப / அசுப காரணிகள்' : 'Positive / Negative Factors'}
        </h3>
        <BilingualBulletList
          positiveFactors={result.positiveFactors}
          negativeFactors={result.negativeFactors}
          language={language}
          showBothLanguages={true}
        />
      </div>

      <div className="text-center text-xs text-gray-400 pt-2 border-t border-gray-100">
        {isTa ? 'உருவாக்கப்பட்டது:' : 'Generated at:'} {new Date(result.generatedAt).toLocaleString()}
        {' · '}AstroJyothi Muhurtha Engine v1.0
      </div>
    </div>
  );
}
