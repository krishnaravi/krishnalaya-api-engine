/** 7ஆம் பாவ பலம். Ref: BPHS, Phaladeepika, Saravali. */
function checkSeventhHouse(f) {
  let score = 0; const notes = [];
  if (f.lordUcham) { score += 5; notes.push("அதிபதி உச்சம்"); }
  if (f.lordSwakshetra) { score += 4; notes.push("அதிபதி சொந்த வீடு"); }
  if (f.guruDrishti) { score += 3; notes.push("குரு பார்வை"); }
  if (f.sukraDrishti) { score += 2; notes.push("சுக்கிரன் பார்வை"); }
  if (f.subhaGrahaInHouse) { score += 2; notes.push("சுபகிரகம் 7ல்"); }
  if (f.severePapaAffliction) { score -= 5; notes.push("⚠️ கடும் பாப பாதிப்பு"); }
  if (f.lordNeecham) { score -= 5; notes.push("⚠️ அதிபதி நீசம்"); }
  if (f.lordIn6_8_12) { score -= 4; notes.push("⚠️ அதிபதி 6/8/12ல்"); }
  return {
    score,
    maxScore: 15,
    tamilExplanation: notes.length ? notes.join(", ") + "." : "குறிப்பிடத்தக்க பலம்/தோஷம் இல்லை.",
    source: "BPHS, Phaladeepika, Saravali"
  };
}
module.exports = { checkSeventhHouse };
