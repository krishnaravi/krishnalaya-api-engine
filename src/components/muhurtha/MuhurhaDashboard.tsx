import React, { useState, useEffect, useCallback } from 'react';
import type { CategoryItem, MuhurthaResult, SearchFormValues, Language } from './types';
import { CategoryCards } from './CategoryCards';
import { SearchForm } from './SearchForm';
import { ResultScreen } from './ResultScreen';

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:4000';

type DashboardView = 'categories' | 'search' | 'result' | 'error';

interface APIError {
  message: string;
  messageTa?: string;
  fields?: Array<{ field: string; message: string; messageTa: string }>;
}

function LanguageToggle({ language, onChange }: { language: Language; onChange: (l: Language) => void }) {
  return (
    <div className="flex items-center bg-gray-100 rounded-lg p-0.5 gap-0.5">
      <button
        onClick={() => onChange('en')}
        className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
          language === 'en' ? 'bg-white text-indigo-700 shadow-sm' : 'text-gray-500 hover:text-gray-700'
        }`}
      >
        EN
      </button>
      <button
        onClick={() => onChange('ta')}
        className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
          language === 'ta' ? 'bg-white text-indigo-700 shadow-sm' : 'text-gray-500 hover:text-gray-700'
        }`}
      >
        தமிழ்
      </button>
    </div>
  );
}

function LoadingSpinner({ message }: { message: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-4">
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 rounded-full border-4 border-indigo-100" />
        <div className="absolute inset-0 rounded-full border-4 border-indigo-500 border-t-transparent animate-spin" />
        <div className="absolute inset-0 flex items-center justify-center text-2xl">🔮</div>
      </div>
      <p className="text-sm text-gray-500 font-medium">{message}</p>
    </div>
  );
}

function ErrorDisplay({ error, onRetry, language }: { error: APIError; onRetry: () => void; language: Language }) {
  const isTa = language === 'ta';
  return (
    <div className="max-w-md mx-auto text-center py-12">
      <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center text-3xl mx-auto mb-4">
        ⚠️
      </div>
      <h3 className="font-bold text-gray-900 mb-2">
        {isTa ? 'பிழை ஏற்பட்டது' : 'An Error Occurred'}
      </h3>
      <p className="text-sm text-gray-600 mb-1">
        {isTa && error.messageTa ? error.messageTa : error.message}
      </p>
      {error.fields && error.fields.length > 0 && (
        <ul className="text-xs text-red-600 mt-2 text-left bg-red-50 rounded-lg p-3 space-y-1">
          {error.fields.map((f, i) => (
            <li key={i}>{f.field}: {isTa ? f.messageTa : f.message}</li>
          ))}
        </ul>
      )}
      <button
        onClick={onRetry}
        className="mt-6 px-5 py-2.5 bg-indigo-600 text-white text-sm font-semibold rounded-xl hover:bg-indigo-700 transition-colors"
      >
        {isTa ? 'மீண்டும் முயற்சிக்கவும்' : 'Try Again'}
      </button>
    </div>
  );
}

interface StepIndicatorProps {
  currentStep: number;
  language: Language;
}

function StepIndicator({ currentStep, language }: StepIndicatorProps) {
  const isTa = language === 'ta';
  const steps = [
    { icon: '🗂', label: isTa ? 'வகை' : 'Category' },
    { icon: '📝', label: isTa ? 'விவரங்கள்' : 'Details' },
    { icon: '✨', label: isTa ? 'முடிவு' : 'Result' },
  ];

  return (
    <div className="flex items-center justify-center gap-2 mb-6">
      {steps.map((step, idx) => {
        const stepNum = idx + 1;
        const isCompleted = currentStep > stepNum;
        const isCurrent = currentStep === stepNum;

        return (
          <React.Fragment key={idx}>
            <div className="flex items-center gap-1.5">
              <div
                className={[
                  'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all',
                  isCompleted ? 'bg-emerald-500 text-white' :
                  isCurrent ? 'bg-indigo-600 text-white ring-4 ring-indigo-100' :
                  'bg-gray-100 text-gray-400',
                ].join(' ')}
              >
                {isCompleted ? '✓' : step.icon}
              </div>
              <span className={`text-xs font-medium hidden sm:block ${isCurrent ? 'text-indigo-600' : 'text-gray-400'}`}>
                {step.label}
              </span>
            </div>
            {idx < steps.length - 1 && (
              <div className={`flex-1 max-w-12 h-0.5 rounded ${currentStep > stepNum ? 'bg-emerald-400' : 'bg-gray-200'}`} />
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
}

export function MuhurhaDashboard() {
  const [view, setView] = useState<DashboardView>('categories');
  const [categories, setCategories] = useState<CategoryItem[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [result, setResult] = useState<MuhurthaResult | null>(null);
  const [error, setError] = useState<APIError | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState<Language>('en');
  const [categoriesLoading, setCategoriesLoading] = useState(true);

  const isTa = language === 'ta';

  useEffect(() => {
    fetch(`${API_BASE}/api/muhurtha/categories`)
      .then((r) => r.json())
      .then((data) => {
        if (data.success && data.data) {
          setCategories(data.data);
        }
      })
      .catch(() => {
        setCategories([]);
      })
      .finally(() => setCategoriesLoading(false));
  }, []);

  const handleCategorySelect = useCallback((id: string) => {
    setSelectedCategory(id);
  }, []);

  const handleCategoryConfirm = useCallback(() => {
    if (!selectedCategory) return;
    setView('search');
  }, [selectedCategory]);

  const handleSearch = useCallback(async (values: SearchFormValues) => {
    setIsLoading(true);
    setError(null);

    try {
      const payload = {
        date: values.date,
        time: values.time,
        latitude: parseFloat(values.latitude),
        longitude: parseFloat(values.longitude),
        timezone: values.timezone,
        category: values.category || selectedCategory,
        ...(values.birthNakshatra && { birthNakshatra: values.birthNakshatra }),
      };

      const response = await fetch(`${API_BASE}/api/muhurtha/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        setError({
          message: data.error?.message ?? 'An error occurred',
          messageTa: data.error?.messageTa,
          fields: data.error?.fields,
        });
        setView('error');
        return;
      }

      setResult(data.data);
      setView('result');
    } catch {
      setError({
        message: 'Failed to connect to the server. Please check your connection.',
        messageTa: 'சேவையகத்துடன் இணைக்க முடியவில்லை. உங்கள் இணைப்பை சரிபார்க்கவும்.',
      });
      setView('error');
    } finally {
      setIsLoading(false);
    }
  }, [selectedCategory]);

  const handleReset = useCallback(() => {
    setView('categories');
    setSelectedCategory('');
    setResult(null);
    setError(null);
  }, []);

  const currentStep = view === 'categories' ? 1 : view === 'search' ? 2 : 3;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-indigo-50 to-purple-50">
      <header className="sticky top-0 z-20 bg-white/95 backdrop-blur-sm border-b border-gray-100 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center text-lg shadow-md">
              🕉
            </div>
            <div>
              <h1 className="text-base font-black text-gray-900 leading-tight">
                AstroJyothi
              </h1>
              <p className="text-[10px] text-indigo-600 font-semibold tracking-wide uppercase">
                {isTa ? 'முகூர்த்த இயந்திரம்' : 'Muhurtha Engine'}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {view !== 'categories' && (
              <button
                onClick={handleReset}
                className="text-xs text-gray-500 hover:text-gray-700 font-medium px-2 py-1.5 rounded-lg hover:bg-gray-100"
              >
                ← {isTa ? 'முகப்பு' : 'Home'}
              </button>
            )}
            <LanguageToggle language={language} onChange={setLanguage} />
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        {(view === 'categories' || view === 'search') && (
          <StepIndicator currentStep={currentStep} language={language} />
        )}

        {view === 'categories' && (
          <div className="space-y-6">
            {categoriesLoading ? (
              <LoadingSpinner message={isTa ? 'வகைகளை ஏற்றுகிறது...' : 'Loading categories...'} />
            ) : (
              <>
                <CategoryCards
                  categories={categories}
                  selectedCategory={selectedCategory}
                  onSelect={handleCategorySelect}
                  language={language}
                />
                <div className="flex justify-end">
                  <button
                    onClick={handleCategoryConfirm}
                    disabled={!selectedCategory}
                    className={[
                      'px-6 py-3 rounded-xl text-sm font-bold transition-all duration-200 flex items-center gap-2',
                      selectedCategory
                        ? 'bg-indigo-600 text-white hover:bg-indigo-700 shadow-md hover:shadow-lg'
                        : 'bg-gray-200 text-gray-400 cursor-not-allowed',
                    ].join(' ')}
                  >
                    {isTa ? 'தொடரவும்' : 'Continue'}
                    <span>→</span>
                  </button>
                </div>
              </>
            )}
          </div>
        )}

        {view === 'search' && (
          <div className="max-w-2xl mx-auto">
            <div className="mb-4">
              <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-indigo-50 rounded-lg border border-indigo-100">
                <span className="text-xs text-indigo-600 font-medium">
                  {isTa ? 'தேர்ந்தெடுக்கப்பட்ட வகை:' : 'Selected:'}
                </span>
                <span className="text-xs font-bold text-indigo-800">
                  {categories.find((c) => c.id === selectedCategory)?.[language === 'ta' ? 'nameTa' : 'name'] ?? selectedCategory}
                </span>
              </div>
            </div>
            <SearchForm
              onSubmit={handleSearch}
              isLoading={isLoading}
              language={language}
              selectedCategory={selectedCategory}
            />
          </div>
        )}

        {view === 'result' && result && (
          <ResultScreen
            result={result}
            language={language}
            onReset={handleReset}
          />
        )}

        {view === 'error' && error && (
          <ErrorDisplay
            error={error}
            onRetry={() => setView('search')}
            language={language}
          />
        )}

        {isLoading && view !== 'result' && (
          <div className="fixed inset-0 bg-black/30 backdrop-blur-sm z-50 flex items-center justify-center">
            <div className="bg-white rounded-2xl p-8 shadow-2xl text-center max-w-xs mx-4">
              <LoadingSpinner message={isTa ? 'பஞ்சாங்கம் கணக்கிடுகிறது...' : 'Computing Panchang...'} />
              <p className="text-xs text-gray-400 mt-2">
                {isTa ? 'அனைத்து விதிகளும் மதிப்பிடப்படுகின்றன' : 'Evaluating all Vedic rules'}
              </p>
            </div>
          </div>
        )}
      </main>

      <footer className="text-center py-6 text-xs text-gray-400 border-t border-gray-100 mt-8">
        <p>
          AstroJyothi Muhurtha Engine · Lahiri Ayanamsa · 37 {isTa ? 'வகைகள்' : 'Categories'} ·
          {' '}{isTa ? 'தமிழ் & ஆங்கிலம்' : 'Tamil & English'}
        </p>
        <p className="mt-1 text-gray-300">
          {isTa ? 'வேத ஜோதிடம் அடிப்படையிலான முகூர்த்த மதிப்பீட்டு இயந்திரம்' : 'Vedic Astrology-based Muhurtha Evaluation Engine'}
        </p>
      </footer>
    </div>
  );
}
