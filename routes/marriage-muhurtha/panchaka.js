/** பஞ்சக தோஷம் — அவிட்டம்(3,4)/சதயம்/பூரட்டாதி/உத்திரட்டாதி/ரேவதி. Ref: Muhurta Chintamani, Dharma Sindhu. */
const PANCHAKA_SET = ["அவிட்டம்_3","அவிட்டம்_4","சதயம்","பூரட்டாதி","உத்திரட்டாதி","ரேவதி"];

function checkPanchaka(chandraNakshatra, chandraPada, seventhLordStrength, isPushkaraNavamsa) {
  const key = chandraNakshatra === "அவிட்டம்" ? `அவிட்டம்_${chandraPada}` : chandraNakshatra;
  if (!PANCHAKA_SET.includes(key)) {
    return { score: 0, tamilExplanation: "பஞ்சக தோஷம் இல்லை.", source: "Muhurta Chintamani, Dharma Sindhu" };
  }
  let score = -5;
  let msg = "சந்திரன் பஞ்சக காலத்தில் உள்ளார்";
  if (seventhLordStrength === "weak") {
    score = -10;
    msg += " + 7ஆம் அதிபதி பலவீனம்";
  } else if (isPushkaraNavamsa) {
    score = -2;
    msg += " ஆனால் புஷ்கர நவாம்சத்தால் தீவிரம் குறைந்துள்ளது";
  }
  return { score, tamilExplanation: msg + ".", source: "Muhurta Chintamani, Dharma Sindhu" };
}
module.exports = { checkPanchaka };
