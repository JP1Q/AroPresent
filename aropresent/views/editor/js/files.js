// Saved under the name of the .pmd the server was started with, or of the last loaded file.
let deckFileName = document.body.dataset.deckName || 'presentation';

// In the desktop app (pywebview) files go through native dialogs; in a browser, download/upload.
const hasDesktopApi = () => !!(window.pywebview && window.pywebview.api);

function loadPmdText(text) {
  fetch('/parse_raw', { method: 'POST', body: text })
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
}

savePmdBtn.addEventListener('click', async () => {
  const name = deckFileName.endsWith('.pmd') ? deckFileName : deckFileName + '.pmd';
  if (hasDesktopApi()) {
    const result = await window.pywebview.api.save_pmd(buildPmd(), name);
    if (result && result.error) alert(result.error);
    else if (result && result.name) deckFileName = result.name;
    return;
  }
  const blob = new Blob([buildPmd()], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
});

// The file input is only used in the browser; the desktop app opens a native dialog instead.
loadPmdInput.addEventListener('click', async (e) => {
  if (!hasDesktopApi()) return;
  e.preventDefault();
  const result = await window.pywebview.api.open_pmd();
  if (!result) return;
  if (result.error) {
    alert(result.error);
    return;
  }
  deckFileName = result.name;
  loadPmdText(result.text);
});

loadPmdInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (!file) return;
  deckFileName = file.name;
  e.target.value = '';  // allow loading the same file again
  const reader = new FileReader();
  reader.onload = evt => loadPmdText(evt.target.result);
  reader.readAsText(file);
});
