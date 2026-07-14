const { spawn } = require('child_process');
const express = require('express');
const router = express.Router();

/**
 * AstroSuite V8 API Router Endpoint
 * Route: POST /api/report
 */
router.post('/report', async (req, res) => {
    try {
        const { place = 'Vellore', date, time, mode = 'Research' } = req.body;

        if (!date || !time) {
            return res.status(400).json({ success: false, error: 'Missing date or time' });
        }

        // அசல் V8 பைதான் என்ஜினை இயக்குகிறோம் நண்பா
        const pyEngine = spawn('python3', [
            '/root/astrology_v8.py',
            place,
            date,
            time,
            '--mode', mode,
            '--json'
        ]);

        let stdOutput = '';
        let errOutput = '';

        pyEngine.stdout.on('data', (data) => { stdOutput += data.toString(); });
        pyEngine.stderr.on('data', (data) => { errOutput += data.toString(); });

        pyEngine.on('close', (code) => {
            if (code !== 0) {
                return res.status(500).json({ success: false, error: 'Python Engine Failure', details: errOutput });
            }
            try {
                const parsedData = JSON.parse(stdOutput);
                return res.status(200).json({ success: true, v8_core_sync: 'perfect', data: parsedData });
            } catch (jsonErr) {
                return res.status(500).json({ success: false, error: 'JSON Stream Parse Failure', raw: stdOutput });
            }
        });
    } catch (globalErr) {
        return res.status(500).json({ success: false, error: globalErr.message });
    }
});

// நீங்கள் சொன்ன கச்சிதமான எக்ஸ்போர்ட் ஃபார்மட் நண்பா!
module.exports = router;
