import { z } from 'zod';
import { MUHURTHA_CATEGORIES } from '../constants/muhurthaConstants';
import { ERROR_MESSAGES } from '../constants/muhurthaConstants';

const VALID_CATEGORY_IDS = MUHURTHA_CATEGORIES.map((c) => c.id);

function isValidIANATimezone(tz: string): boolean {
  try {
    Intl.DateTimeFormat(undefined, { timeZone: tz });
    return true;
  } catch {
    return false;
  }
}

const VALID_NAKSHATRA_NAMES = [
  'Ashwini','Bharani','Krittika','Rohini','Mrigashirsha','Ardra','Punarvasu',
  'Pushya','Ashlesha','Magha','Purva Phalguni','Uttara Phalguni','Hasta',
  'Chitra','Swati','Vishakha','Anuradha','Jyeshtha','Mula','Purva Ashadha',
  'Uttara Ashadha','Shravana','Dhanishtha','Shatabhisha','Purva Bhadrapada',
  'Uttara Bhadrapada','Revati',
];

export const MuhurthaSearchSchema = z.object({
  date: z
    .string({ required_error: ERROR_MESSAGES.INVALID_DATE.en })
    .regex(/^\d{4}-\d{2}-\d{2}$/, ERROR_MESSAGES.INVALID_DATE.en)
    .refine((d) => {
      const parsed = new Date(d);
      return !isNaN(parsed.getTime()) && parsed.toISOString().startsWith(d);
    }, ERROR_MESSAGES.INVALID_DATE.en),

  time: z
    .string({ required_error: ERROR_MESSAGES.INVALID_TIME.en })
    .regex(/^([01]\d|2[0-3]):([0-5]\d)$/, ERROR_MESSAGES.INVALID_TIME.en),

  latitude: z
    .number({ required_error: ERROR_MESSAGES.INVALID_LATITUDE.en })
    .min(-90, ERROR_MESSAGES.INVALID_LATITUDE.en)
    .max(90, ERROR_MESSAGES.INVALID_LATITUDE.en),

  longitude: z
    .number({ required_error: ERROR_MESSAGES.INVALID_LONGITUDE.en })
    .min(-180, ERROR_MESSAGES.INVALID_LONGITUDE.en)
    .max(180, ERROR_MESSAGES.INVALID_LONGITUDE.en),

  timezone: z
    .string({ required_error: ERROR_MESSAGES.INVALID_TIMEZONE.en })
    .refine(isValidIANATimezone, ERROR_MESSAGES.INVALID_TIMEZONE.en),

  category: z
    .string({ required_error: ERROR_MESSAGES.INVALID_CATEGORY.en })
    .refine(
      (c) => VALID_CATEGORY_IDS.includes(c),
      ERROR_MESSAGES.INVALID_CATEGORY.en,
    ),

  birthNakshatra: z
    .string()
    .refine(
      (n) => VALID_NAKSHATRA_NAMES.includes(n),
      'Invalid birth nakshatra name.',
    )
    .optional(),
});

export const MuhurthaDetailsSchema = MuhurthaSearchSchema;

export const MuhurthaAiSchema = MuhurthaSearchSchema.extend({
  outputLanguage: z.enum(['en', 'ta', 'both']).default('both'),
  includeRawPanchang: z.boolean().default(true),
  includeRecommendations: z.boolean().default(true),
});

export type MuhurthaSearchInput = z.infer<typeof MuhurthaSearchSchema>;
export type MuhurthaAiInput = z.infer<typeof MuhurthaAiSchema>;

export function validateSearchInput(data: unknown): {
  success: boolean;
  data?: MuhurthaSearchInput;
  errors?: Array<{ field: string; message: string; messageTa: string }>;
} {
  const result = MuhurthaSearchSchema.safeParse(data);

  if (result.success) {
    return { success: true, data: result.data };
  }

  const errors = result.error.issues.map((issue) => {
    const field = issue.path.join('.');
    const tamilMsg = getTamilErrorMessage(field, issue.message);
    return {
      field: field || 'unknown',
      message: issue.message,
      messageTa: tamilMsg,
    };
  });

  return { success: false, errors };
}

export function validateAiInput(data: unknown): {
  success: boolean;
  data?: MuhurthaAiInput;
  errors?: Array<{ field: string; message: string; messageTa: string }>;
} {
  const result = MuhurthaAiSchema.safeParse(data);

  if (result.success) {
    return { success: true, data: result.data };
  }

  const errors = result.error.issues.map((issue) => {
    const field = issue.path.join('.');
    return {
      field: field || 'unknown',
      message: issue.message,
      messageTa: getTamilErrorMessage(field, issue.message),
    };
  });

  return { success: false, errors };
}

function getTamilErrorMessage(field: string, defaultEn: string): string {
  const map: Record<string, string> = {
    date: ERROR_MESSAGES.INVALID_DATE.ta,
    time: ERROR_MESSAGES.INVALID_TIME.ta,
    latitude: ERROR_MESSAGES.INVALID_LATITUDE.ta,
    longitude: ERROR_MESSAGES.INVALID_LONGITUDE.ta,
    timezone: ERROR_MESSAGES.INVALID_TIMEZONE.ta,
    category: ERROR_MESSAGES.INVALID_CATEGORY.ta,
  };
  return map[field] ?? defaultEn;
}
