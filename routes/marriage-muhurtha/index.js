const { checkPushkaraNavamsa } = require("./pushkaraNavamsa");
const { checkLagnadhipatiJeevan } = require("./navamsaLagnaStrength");
const { checkTaraBala } = require("./taraBala");
const { checkChandraBala } = require("./chandraBala");
const { checkSeventhHouse } = require("./seventhHouseStrength");
const { checkVenusStrength, checkJupiterStrength } = require("./venusJupiterStrength");
const { checkPanchaka } = require("./panchaka");
const { checkAbhijit } = require("./abhijitMuhurtha");
const { checkVedha } = require("./vedhaCheck");
const { checkHora } = require("./hora");
const { checkAnandadiYoga } = require("./anandadiYoga");
const { checkVaarTyajyam, checkTithiTyajyam, checkNakshatraVarjyam } = require("./tyajyamModules");
const { checkDurmuhurtha } = require("./durmuhurtha");
const { checkJaiminiRules } = require("./jaiminiRules");

function calculateMuhurthaScore(input) {
  const results = {
    pushkaraNavamsa: checkPushkaraNavamsa(input.lagna.rasi, input.lagna.degreeInRasi),
    lagnadhipatiJeevan: checkLagnadhipatiJeevan(input.lagnadhipati),
    taraBala: checkTaraBala(input.nakshatra.janma, input.nakshatra.muhurtha),
    chandraBala: checkChandraBala(input.chandra),
    seventhHouse: checkSeventhHouse(input.seventhHouse),
    venusStrength: checkVenusStrength(input.venus),
    jupiterStrength: checkJupiterStrength(input.jupiter),
    panchaka: checkPanchaka(
      input.nakshatra.muhurtha,
      input.nakshatra.muhurthaPada,
      input.panchakaInputs.seventhLordStrength,
      input.panchakaInputs.isPushkaraNavamsa
    ),
    abhijit: checkAbhijit(
      input.time.sunrise,
      input.time.sunset,
      input.time.muhurthaTime,
      input.traditionAllowsAbhijitForMarriage
    ),
    vedha: checkVedha(input.nakshatra.muhurtha, input.bride.nakshatra, input.groom.nakshatra),
    hora: checkHora(input.time.muhurthaTime, input.time.sunrise, input.time.nextSunrise, input.time.weekdayIndex),
    anandadiYoga: checkAnandadiYoga(input.time.weekdayOffset, input.time.nakshatraNumber),
    vaarTyajyam: checkVaarTyajyam(input.time.muhurthaTime, input.time.sunrise, input.time.weekdayIndex),
    tithiTyajyam: checkTithiTyajyam(
      input.time.muhurthaTime,
      input.time.tithiName,
      input.time.tithiStartTime,
      input.time.tithiActualDurMin
    ),
    nakshatraVarjyam: checkNakshatraVarjyam(
      input.time.muhurthaTime,
      input.nakshatra.muhurtha,
      input.time.nakshatraStartTime,
      input.time.nakshatraActualDurMin
    ),
    durmuhurtha: checkDurmuhurtha(input.time.muhurthaTime, input.time.sunrise, input.time.sunset, input.time.weekdayIndex),
    jaiminiRules: checkJaiminiRules(input.jaimini)
  };

  let coreScore = 0;
  let researchScore = 0;
  const coreBreakdown = [];
  const researchBreakdown = [];

  for (const [module, result] of Object.entries(results)) {
    const entry = { module, ...result };
    if (result.isResearchOnly) {
      researchScore += result.score;
      researchBreakdown.push(entry);
    } else {
      coreScore += result.score;
      coreBreakdown.push(entry);
    }
  }

  let verdict;
  if (coreScore >= 30) verdict = "மிகச் சிறந்த முஹூர்த்தம்";
  else if (coreScore >= 15) verdict = "நல்ல முஹூர்த்தம்";
  else if (coreScore >= 0) verdict = "சாதாரண முஹூர்த்தம் — கவனம் தேவை";
  else verdict = "தவிர்க்கப்பட வேண்டிய முஹூர்த்தம்";

  return {
    coreScore,
    researchScore,
    totalScore: coreScore + researchScore,
    verdict,
    coreBreakdown,
    researchBreakdown
  };
}

module.exports = { calculateMuhurthaScore };
