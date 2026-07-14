/** புஷ்கர நவாம்சம் — Ref: BPHS, Jataka Parijata. குருநாதர் உறுதிசெய்தது. */
const PUSHKARA_NAVAMSA = {
  "மேஷம்":[7,9], "ரிஷபம்":[3,5], "மிதுனம்":[6,8], "கடகம்":[1,3],
  "சிம்மம்":[7,9], "கன்னி":[3,5], "துலாம்":[6,8], "விருச்சிகம்":[1,3],
  "தனுசு":[7,9], "மகரம்":[3,5], "கும்பம்":[6,8], "மீனம்":[1,3]
};
function getNavamsaNumber(degreeInRasi) { return Math.floor(degreeInRasi / 3.3333) + 1; }
function checkPushkaraNavamsa(rasi, degreeInRasi) {
  const navamsaNum = getNavamsaNumber(degreeInRasi);
  const isPushkara = PUSHKARA_NAVAMSA[rasi]?.includes(navamsaNum);
  return {
    score: isPushkara ? 10 : 0,
    navamsaNumber: navamsaNum,
    tamilExplanation: isPushkara ? "லக்னம் புஷ்கர நவாம்சத்தில் அமைந்துள்ளது — சுப பலம் அதிகரிக்கிறது." : "புஷ்கர நவாம்சம் இல்லை.",
    source: "BPHS, Jataka Parijata"
  };
}
module.exports = { checkPushkaraNavamsa, PUSHKARA_NAVAMSA };
