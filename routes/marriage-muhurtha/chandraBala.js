/** சந்திரபலம் — ஜென்ம ராசியிலிருந்து சந்திரன் நிலை. Ref: Muhurta Chintamani, Kalaprakashika, Muhurta Martanda. */
const HOUSE_SCORE = {1:10,3:10,6:10,7:10,10:10,11:10, 2:5,5:5,9:5, 4:-10,8:-10,12:-10};
function checkChandraBala(f) {
  let score = HOUSE_SCORE[f.chandraHouseFromJanmaRasi] || 0;
  const notes = [];
  if (f.isUcham) { score += 2; notes.push("சந்திரன் உச்சத்தில்"); }
  if (f.hasGuruDrishti) { score += 2; notes.push("குரு பார்வை உண்டு"); }
  if (f.hasPapaAffliction) { score -= 3; notes.push("பாப கிரக பாதிப்பு உண்டு"); }
  return {
    score,
    tamilExplanation: `சந்திரன் ${f.chandraHouseFromJanmaRasi}-ஆம் வீட்டில். ${notes.join(", ")}.`,
    source: "Muhurta Chintamani, Kalaprakashika, Muhurta Martanda"
  };
}
module.exports = { checkChandraBala };
