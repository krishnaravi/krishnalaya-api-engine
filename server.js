const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const { exec } = require('child_process'); // 👈 பைதான் ஸ்கிரிப்டை இயக்க
const app = express();

// JSON பாடி ரிக்வெஸ்ட்டுகளை ஏற்க
app.use(express.json());
app.set('trust proxy', 1);

const PORT = process.env.PORT || 3003; 
const TARGET_BACKEND = 'http://127.0.0.1:8000'; // அசல் பைதான் சர்வர்

// ── ரேட் லிமிட்டிங் ──
const ipRequestCounts = new Map();
setInterval(() => ipRequestCounts.clear(), 15 * 60 * 1000);
app.use((req, res, next) => {
  const ip = req.ip;
  const count = ipRequestCounts.get(ip) || 0;
  if (count >= 100) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  ipRequestCounts.set(ip, count + 1);
  next();
});

// ── ரூட் எண்ட் பாயிண்ட் ──
app.get('/', (req, res) => {
  res.json({ status: 'success', name: 'Krishnalaya Astrology API Gateway' });
});

// ── K.P. Astrology எண்ட் பாயிண்ட் (நேரடியாக பைதான் ஸ்கிரிப்டை இயக்குகிறது) ──
app.post('/api/kp-astrology', (req, res) => {
  const { year, month, day, hour, minute, lat, lon } = req.body;

  // வேலிடேஷன்
  if (!year || !month || !day || hour === undefined || minute === undefined || !lat || !lon) {
    return res.status(400).json({ error: "Missing required parameters" });
  }

  // நாம் உருவாக்கிய kp_astrology.py கோப்பை arguments உடன் இயக்குகிறோம்
  const pythonCommand = `python3 /root/kp_astrology.py ${year} ${month} ${day} ${hour} ${minute} ${lat} ${lon}`;

  exec(pythonCommand, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ error: error.message });
    }
    try {
      const data = JSON.parse(stdout);
      res.json(data);
    } catch (e) {
      res.status(500).json({ error: "Failed to parse astrology data", details: stdout });
    }
  });
});

// ── பஞ்சாங்கம் பிராக்சி ──
app.use('/api/panchangam', createProxyMiddleware({
  target: TARGET_BACKEND,
  changeOrigin: true,
  pathRewrite: { '^/api/panchangam': '/api/v1/panchangam' },
  onError: (err, req, res) => {
    res.status(500).json({ error: 'Proxy to Panchangam service failed' });
  }
}));

// ── பஞ்சபக்ஷி பிராக்சி ──
app.use('/api/panchapakshi', createProxyMiddleware({
  target: TARGET_BACKEND,
  changeOrigin: true,
  pathRewrite: { '^/api/panchapakshi': '/api/v1/panchapakshi' },
  onError: (err, req, res) => {
    res.status(500).json({ error: 'Proxy to Pancha Pakshi service failed' });
  }
}));

// ── சர்வர் துவக்கம் ──
app.listen(PORT, () => {
  console.log(`API Gateway is running on port ${PORT}`);
});
