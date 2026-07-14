/** ஜெயமினி விதிகள் — Research module (isResearchOnly:true), பாரம்பரிய முஹூர்த்த விதி அல்ல. Ref: Jaimini Sutras. */
function checkJaiminiRules(f) {
  const r = {
    charaDasha: f.charaDashaConnectsToSeventh ? 8 : (f.charaDashaConnects6_8_12 ? -8 : 0),
    daraKaraka: (f.darakarakaUcham || f.darakarakaSwakshetra) ? 8
      : (f.darakarakaNeecham ? -8 : (f.darakarakaPapaDrishti ? -5 : 0)),
    upapadaLagna: (f.ulSeventhGoodConnection ? 10 : 0) + (f.ulSubhaDrishti ? 5 : 0) + (f.ulPapaAffliction ? -8 : 0),
    padaLagna: f.padaLagnaKendraTrikonaWithUL ? 5 : (f.padaLagna6_8_12WithUL ? -5 : 0),
    rasiDrishti: f.subhaRasiDrishtiOn7th ? 5 : (f.papaRasiDrishtiOn7th ? -5 : 0),
    akDkRelation: f.akDkKendraTrikona ? 6 : (f.akDk6_8 ? -6 : (f.akDk2_12 ? -4 : 0))
  };
  const total = Object.values(r).reduce((s, v) => s + v, 0);
  return {
    score: total,
    maxScore: 10,
    subResults: r,
    isResearchOnly: true,
    tamilExplanation: "ஜெயமினி ஜோதிட ஆராய்ச்சி அடிப்படையிலான கூடுதல் மதிப்பீடு — பாரம்பரிய முஹூர்த்த விதி அல்ல.",
    source: "Jaimini Sutras (ஆராய்ச்சி பயன்பாடு)"
  };
}
module.exports = { checkJaiminiRules };
