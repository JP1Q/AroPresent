source.addEventListener('input', () => {
  if (slides.length === 0) {
    slides.push('');
    animations.push('none none');
    index = 0;
  }
  slides[index] = source.value;
  clearTimeout(renderTimer);
  renderTimer = setTimeout(renderSlides, 300);
});

transitionSelect.addEventListener('change', () => {
  if (slides.length === 0) return;
  const currentConfigs = parseConfigs(animations[index] || 'none none');
  animations[index] = transitionSelect.value + " " + currentConfigs.text;
  renderSlides();
});

textAnimSelect.addEventListener('change', () => {
  if (slides.length === 0) return;
  const currentConfigs = parseConfigs(animations[index] || 'none none');
  animations[index] = currentConfigs.slide + " " + textAnimSelect.value;
  renderSlides();
});

deleteBtn.addEventListener('click', () => {
  if (slides.length === 0) return;
  slides.splice(index, 1);
  animations.splice(index, 1);
  if (index >= slides.length) {
    index = Math.max(0, slides.length - 1);
  }
  source.value = slides[index] || '';
  renderSlides();
});
