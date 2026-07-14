/** ஹோரா — Chaldean order. Ref: Hora Ratnam, Kalaprakashika. */
const CHALDEAN_ORDER = ["சனி","குரு","செவ்வாய்","சூரியன்","சுக்கிரன்","புதன்","சந்திரன்"];
const WEEKDAY_LORD = {0:"சூரியன்",1:"சந்திரன்",2:"செவ்வாய்",3:"புதன்",4:"குரு",5:"சுக்கிரன்",6:"சனி"};
const HORA_SCORE = {"குரு":5,"சுக்கிரன்":5,"சந்திரன்":3,"புதன்":2,"சூரியன்":-2,"செவ்வாய்":-4,"சனி":-5};

function getHoraTimeline(sunrise, nextSunrise, weekdayIndex) {
  const startIdx = CHALDEAN_ORDER.indexOf(WEEKDAY_LORD[weekdayIndex]);
  const horaLen = (new Date(nextSunrise) - new Date(sunrise)) / 24;
  return Array.from({ length: 24 }, (_, i) => {
    const start = new Date(new Date(sunrise).getTime() + i * horaLen);
    return { lord: CHALDEAN_ORDER[(startIdx + i) % 7], start, end: new Date(start.getTime() + horaLen) };
  });
}

function checkHora(muhurthaTime, sunrise, nextSunrise, weekdayIndex) {
  const t = new Date(muhurthaTime);
  const timeline = getHoraTimeline(sunrise, nextSunrise, weekdayIndex);
  const active = timeline.find(h => t >= h.start && t < h.end);
  if (!active) return { score: 0, tamilExplanation: "ஹோரை கண்டறிய முடியவில்லை.", source: "Hora Ratnam, Kalaprakashika" };
  return {
    score: HORA_SCORE[active.lord] || 0,
    lord: active.lord,
    tamilExplanation: `${active.lord} ஹோரையில் முஹூர்த்தம் அமைந்துள்ளது.`,
    source: "Hora Ratnam, Kalaprakashika"
  };
}
module.exports = { getHoraTimeline, checkHora };
