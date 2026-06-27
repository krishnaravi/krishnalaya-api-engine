import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { rateLimit } from 'express-rate-limit';
import { muhurthaRouter, registerWordPressCompatibleRoutes } from './modules/muhurtha/routes/muhurthaRoutes';
import { globalErrorHandler } from './modules/muhurtha/controllers/muhurthaController';

const app = express();

app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') ?? ['http://localhost:5173', 'http://localhost:3000'],
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-WP-Nonce'],
}));
app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ extended: true }));

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 200,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    success: false,
    error: {
      code: 'RATE_LIMIT_EXCEEDED',
      message: 'Too many requests. Please try again in 15 minutes.',
      messageTa: 'அதிக கோரிக்கைகள். 15 நிமிடங்களில் மீண்டும் முயற்சிக்கவும்.',
    },
  },
});

app.use('/api/', apiLimiter);

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'AstroJyothi Muhurtha Engine', version: '1.0.0' });
});

app.use('/api/muhurtha', muhurthaRouter);

registerWordPressCompatibleRoutes(app);

app.use(globalErrorHandler);

export default app;
