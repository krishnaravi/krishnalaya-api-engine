/** துர்முஹூர்த்தம் — பகல் 15 பாகங்கள். Ref: குருநாதர் பஞ்சாங்க குறிப்பு. */
const DURMUHURTHA_NUMBERS = {0:[14],1:[9,12],2:[4,10],3:[8],4:[6,12],5:[4,9],6:[1,2]};

function checkDurmuhurtha(muhurthaTime, sunrise, sunset, weekdayIndex) {
  const partLen = (new Date(sunset) - new Date(sunrise)) / 15;
  const nums = DURMUHURTHA_NUMBERS[weekdayIndex] || [];
  const t = new Date(muhurthaTime);
  const hit = nums.find(n => {
    const s = new Date(new Date(sunrise).getTime() + (n - 1) * partLen);
    return t >= s && t < new Date(s.getTime() + partLen);
  });
  return {
    score: hit ? -10 : 0,
    tamilExplanation: hit ? `${hit}-வது துர்முஹூர்த்தத்தில் முஹூர்த்தம் அமைந்துள்ளது.` : "துர்முஹூர்த்தம் இல்லை.",
    source: "குருநாதர் பஞ்சாங்க குறிப்பு"
  };
}
module.exports = { checkDurmuhurtha };
