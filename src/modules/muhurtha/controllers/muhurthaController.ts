import type { Request, Response, NextFunction } from 'express';
import {
  validateSearchInput,
  validateAiInput,
} from '../validators/muhurthaValidator';
import {
  calculateMuhurtha,
  getMuhurthaCategories,
} from '../services/muhurthaService';
import { generateAiResponse } from '../services/aiIntegrationService';
import { ERROR_MESSAGES } from '../constants/muhurthaConstants';

function sendValidationError(
  res: Response,
  errors: Array<{ field: string; message: string; messageTa: string }>,
) {
  return res.status(400).json({
    success: false,
    error: {
      code: 'VALIDATION_ERROR',
      message: 'Request validation failed',
      messageTa: 'கோரிக்கை சரிபார்ப்பு தோல்வியடைந்தது',
      fields: errors,
    },
  });
}

export async function getCategories(
  _req: Request,
  res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    const categories = getMuhurthaCategories();
    res.status(200).json({
      success: true,
      count: categories.length,
      data: categories,
    });
  } catch (err) {
    next(err);
  }
}

export async function searchMuhurtha(
  req: Request,
  res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    const validation = validateSearchInput(req.body);
    if (!validation.success || !validation.data) {
      sendValidationError(res, validation.errors ?? []);
      return;
    }

    const result = calculateMuhurtha(validation.data);

    res.status(200).json({
      success: true,
      data: {
        requestId: result.requestId,
        category: {
          id: result.category,
          nameTa: result.categoryNameTa,
        },
        date: result.date,
        time: result.time,
        score: result.score,
        stars: result.stars,
        starDisplay: result.starDisplay,
        verdict: result.verdict,
        panchang: result.panchang,
        windows: result.windows,
        positiveFactors: result.positiveFactors,
        negativeFactors: result.negativeFactors,
        suitableTimes: result.suitableTimes,
        avoidTimes: result.avoidTimes,
        generatedAt: result.generatedAt,
      },
    });
  } catch (err) {
    next(err);
  }
}

export async function getMuhurthaDetails(
  req: Request,
  res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    const validation = validateSearchInput(req.body);
    if (!validation.success || !validation.data) {
      sendValidationError(res, validation.errors ?? []);
      return;
    }

    const result = calculateMuhurtha(validation.data);

    res.status(200).json({
      success: true,
      data: {
        requestId: result.requestId,
        overview: {
          score: result.score,
          stars: result.stars,
          starDisplay: result.starDisplay,
          verdict: result.verdict,
        },
        panchangDetails: {
          tithi: result.panchang.tithi,
          nakshatra: result.panchang.nakshatra,
          yoga: result.panchang.yoga,
          karana: result.panchang.karana,
          vaara: result.panchang.vaara,
          hora: result.panchang.hora,
          lagna: result.panchang.lagna,
        },
        doshaAnalysis: {
          rahuKalam: result.panchang.rahuKalam,
          yamagandam: result.panchang.yamagandam,
          kuligai: result.panchang.kuligai,
          abhijitMuhurtha: result.panchang.abhijitMuhurtha,
          chandrashtama: result.panchang.chandrashtama,
          taraBalance: result.panchang.taraBalance,
        },
        strengthAnalysis: {
          moonLongitude: result.panchang.moonLongitude,
          sunLongitude: result.panchang.sunLongitude,
        },
        ruleBreakdown: result.ruleResults.map((r) => ({
          ruleName: r.ruleName,
          impact: r.impact,
          weight: r.weight,
          contributedScore: r.contributedScore,
          reason: r.reason,
          details: r.details,
        })),
        positiveFactors: result.positiveFactors,
        negativeFactors: result.negativeFactors,
        timeWindows: result.windows,
        suitableTimes: result.suitableTimes,
        avoidTimes: result.avoidTimes,
        generatedAt: result.generatedAt,
      },
    });
  } catch (err) {
    next(err);
  }
}

export async function getAiPayload(
  req: Request,
  res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    const validation = validateAiInput(req.body);
    if (!validation.success || !validation.data) {
      sendValidationError(res, validation.errors ?? []);
      return;
    }

    const payload = generateAiResponse(validation.data);

    res.status(200).json({
      success: true,
      data: payload,
    });
  } catch (err) {
    next(err);
  }
}

export function globalErrorHandler(
  err: Error,
  _req: Request,
  res: Response,
  _next: NextFunction,
): void {
  console.error('[MuhurthaController] Unhandled error:', err);
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: ERROR_MESSAGES.CALCULATION_ERROR.en,
      messageTa: ERROR_MESSAGES.CALCULATION_ERROR.ta,
      ...(process.env.NODE_ENV !== 'production' && { stack: err.stack }),
    },
  });
}
