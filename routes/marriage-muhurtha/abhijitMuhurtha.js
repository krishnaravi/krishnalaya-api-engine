/** அபிஜித் முஹூர்த்தம் — பகல் 15 பாகங்களில் 8வது. திருமணத்திற்கு default OFF (மரபு toggle). */
function checkAbhijit(sunrise, sunset, muhurthaTime, traditionAllowsForMarriage = false) {
  const partLen = (new Date(sunset) - new Date(sunrise)) / 15;
  const start = new Date(new Date(sunrise).getTime() + 7 * partLen);
  const end = new Date(new Date(sunrise).getTime() + 8 * partLen);
  const t = new Date(muhurthaTime);
  const inAbhijit = t >= start && t <= end;

  if (!inAbhijit) {
    return { score: 0, tamilExplanation: "அபிஜித் முஹூர்த்தம் அல்ல.", source: "குருநாதர் பஞ்சாங்க குறிப்பு" };
  }
  return {
    score: traditionAllowsForMarriage ? 3 : 0,
    tamilExplanation: traditionAllowsForMarriage
      ? "அபிஜித் முஹூர்த்தம் — மரபு அமைப்பின்படி ஏற்கத்தக்கது."
      : "அபிஜித் முஹூர்த்தம் — திருமணத்திற்கு பொதுவாக பயன்படுத்தப்படுவதில்லை.",
    isResearchOnly: !traditionAllowsForMarriage,
    source: "குருநாதர் பஞ்சாங்க குறிப்பு"
  };
}
module.exports = { checkAbhijit };
