/** ஆனந்தாதி யோகம் — 189-cell formula (4 நாள் guru-verified, 3 நாள் extrapolated). */
const ANANDADI_YOGA_LIST = [
  "ஆனந்த","காலதண்ட","தூம்ர","தாத்ரி","சௌம்ய","த்வாங்க்ஷ","த்வஜ",
  "ஸ்ரீவத்ஸ","வஜ்ர","முத்கர","சத்ர","மித்ர","மானச","பத்ம",
  "லம்ப","உத்பாத","மிருத்யு","கால","சித்த","சுப","அமிர்த",
  "முசல","கதா","மாதங்க","ராக்ஷச","சர","ஸ்திர","வர்த்தமான"
];
const YOGA_SCORE = {
  "ஆனந்த":5,"தாத்ரி":3,"சௌம்ய":3,"த்வஜ":3,"ஸ்ரீவத்ஸ":3,"மித்ர":3,"மானச":3,
  "பத்ம":3,"சித்த":3,"சுப":3,"அமிர்த":3,"மாதங்க":3,"ஸ்திர":3,"வர்த்தமான":3,
  "காலதண்ட":-5,"தூம்ர":-5,"த்வாங்க்ஷ":-5,"வஜ்ர":-5,"முத்கர":-5,"லம்ப":-5,
  "உத்பாத":-5,"கால":-5,"முசல":-5,"கதா":-5,"ராக்ஷச":-5,"மிருத்யு":-8
};

function checkAnandadiYoga(weekdayOffset, nakshatraNumber) {
  const idx = (weekdayOffset * 27 + (nakshatraNumber - 1)) % 28;
  const yogaName = ANANDADI_YOGA_LIST[idx];
  return {
    score: YOGA_SCORE[yogaName] || 0,
    yogaName,
    tamilExplanation: `${yogaName} யோகம் அமைந்துள்ளது.`,
    source: "குருநாதர் பஞ்சாங்க குறிப்பு (4 நாள் verified, 3 நாள் formula-extrapolated)"
  };
}
module.exports = { checkAnandadiYoga, ANANDADI_YOGA_LIST };
