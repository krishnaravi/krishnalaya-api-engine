/** ஜீவன் — லக்னாதிபதி பலம். Ref: BPHS Shadbala. Threshold குருநாதர் உறுதி செய்ய வேண்டும். */
function checkLagnadhipatiJeevan(f) {
  const checks = {
    rasiBala: f.lordInOwnExaltationFriendly ? "pass" : "fail",
    sthanaBala: f.lordInKendraTrikona ? "pass" : "fail",
    papaKartariDosha: !f.papaAffliction ? "pass" : "fail",
    combustion: !f.isCombust ? "pass" : "fail"
  };
  const passCount = Object.values(checks).filter(c => c === "pass").length;
  const lines = [];
  lines.push(checks.rasiBala === "pass" ? `${f.lagnaLord} நல்ல ராசிபலத்துடன் உள்ளார்` : `${f.lagnaLord} பலவீனமான ராசியில் உள்ளார்`);
  if (checks.sthanaBala === "pass") lines.push("கேந்திர/திரிகோண ஸ்தானத்தில் நல்ல நிலை");
  if (checks.papaKartariDosha !== "pass") lines.push("⚠️ பாபகிரக தொடர்பு உள்ளது");
  if (checks.combustion !== "pass") lines.push("⚠️ அஸ்தங்கத தோஷம் உள்ளது");
  return {
    score: passCount >= 3 ? 8 : -4,
    checks, tamilExplanation: lines.join(". ") + ".",
    source: "BPHS Shadbala அத்தியாயம் (threshold குருநாதர் உறுதி pending)"
  };
}
module.exports = { checkLagnadhipatiJeevan };
