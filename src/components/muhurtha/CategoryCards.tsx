import React from 'react';
import type { CategoryItem, Language } from './types';

const CATEGORY_ICONS: Record<string, string> = {
  marriage: '💒', engagement: '💍', house_warming: '🏠', land_purchase: '🌾',
  land_registration: '📋', bhoomi_pooja: '⛏️', foundation: '🏗️',
  roof_installation: '🏚️', business_opening: '🏢', office_opening: '🖥️',
  shop_opening: '🏪', vehicle_purchase: '🚗', vehicle_registration: '📄',
  school_admission: '🏫', college_admission: '🎓', aksharabhyasam: '✍️',
  naming_ceremony: '👶', ear_piercing: '💎', annaprasanam: '🍚',
  mottai: '✂️', upanayanam: '🪡', medical_treatment: '💊', surgery: '🔬',
  ivf: '🧬', passport: '🛂', visa: '✈️', foreign_travel: '🌍',
  investment: '📈', gold_purchase: '🥇', silver_purchase: '🥈',
  temple_kumbabishekam: '🛕', homam: '🔥', yagam: '🪔', deeksha: '🙏',
  agriculture: '🌱', well_digging: '💧', borewell: '🚰',
};

const CATEGORY_COLORS: Record<string, { bg: string; border: string; badge: string }> = {
  marriage:           { bg: 'bg-rose-50',    border: 'border-rose-200',    badge: 'bg-rose-100 text-rose-700'   },
  engagement:         { bg: 'bg-pink-50',    border: 'border-pink-200',    badge: 'bg-pink-100 text-pink-700'   },
  house_warming:      { bg: 'bg-amber-50',   border: 'border-amber-200',   badge: 'bg-amber-100 text-amber-700' },
  land_purchase:      { bg: 'bg-green-50',   border: 'border-green-200',   badge: 'bg-green-100 text-green-700' },
  land_registration:  { bg: 'bg-teal-50',    border: 'border-teal-200',    badge: 'bg-teal-100 text-teal-700'   },
  bhoomi_pooja:       { bg: 'bg-yellow-50',  border: 'border-yellow-200',  badge: 'bg-yellow-100 text-yellow-700'},
  foundation:         { bg: 'bg-stone-50',   border: 'border-stone-200',   badge: 'bg-stone-100 text-stone-700' },
  roof_installation:  { bg: 'bg-slate-50',   border: 'border-slate-200',   badge: 'bg-slate-100 text-slate-700' },
  business_opening:   { bg: 'bg-blue-50',    border: 'border-blue-200',    badge: 'bg-blue-100 text-blue-700'   },
  office_opening:     { bg: 'bg-indigo-50',  border: 'border-indigo-200',  badge: 'bg-indigo-100 text-indigo-700'},
  shop_opening:       { bg: 'bg-violet-50',  border: 'border-violet-200',  badge: 'bg-violet-100 text-violet-700'},
  vehicle_purchase:   { bg: 'bg-cyan-50',    border: 'border-cyan-200',    badge: 'bg-cyan-100 text-cyan-700'   },
  school_admission:   { bg: 'bg-sky-50',     border: 'border-sky-200',     badge: 'bg-sky-100 text-sky-700'     },
  gold_purchase:      { bg: 'bg-yellow-50',  border: 'border-yellow-300',  badge: 'bg-yellow-200 text-yellow-800'},
  temple_kumbabishekam:{ bg: 'bg-orange-50', border: 'border-orange-200',  badge: 'bg-orange-100 text-orange-700'},
  homam:              { bg: 'bg-red-50',     border: 'border-red-200',     badge: 'bg-red-100 text-red-700'     },
};

function getColors(id: string) {
  return CATEGORY_COLORS[id] ?? { bg: 'bg-purple-50', border: 'border-purple-200', badge: 'bg-purple-100 text-purple-700' };
}

interface CategoryCardsProps {
  categories: CategoryItem[];
  selectedCategory: string;
  onSelect: (id: string) => void;
  language?: Language;
}

export function CategoryCards({
  categories,
  selectedCategory,
  onSelect,
  language = 'en',
}: CategoryCardsProps) {
  return (
    <div className="w-full">
      <div className="mb-4">
        <h2 className="text-xl font-bold text-gray-800">
          {language === 'ta' ? 'முகூர்த்த வகைகளை தேர்வு செய்யுங்கள்' : 'Select Muhurtha Category'}
        </h2>
        <p className="text-sm text-gray-500 mt-1">
          {language === 'ta'
            ? `${categories.length} வகைகள் கிடைக்கின்றன`
            : `${categories.length} categories available`}
        </p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3">
        {categories.map((cat) => {
          const colors = getColors(cat.id);
          const isSelected = selectedCategory === cat.id;
          const icon = CATEGORY_ICONS[cat.id] ?? '⭐';

          return (
            <button
              key={cat.id}
              onClick={() => onSelect(cat.id)}
              className={[
                'relative flex flex-col items-center justify-center p-3 rounded-xl border-2 transition-all duration-200 cursor-pointer text-center group',
                colors.bg,
                isSelected
                  ? 'border-indigo-500 ring-2 ring-indigo-200 shadow-md scale-105'
                  : `${colors.border} hover:border-indigo-300 hover:shadow-sm hover:scale-102`,
              ].join(' ')}
              aria-pressed={isSelected}
              title={language === 'ta' ? cat.nameTa : cat.name}
            >
              {isSelected && (
                <span className="absolute -top-2 -right-2 w-5 h-5 bg-indigo-600 rounded-full flex items-center justify-center text-white text-xs shadow">
                  ✓
                </span>
              )}

              <span className="text-2xl mb-1.5 group-hover:scale-110 transition-transform duration-150">
                {icon}
              </span>

              <span className="text-xs font-semibold text-gray-800 leading-tight">
                {language === 'ta' ? cat.nameTa : cat.name}
              </span>

              {language === 'en' && cat.nameTa && (
                <span className="text-[10px] text-gray-500 mt-0.5 font-medium">
                  {cat.nameTa}
                </span>
              )}

              <span className={`mt-1.5 text-[9px] px-1.5 py-0.5 rounded-full font-medium ${colors.badge}`}>
                {language === 'ta' ? 'முகூர்த்தம்' : 'Muhurtha'}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

interface CompactCategoryBadgeProps {
  category: CategoryItem;
  language?: Language;
}

export function CompactCategoryBadge({ category, language = 'en' }: CompactCategoryBadgeProps) {
  const colors = getColors(category.id);
  const icon = CATEGORY_ICONS[category.id] ?? '⭐';
  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium ${colors.bg} border ${colors.border}`}>
      <span>{icon}</span>
      <span>{language === 'ta' ? category.nameTa : category.name}</span>
    </span>
  );
}
