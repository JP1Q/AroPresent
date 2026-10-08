function renderSlides() {
  if (slides.length === 0) {
    rendered = [];
    slide.innerHTML = "";
    slideList.innerHTML = "";
    counter.textContent = "0 / 0";
    prevBtn.disabled = true;
    nextBtn.disabled = true;
    return;
  }
  fetch('/render', { method: 'POST', body: buildPmd() })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        rendered = [];
        slide.textContent = data.error;
        counter.textContent = '';
        prevBtn.disabled = true;
        nextBtn.disabled = true;
        return;
      }
      rendered = data.slides || [];
      saveToLocal();
      showSlide();
      refreshList();
    });
}

function showSlide() {
  if (rendered[index]) {
    slide.innerHTML = rendered[index].html;
    const animConfigs = parseConfigs(animations[index] || 'none none');
    slide.className = "slide-view " + animConfigs.slide + " " + animConfigs.text;
    slide.style = "overflow: hidden;"

    const items = slide.querySelectorAll('li, p, pre, h1, h2, h3, img');
    items.forEach((el) => el.classList.add('animate-item'));

    if (animConfigs.text === 'none') {
      items.forEach(el => el.classList.add('animated-visible'));
      textStep = items.length;
    } else {
      textStep = 0;
      updateTextAnimations();
    }
  } else {
    slide.innerHTML = "";
    slide.className = "slide-view none none no-over";
    slide.style = "background: red"
    textStep = 0;
  }
  counter.textContent = slides.length ? (index + 1) + " / " + slides.length : "0 / 0";
  prevBtn.disabled = index <= 0 && textStep <= 0;
  nextBtn.disabled = index >= slides.length - 1 && (rendered[index] ? textStep >= slide.querySelectorAll('.animate-item').length : true);

  const currentConfigs = parseConfigs(animations[index] || 'none none');
  transitionSelect.value = currentConfigs.slide;
  textAnimSelect.value = currentConfigs.text;
}

function updateTextAnimations() {
  const items = slide.querySelectorAll('.animate-item');
  items.forEach((el, i) => {
    if (i < textStep) {
      el.classList.add('animated-visible');
    } else {
      el.classList.remove('animated-visible');
    }
  });
}

function refreshList() {
  slideList.innerHTML = '';
  slides.forEach((s, i) => {
    const div = document.createElement('div');
    div.className = 'slide-thumb' + (i === index ? ' active' : '');
    div.textContent = "Slide " + (i + 1);
    div.addEventListener('click', () => {
      index = i;
      source.value = slides[index] || '';
      showSlide();
      refreshList();
    });
    slideList.appendChild(div);
  });
}
