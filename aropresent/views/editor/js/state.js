let slides = [];
let animations = [];
let rendered = [];
let index = 0;
let textStep = 0;
let renderTimer = null;

let templates = {};

function parseConfigs(animStr) {
  const parts = animStr.split(' ');
  return {
    slide: parts[0] || 'none',
    text: parts[1] || 'none'
  };
}

function buildPmd() {
  return slides.map((s, i) => {
    const anim = animations[i] || 'none none';
    const prefix = anim === 'none none' ? '' : anim + '\n';
    return "{\n" + prefix + s + "\n}";
  }).join('\n');
}
