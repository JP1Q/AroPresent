savePmdBtn.addEventListener('click', () => {
  const data = buildPmd();
  const blob = new Blob([data], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = (title.endsWith('.pmd') ? title : title + '.pmd');
  a.click();
});

loadPmdInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(evt) {
    fetch('/parse_raw', { method: 'POST', body: evt.target.result })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          alert(data.error);
          return;
        }
        slides = [];
        animations = [];
        (data.slides || []).forEach(s => {
          slides.push(s.content || '');
          animations.push(s.animation || 'none none');
        });
        index = 0;
        source.value = slides[index] || '';
        renderSlides();
      });
  };
  reader.readAsText(file);
});
