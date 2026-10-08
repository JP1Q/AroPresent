function showSlide() {
  const elements = container.querySelectorAll('.slide-view');
  elements.forEach((el, i) => {
    if (i === index) {
      el.classList.add('active');
      const animConfigs = parseConfigs(slides[index].animation);
      const items = el.querySelectorAll('.animate-item');

      if (animConfigs.text === 'none') {
        items.forEach(item => item.classList.add('animated-visible'));
        textStep = items.length;
      } else {
        items.forEach((item, k) => {
          if (k < textStep) {
            item.classList.add('animated-visible');
          } else {
            item.classList.remove('animated-visible');
          }
        });
      }
    } else {
      el.classList.remove('active');
    }
  });
}

function initPresentation(data) {
  slides = data.slides || [];
  if (slides.length === 0) {
    container.innerHTML = '<div class="slide-view active" style="text-align:center;">No slides to display</div>';
    return;
  }
  container.innerHTML = '';
  slides.forEach((slide) => {
    const div = document.createElement('div');
    const animConfigs = parseConfigs(slide.animation);
    div.className = "slide-view " + animConfigs.slide + " " + animConfigs.text;
    div.innerHTML = slide.html;

    const items = div.querySelectorAll('li, p, pre, h1, h2, h3, img');
    items.forEach(el => el.classList.add('animate-item'));

    container.appendChild(div);
  });
  index = 0;
  textStep = 0;
  showSlide();
}
