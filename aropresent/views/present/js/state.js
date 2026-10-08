const container = document.getElementById('presentation');
let slides = [];
let index = 0;
let textStep = 0;

function parseConfigs(animStr) {
  const parts = (animStr || 'none none').split(' ');
  return {
    slide: parts[0] || 'none',
    text: parts[1] || 'none'
  };
}
