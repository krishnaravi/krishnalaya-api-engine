import React, { useState, useCallback } from 'react';
import type { SearchFormValues, Language } from './types';

const TIMEZONES = [
  'Asia/Kolkata', 'Asia/Colombo', 'Asia/Dubai', 'Asia/Singapore',
  'America/New_York', 'America/Los_Angeles', 'America/Chicago',
  'Europe/London', 'Europe/Berlin', 'Australia/Sydney',
  'Pacific/Auckland', 'Asia/Tokyo', 'Asia/Bangkok', 'Asia/Kuala_Lumpur',
];

const NAKSHATRAS = [
  'Ashwini','Bharani','Krittika','Rohini','Mrigashirsha','Ardra','Punarvasu',
  'Pushya','Ashlesha','Magha','Purva Phalguni','Uttara Phalguni','Hasta',
  'Chitra','Swati','Vishakha','Anuradha','Jyeshtha','Mula','Purva Ashadha',
  'Uttara Ashadha','Shravana','Dhanishtha','Shatabhisha','Purva Bhadrapada',
  'Uttara Bhadrapada','Revati',
];

interface SearchFormProps {
  onSubmit: (values: SearchFormValues) => void;
  isLoading?: boolean;
  language?: Language;
  selectedCategory?: string;
}

const defaultValues: SearchFormValues = {
  date: new Date().toISOString().split('T')[0],
  time: '10:00',
  latitude: '13.0827',
  longitude: '80.2707',
  timezone: 'Asia/Kolkata',
  category: '',
  birthNakshatra: '',
};

type FieldErrors = Partial<Record<keyof SearchFormValues, string>>;

export function SearchForm({
  onSubmit,
  isLoading = false,
  language = 'en',
  selectedCategory = '',
}: SearchFormProps) {
  const [values, setValues] = useState<SearchFormValues>({
    ...defaultValues,
    category: selectedCategory,
  });
  const [errors, setErrors] = useState<FieldErrors>({});
  const [geoLoading, setGeoLoading] = useState(false);

  const isTa = language === 'ta';

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
      const { name, value } = e.target;
      setValues((prev) => ({ ...prev, [name]: value }));
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    },
    [],
  );

  const validate = useCallback((): boolean => {
    const newErrors: FieldErrors = {};

    if (!values.date) newErrors.date = isTa ? 'தேதி தேவை' : 'Date is required';
    if (!values.time) newErrors.time = isTa ? 'நேரம் தேவை' : 'Time is required';
    if (!values.category) newErrors.category = isTa ? 'வகை தேர்வு செய்யவும்' : 'Please select a category';

    const lat = parseFloat(values.latitude);
    const lng = parseFloat(values.longitude);
    if (isNaN(lat) || lat < -90 || lat > 90) {
      newErrors.latitude = isTa ? 'செல்லுபடியான அட்சரேகை (−90 முதல் 90)' : 'Valid latitude required (−90 to 90)';
    }
    if (isNaN(lng) || lng < -180 || lng > 180) {
      newErrors.longitude = isTa ? 'செல்லுபடியான தீர்க்கரேகை (−180 முதல் 180)' : 'Valid longitude required (−180 to 180)';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [values, isTa]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(values);
    }
  };

  const detectLocation = () => {
    if (!navigator.geolocation) return;
    setGeoLoading(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setValues((prev) => ({
          ...prev,
          latitude: pos.coords.latitude.toFixed(4),
          longitude: pos.coords.longitude.toFixed(4),
        }));
        setErrors((prev) => ({ ...prev, latitude: undefined, longitude: undefined }));
        setGeoLoading(false);
      },
      () => setGeoLoading(false),
    );
  };

  const fieldClass = (name: keyof SearchFormValues) =>
    [
      'w-full px-3 py-2 rounded-lg border text-sm transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-indigo-400',
      errors[name] ? 'border-red-400 bg-red-50' : 'border-gray-300 bg-white hover:border-indigo-300',
    ].join(' ');

  const labelClass = 'block text-xs font-semibold text-gray-700 mb-1';
  const errorClass = 'text-xs text-red-600 mt-1';

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 space-y-5">
      <div className="flex items-center gap-3 mb-2">
        <div className="w-10 h-10 rounded-xl bg-indigo-100 flex items-center justify-center text-xl">🔍</div>
        <div>
          <h2 className="text-lg font-bold text-gray-900">
            {isTa ? 'முகூர்த்த தேடல்' : 'Muhurtha Search'}
          </h2>
          <p className="text-xs text-gray-500">
            {isTa ? 'விவரங்களை உள்ளிட்டு சுப நேரத்தை கண்டறியுங்கள்' : 'Enter details to find the auspicious time'}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label htmlFor="date" className={labelClass}>
            {isTa ? '📅 தேதி' : '📅 Date'}
          </label>
          <input
            id="date"
            type="date"
            name="date"
            value={values.date}
            onChange={handleChange}
            className={fieldClass('date')}
            min="2000-01-01"
            max="2099-12-31"
          />
          {errors.date && <p className={errorClass}>{errors.date}</p>}
        </div>

        <div>
          <label htmlFor="time" className={labelClass}>
            {isTa ? '⏰ நேரம் (HH:MM)' : '⏰ Time (HH:MM)'}
          </label>
          <input
            id="time"
            type="time"
            name="time"
            value={values.time}
            onChange={handleChange}
            className={fieldClass('time')}
          />
          {errors.time && <p className={errorClass}>{errors.time}</p>}
        </div>
      </div>

      <div>
        <div className="flex items-center justify-between mb-1">
          <span className={labelClass.replace('mb-1', '')}>
            {isTa ? '📍 இருப்பிடம்' : '📍 Location'}
          </span>
          <button
            type="button"
            onClick={detectLocation}
            disabled={geoLoading}
            className="text-xs text-indigo-600 hover:text-indigo-800 font-medium flex items-center gap-1 disabled:opacity-50"
          >
            {geoLoading ? (
              <span className="inline-block w-3 h-3 border-2 border-indigo-400 border-t-transparent rounded-full animate-spin" />
            ) : (
              '📡'
            )}
            {isTa ? 'தானாக கண்டறிய' : 'Auto-detect'}
          </button>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <input
              id="latitude"
              type="number"
              name="latitude"
              value={values.latitude}
              onChange={handleChange}
              placeholder={isTa ? 'அட்சரேகை' : 'Latitude'}
              step="0.0001"
              min="-90"
              max="90"
              className={fieldClass('latitude')}
            />
            {errors.latitude && <p className={errorClass}>{errors.latitude}</p>}
          </div>
          <div>
            <input
              id="longitude"
              type="number"
              name="longitude"
              value={values.longitude}
              onChange={handleChange}
              placeholder={isTa ? 'தீர்க்கரேகை' : 'Longitude'}
              step="0.0001"
              min="-180"
              max="180"
              className={fieldClass('longitude')}
            />
            {errors.longitude && <p className={errorClass}>{errors.longitude}</p>}
          </div>
        </div>
      </div>

      <div>
        <label htmlFor="timezone" className={labelClass}>
          {isTa ? '🌐 நேர மண்டலம்' : '🌐 Timezone'}
        </label>
        <select
          id="timezone"
          name="timezone"
          value={values.timezone}
          onChange={handleChange}
          className={fieldClass('timezone')}
        >
          {TIMEZONES.map((tz) => (
            <option key={tz} value={tz}>{tz}</option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="birthNakshatra" className={labelClass}>
          {isTa ? '⭐ பிறப்பு நட்சத்திரம் (விருப்பத்தேர்வு)' : '⭐ Birth Nakshatra (optional)'}
        </label>
        <select
          id="birthNakshatra"
          name="birthNakshatra"
          value={values.birthNakshatra}
          onChange={handleChange}
          className={fieldClass('birthNakshatra')}
        >
          <option value="">{isTa ? '-- தேர்வு செய்யவும் --' : '-- Select --'}</option>
          {NAKSHATRAS.map((n) => (
            <option key={n} value={n}>{n}</option>
          ))}
        </select>
        <p className="text-xs text-gray-400 mt-1">
          {isTa
            ? 'தார பலம் மற்றும் சந்திராஷ்டம கணக்கீட்டிற்கு தேவை'
            : 'Required for Tara Bala and Chandrashtama calculation'}
        </p>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className={[
          'w-full py-3 px-6 rounded-xl text-white font-semibold text-sm transition-all duration-200 flex items-center justify-center gap-2',
          isLoading
            ? 'bg-indigo-400 cursor-not-allowed'
            : 'bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 shadow-md hover:shadow-lg',
        ].join(' ')}
      >
        {isLoading ? (
          <>
            <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            {isTa ? 'கணக்கிடுகிறது...' : 'Calculating...'}
          </>
        ) : (
          <>
            <span>🔮</span>
            {isTa ? 'முகூர்த்தம் கண்டறிய' : 'Find Muhurtha'}
          </>
        )}
      </button>
    </form>
  );
}
