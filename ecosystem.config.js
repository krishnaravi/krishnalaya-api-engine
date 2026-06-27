/**
 * PM2 Ecosystem Configuration for AstroJyothi Muhurtha Engine
 * Usage: pm2 start ecosystem.config.js [--env production]
 */

module.exports = {
  apps: [
    {
      name: 'astrojyothi-muhurtha',
      script: './dist/server.js',
      cwd: '/var/www/astrojyothi/backend',
      instances: 'max',
      exec_mode: 'cluster',
      watch: false,
      max_memory_restart: '512M',

      env: {
        NODE_ENV: 'development',
        PORT: 4000,
        ALLOWED_ORIGINS: 'http://localhost:5173,http://localhost:3000',
        LOG_LEVEL: 'debug',
      },

      env_production: {
        NODE_ENV: 'production',
        PORT: 4000,
        ALLOWED_ORIGINS: 'https://astrojyothi.com,https://www.astrojyothi.com',
        LOG_LEVEL: 'warn',
      },

      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      out_file: '/var/log/astrojyothi/muhurtha-out.log',
      error_file: '/var/log/astrojyothi/muhurtha-error.log',
      merge_logs: true,

      exp_backoff_restart_delay: 100,
      max_restarts: 10,
      min_uptime: '10s',

      kill_timeout: 5000,
      listen_timeout: 8000,

      autorestart: true,

      node_args: '--max-old-space-size=512 --enable-source-maps',
    },

    {
      name: 'astrojyothi-frontend',
      script: 'serve',
      args: '-s dist -l 5173',
      cwd: '/var/www/astrojyothi/frontend',
      instances: 1,
      exec_mode: 'fork',
      watch: false,
      env_production: {
        NODE_ENV: 'production',
      },
      out_file: '/var/log/astrojyothi/frontend-out.log',
      error_file: '/var/log/astrojyothi/frontend-error.log',
    },
  ],

  deploy: {
    production: {
      user: 'astrojyothi',
      host: ['your-server-ip'],
      ref: 'origin/main',
      repo: 'git@github.com:yourorg/astrojyothi.git',
      path: '/var/www/astrojyothi',
      'pre-deploy-local': '',
      'post-deploy':
        'cd backend && npm ci --production && npm run build && pm2 reload ecosystem.config.js --env production && cd ../frontend && npm ci && npm run build',
      'pre-setup': '',
    },
  },
};
