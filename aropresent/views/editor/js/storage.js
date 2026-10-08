function saveToLocal() {
  localStorage.setItem('aropresent_slides', JSON.stringify(slides));
  localStorage.setItem('aropresent_anims', JSON.stringify(animations));
}

function loadFromLocal() {
  const saved = localStorage.getItem('aropresent_slides');
  const savedAnims = localStorage.getItem('aropresent_anims');
  if (saved && savedAnims) {
    slides = JSON.parse(saved);
    animations = JSON.parse(savedAnims);
  } else {
    const first = templateSelect.options[1];
    slides = [first ? templates[first.value] : ''];
    animations = ['none none'];
  }
  index = 0;
  source.value = slides[index] || '';
  renderSlides();
}
