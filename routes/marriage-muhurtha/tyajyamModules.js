/** மூன்று Tyajyam types. Ref: குருநாதர் பஞ்சாங்க குறிப்பு. 1 கடிகை = 24 நிமிடம். */

// 1. வார தியாஜ்யம்
const VAAR_TYAJYAM_NAZHIGAI = {0:32,1:42,2:31,3:42,4:31,5:21,6:14};
function checkVaarTyajyam(muhurthaTime, sunrise, weekdayIndex) {
  const start = new Date(new Date(sunrise).getTime() + VAAR_TYAJYAM_NAZHIGAI[weekdayIndex] * 24 * 60000);
  const end = new Date(start.getTime() + 90 * 60000);
  const t = new Date(muhurthaTime);
  const inWindow = t >= start && t < end;
  return {
    score: inWindow ? -3 : 0,
    tamilExplanation: inWindow ? "வார தியாஜ்யத்தில் உள்ளது." : "வார தியாஜ்யம் இல்லை.",
    source: "குருநாதர் பஞ்சாங்க குறிப்பு"
  };
}

// 2. திதி தியாஜ்யம்
const TITHI_TYAJYAM_START_GHATI = {
  "பிரதமை":14,"த்விதியை":22,"திரிதியை":29,"சதுர்த்தி":35,"பஞ்சமி":41,"ஷஷ்டி":46,
  "சப்தமி":52,"அஷ்டமி":57,"நவமி":3,"தசமி":9,"ஏகாதசி":15,"துவாதசி":21,
  "திரயோதசி":27,"சதுர்த்தசி":33,"பௌர்ணமி":39,"அமாவாசை":39
};
function checkTithiTyajyam(muhurthaTime, tithiName, tithiStartTime, tithiActualDurMin) {
  const g = TITHI_TYAJYAM_START_GHATI[tithiName];
  if (g === undefined) return { score: 0, tamilExplanation: "திதி பெயர் பொருந்தவில்லை.", source: "குருநாதர்" };
  const scale = tithiActualDurMin / 1440;
  const start = new Date(new Date(tithiStartTime).getTime() + (g * 24 * scale) * 60000);
  const end = new Date(start.getTime() + (4 * 24 * scale) * 60000);
  const t = new Date(muhurthaTime);
  const inWindow = t >= start && t < end;
  return {
    score: inWindow ? -5 : 0,
    tamilExplanation: inWindow ? "திதி தியாஜ்யத்தில் உள்ளது." : "திதி தியாஜ்யம் இல்லை.",
    source: "குருநாதர் பஞ்சாங்க குறிப்பு"
  };
}

// 3. நட்சத்திர வர்ஜ்யம்
const NAKSHATRA_VARJYAM_START_GHATI = {
  "அஸ்வினி":50,"பரணி":24,"கார்த்திகை":30,"ரோகிணி":40,"மிருகசீரிடம்":14,"திருவாதிரை":21,
  "புனர்பூசம்":30,"பூசம்":20,"ஆயில்யம்":32,"மகம்":30,"பூரம்":20,"உத்திரம்":18,
  "ஹஸ்தம்":21,"சித்திரை":20,"சுவாதி":14,"விசாகம்":14,"அனுஷம்":10,"கேட்டை":14,
  "மூலம்":20,"பூராடம்":24,"உத்திராடம்":20,"திருவோணம்":10,"அவிட்டம்":10,"சதயம்":18,
  "பூரட்டாதி":16,"உத்திரட்டாதி":24,"ரேவதி":30
};
function checkNakshatraVarjyam(muhurthaTime, nakshatraName, nakshatraStartTime, nakshatraActualDurMin) {
  const g = NAKSHATRA_VARJYAM_START_GHATI[nakshatraName];
  if (g === undefined) return { score: 0, tamilExplanation: "நட்சத்திரம் பொருந்தவில்லை.", source: "குருநாதர்" };
  const scale = nakshatraActualDurMin / 1440;
  const start = new Date(new Date(nakshatraStartTime).getTime() + (g * 24 * scale) * 60000);
  const end = new Date(start.getTime() + (4 * 24 * scale) * 60000);
  const t = new Date(muhurthaTime);
  const inWindow = t >= start && t < end;
  return {
    score: inWindow ? -8 : 0,
    tamilExplanation: inWindow ? "நட்சத்திர வர்ஜ்யத்தில் உள்ளது." : "நட்சத்திர வர்ஜ்யம் இல்லை.",
    source: "குருநாதர் பஞ்சாங்க குறிப்பு"
  };
}

module.exports = { checkVaarTyajyam, checkTithiTyajyam, checkNakshatraVarjyam };
