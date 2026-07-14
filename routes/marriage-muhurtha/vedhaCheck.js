/** நட்சத்திர வேதை — குருநாதர் guru-verified source. */
const VEDHA_MUTUAL_PAIRS = {
  "அஸ்வினி":"கேட்டை","கேட்டை":"அஸ்வினி",
  "பரணி":"அனுஷம்","அனுஷம்":"பரணி",
  "கிருத்திகை":"விசாகம்","விசாகம்":"கிருத்திகை",
  "ரோகிணி":"சுவாதி","சுவாதி":"ரோகிணி",
  "திருவாதிரை":"திருவோணம்","திருவோணம்":"திருவாதிரை",
  "புனர்பூசம்":"உத்திராடம்","உத்திராடம்":"புனர்பூசம்",
  "பூசம்":"பூராடம்","பூராடம்":"பூசம்",
  "ஆயில்யம்":"மூலம்","மூலம்":"ஆயில்யம்",
  "மகம்":"ரேவதி","ரேவதி":"மகம்",
  "பூரம்":"உத்திரட்டாதி","உத்திரட்டாதி":"பூரம்",
  "உத்திரம்":"பூரட்டாதி","பூரட்டாதி":"உத்திரம்",
  "அஸ்தம்":"சதயம்","சதயம்":"அஸ்தம்"
};
const CHEVVAI_TRIANGULAR_GROUP = ["மிருகசீரிடம்","சித்திரை","அவிட்டம்"];

function checkVedha(muhurthaNakshatra, brideNakshatra, groomNakshatra) {
  function isVedhaOf(nak, muh) {
    if (VEDHA_MUTUAL_PAIRS[nak] === muh) return true;
    if (CHEVVAI_TRIANGULAR_GROUP.includes(nak) && CHEVVAI_TRIANGULAR_GROUP.includes(muh) && nak !== muh) return true;
    return false;
  }
  let score = 0;
  const ex = [];
  if (isVedhaOf(groomNakshatra, muhurthaNakshatra)) {
    score -= 12;
    ex.push(`மணமகன் நட்சத்திரம் (${groomNakshatra}) வேதம்`);
  }
  if (isVedhaOf(brideNakshatra, muhurthaNakshatra)) {
    score -= 12;
    ex.push(`மணமகள் நட்சத்திரம் (${brideNakshatra}) வேதம்`);
  }
  return {
    score,
    tamilExplanation: ex.length ? ex.join(", ") + "." : "வேத தோஷம் இல்லை.",
    source: "குருநாதர் பஞ்சாங்க குறிப்பு"
  };
}
module.exports = { checkVedha, VEDHA_MUTUAL_PAIRS, CHEVVAI_TRIANGULAR_GROUP };
