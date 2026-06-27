import { Router } from 'express';
import {
  getCategories,
  searchMuhurtha,
  getMuhurthaDetails,
  getAiPayload,
} from '../controllers/muhurthaController';

const router = Router();

/**
 * @openapi
 * /api/muhurtha/categories:
 *   get:
 *     tags: [Muhurtha]
 *     summary: Get all 37 Muhurtha categories
 *     description: Returns a complete list of all supported Vedic muhurtha categories with bilingual names (English and Tamil).
 *     responses:
 *       200:
 *         description: List of muhurtha categories
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/CategoriesResponse'
 */
router.get('/categories', getCategories);

/**
 * @openapi
 * /api/muhurtha/search:
 *   post:
 *     tags: [Muhurtha]
 *     summary: Search for auspicious muhurtha
 *     description: Evaluates a date/time/location combination against all Vedic rules and returns a comprehensive muhurtha analysis including score, star rating, suitable/avoid windows, and bilingual explanations.
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/MuhurthaSearchRequest'
 *     responses:
 *       200:
 *         description: Muhurtha evaluation result
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/MuhurthaSearchResponse'
 *       400:
 *         description: Validation error
 */
router.post('/search', searchMuhurtha);

/**
 * @openapi
 * /api/muhurtha/details:
 *   post:
 *     tags: [Muhurtha]
 *     summary: Get deep granular muhurtha breakdown
 *     description: Returns a detailed rule-by-rule breakdown including all panchang elements, dosha analysis, strength analysis, and time window recommendations with full bilingual explanations.
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/MuhurthaSearchRequest'
 *     responses:
 *       200:
 *         description: Detailed muhurtha analysis
 */
router.post('/details', getMuhurthaDetails);

/**
 * @openapi
 * /api/muhurtha/ai:
 *   post:
 *     tags: [Muhurtha]
 *     summary: Get AI-optimized muhurtha JSON payload
 *     description: Returns a clean, structured, token-optimized JSON payload specifically formatted for OpenAI/GPT integration. Includes doshas, recommendations, and remedies.
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/MuhurthaAiRequest'
 *     responses:
 *       200:
 *         description: AI-optimized muhurtha payload
 */
router.post('/ai', getAiPayload);

export { router as muhurthaRouter };

export function registerWordPressCompatibleRoutes(appRouter: Router): void {
  appRouter.get('/wp-json/astrojyothi/v1/muhurtha/categories', getCategories);
  appRouter.post('/wp-json/astrojyothi/v1/muhurtha/search', searchMuhurtha);
  appRouter.post('/wp-json/astrojyothi/v1/muhurtha/details', getMuhurthaDetails);
  appRouter.post('/wp-json/astrojyothi/v1/muhurtha/ai', getAiPayload);
}
