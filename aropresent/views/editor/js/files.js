// Saved under the name of the .pmd the server was started with, or of the last loaded file.
let deckFileName = document.body.dataset.deckName || 'presentation';

savePmdBtn.addEventListener('click', () => {
  const blob = new Blob([buildPmd()], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = deckFileName.endsWith('.pmd') ? deckFileName : deckFileName + '.pmd';
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
});

loadPmdInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (!file) return;
  deckFileName = file.name;
  e.target.value = '';  // allow loading the same file again
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
