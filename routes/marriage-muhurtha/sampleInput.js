const sampleInput = {
  lagna: { rasi: "மேஷம்", degreeInRasi: 21 },

  lagnadhipati: {
    lagnaLord: "செவ்வாய்",
    lordInOwnExaltationFriendly: true,
    lordInKendraTrikona: true,
    papaAffliction: false,
    isCombust: false
  },

  nakshatra: { janma: "அஸ்வினி", muhurtha: "ரோகிணி", muhurthaPada: 2 },

  chandra: {
    chandraHouseFromJanmaRasi: 11,
    isUcham: false,
    hasGuruDrishti: true,
    hasPapaAffliction: false
  },

  seventhHouse: {
    lordUcham: false,
    lordSwakshetra: true,
    guruDrishti: true,
    sukraDrishti: false,
    subhaGrahaInHouse: true,
    severePapaAffliction: false,
    lordNeecham: false,
    lordIn6_8_12: false
  },

  venus: {
    ucham: false,
    swakshetra: true,
    vargottama: false,
    guruDrishti: true,
    astangatha: false,
    neecham: false
  },

  jupiter: {
    ucham: true,
    swakshetra: false,
    aspectsMarriageLagna1_5_7_9: true,
    neecham: false,
    papaGrahaConjunction: false
  },

  panchakaInputs: { seventhLordStrength: "strong", isPushkaraNavamsa: true },

  time: {
    sunrise: new Date("2026-07-14T00:09:00.000Z"),
    sunset: new Date("2026-07-14T13:03:00.000Z"),
    nextSunrise: new Date("2026-07-15T00:09:00.000Z"),
    muhurthaTime: new Date("2026-07-14T06:00:00.000Z"),
    weekdayIndex: 2,
    weekdayOffset: 2,
    tithiName: "பஞ்சமி",
    tithiStartTime: new Date("2026-07-13T18:30:00.000Z"),
    tithiActualDurMin: 1380,
    nakshatraStartTime: new Date("2026-07-13T20:00:00.000Z"),
    nakshatraActualDurMin: 1400,
    nakshatraNumber: 4
  },

  bride: { nakshatra: "பூசம்" },
  groom: { nakshatra: "மிருகசீரிடம்" },

  traditionAllowsAbhijitForMarriage: false,

  jaimini: {
    charaDashaConnectsToSeventh: true,
    charaDashaConnects6_8_12: false,
    darakarakaUcham: true,
    darakarakaSwakshetra: false,
    darakarakaNeecham: false,
    darakarakaPapaDrishti: false,
    ulSeventhGoodConnection: true,
    ulSubhaDrishti: true,
    ulPapaAffliction: false,
    padaLagnaKendraTrikonaWithUL: true,
    padaLagna6_8_12WithUL: false,
    subhaRasiDrishtiOn7th: true,
    papaRasiDrishtiOn7th: false,
    akDkKendraTrikona: true,
    akDk6_8: false,
    akDk2_12: false
  }
};

module.exports = sampleInput;
