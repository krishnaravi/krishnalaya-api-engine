const express = require('express');
const { calculateMuhurthaScore } = require('./index');
const sampleInput = require('./sampleInput');

const router = express.Router();

router.post('/calculate', (req, res) => {
  const input = req.body;
  if (!input || typeof input !== 'object' || Array.isArray(input)) {
    return res.status(400).json({ success: false, error: '`input` object தேவை' });
  }
  try {
    const result = calculateMuhurthaScore(input);
    res.json({ success: true, data: result });
  } catch (e) {
    res.status(400).json({ success: false, error: e.message });
  }
});

router.get('/sample', (_req, res) => {
  res.json({ success: true, data: sampleInput });
});

module.exports = router;
