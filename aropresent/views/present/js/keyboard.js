window.addEventListener('keydown', (e) => {
  if (slides.length === 0) return;
  const activeEl = container.querySelector('.slide-view.active');
  const items = activeEl ? activeEl.querySelectorAll('.animate-item') : [];
  const animConfigs = parseConfigs(slides[index].animation);

  if (e.key === ' ' || e.key === 'ArrowRight') {
    if (animConfigs.text !== 'none' && textStep < items.length) {
      textStep++;
      showSlide();
    } else if (index < slides.length - 1) {
      index++;
      textStep = 0;
      showSlide();
    }
  } else if (e.key === 'Backspace' || e.key === 'ArrowLeft') {
    if (animConfigs.text !== 'none' && textStep > 0) {
      textStep--;
      showSlide();
    } else if (index > 0) {
      index--;
      const prevEl = container.querySelectorAll('.slide-view')[index];
      const prevItems = prevEl ? prevEl.querySelectorAll('.animate-item') : [];
      const prevConfigs = parseConfigs(slides[index].animation);
      textStep = prevConfigs.text !== 'none' ? prevItems.length : 0;
      showSlide();
    }
  } else if (e.key === 'Escape') {
    window.location.href = '/';
  }
});
