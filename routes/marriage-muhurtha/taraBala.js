/** தாரபலன் — ஜென்ம நட்சத்திரத்திலிருந்து எண்ணும் Tara classification. Ref: குருநாதர் பஞ்சாங்க குறிப்பு. */
const NAKSHATRAS = ["அஸ்வினி","பரணி","கிருத்திகை","ரோகிணி","மிருகசீரிடம்","திருவாதிரை","புனர்பூசம்","பூசம்","ஆயில்யம்","மகம்","பூரம்","உத்திரம்","ஹஸ்தம்","சித்திரை","சுவாதி","விசாகம்","அனுஷம்","கேட்டை","மூலம்","பூராடம்","உத்திராடம்","திருவோணம்","அவிட்டம்","சதயம்","பூரட்டாதி","உத்திரட்டாதி","ரேவதி"];
const GOOD_TARA_NUMBERS = [2,4,6,8,9,11,13,15,17,18,19,20,22,24,26,27];

function checkTaraBala(janmaNakshatra, muhurthaNakshatra) {
  const jIdx = NAKSHATRAS.indexOf(janmaNakshatra);
  const mIdx = NAKSHATRAS.indexOf(muhurthaNakshatra);
  let count = (mIdx - jIdx + 27) % 27 + 1;
  const isGood = GOOD_TARA_NUMBERS.includes(count);
  return {
    score: isGood ? 10 : -6,
    taraNumber: count,
    tamilExplanation: isGood
      ? `முஹூர்த்த நட்சத்திரம் ஜென்ம நட்சத்திரத்திலிருந்து ${count}-வது தாரையாக நல்ல தாரையில் அமைந்துள்ளது.`
      : `${count}-வது தாரை நல்ல தாரை பட்டியலில் இல்லை — கவனம் தேவை.`,
    source: "குருநாதர் பஞ்சாங்க குறிப்பு (அஸ்வினி அடிப்படை)"
  };
}
module.exports = { checkTaraBala, NAKSHATRAS };
