import app from './app';

const PORT = parseInt(process.env.PORT ?? '4000', 10);
const HOST = process.env.HOST ?? '0.0.0.0';

const server = app.listen(PORT, HOST, () => {
  console.log(`[AstroJyothi] Muhurtha Engine running at http://${HOST}:${PORT}`);
  console.log(`[AstroJyothi] Environment: ${process.env.NODE_ENV ?? 'development'}`);
  console.log(`[AstroJyothi] Health: http://${HOST}:${PORT}/health`);
});

process.on('SIGTERM', () => {
  console.log('[AstroJyothi] SIGTERM received — graceful shutdown');
  server.close(() => {
    console.log('[AstroJyothi] HTTP server closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('[AstroJyothi] SIGINT received — graceful shutdown');
  server.close(() => process.exit(0));
});

export default server;
