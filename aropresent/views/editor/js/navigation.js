prevBtn.addEventListener('click', () => {
  const items = slide.querySelectorAll('.animate-item');
  const currentConfigs = parseConfigs(animations[index] || 'none none');
  if (currentConfigs.text !== 'none' && textStep > 0) {
    textStep--;
    updateTextAnimations();
    prevBtn.disabled = index <= 0 && textStep <= 0;
    nextBtn.disabled = index >= slides.length - 1 && textStep >= items.length;
  } else if (index > 0) {
    index--;
    source.value = slides[index] || '';
    showSlide();
    const prevItems = slide.querySelectorAll('.animate-item');
    const prevConfigs = parseConfigs(animations[index] || 'none none');
    if (prevConfigs.text !== 'none') {
      textStep = prevItems.length;
      updateTextAnimations();
    }
    refreshList();
  }
});

nextBtn.addEventListener('click', () => {
  const items = slide.querySelectorAll('.animate-item');
  const currentConfigs = parseConfigs(animations[index] || 'none none');
  if (currentConfigs.text !== 'none' && textStep < items.length) {
    textStep++;
    updateTextAnimations();
    prevBtn.disabled = index <= 0 && textStep <= 0;
    nextBtn.disabled = index >= slides.length - 1 && textStep >= items.length;
  } else if (index < slides.length - 1) {
    index++;
    source.value = slides[index] || '';
    showSlide();
    refreshList();
  }
});

presentBtn.addEventListener('click', () => {
  window.open('/present', '_blank');
});
