/** சுக்கிரன்/குரு பலம். Ref: BPHS, Phaladeepika, Saravali. */
function checkVenusStrength(f) {
  let score = 0; const notes = [];
  if (f.ucham) { score += 5; notes.push("உச்சம்"); }
  if (f.swakshetra) { score += 4; notes.push("சொந்த வீடு"); }
  if (f.vargottama) { score += 2; notes.push("வர்கோத்தமம்"); }
  if (f.guruDrishti) { score += 2; notes.push("குரு பார்வை"); }
  if (f.astangatha) { score -= 3; notes.push("⚠️ அஸ்தங்கதம்"); }
  if (f.neecham) { score -= 5; notes.push("⚠️ நீசம்"); }
  return {
    score,
    tamilExplanation: notes.length ? notes.join(", ") + "." : "குறிப்பிடத்தக்க பலம்/தோஷம் இல்லை.",
    source: "BPHS, Phaladeepika"
  };
}

function checkJupiterStrength(f) {
  let score = 0; const notes = [];
  if (f.ucham) { score += 5; notes.push("உச்சம்"); }
  if (f.swakshetra) { score += 4; notes.push("சொந்த வீடு"); }
  if (f.aspectsMarriageLagna1_5_7_9) { score += 3; notes.push("1/5/7/9 பார்வை"); }
  if (f.neecham) { score -= 5; notes.push("⚠️ நீசம்"); }
  if (f.papaGrahaConjunction) { score -= 3; notes.push("⚠️ பாபகிரக இணைவு"); }
  return {
    score,
    tamilExplanation: notes.length ? notes.join(", ") + "." : "குறிப்பிடத்தக்க பலம்/தோஷம் இல்லை.",
    source: "BPHS, Saravali"
  };
}
module.exports = { checkVenusStrength, checkJupiterStrength };
