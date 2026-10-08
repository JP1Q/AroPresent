templateSelect.addEventListener('change', () => {
  const val = templateSelect.value;
  if (!val) return;
  const content = templates[val] || '';
  slides.push(content);
  animations.push('none none');
  index = slides.length - 1;
  source.value = content;
  templateSelect.value = '';
  renderSlides();
});

function loadTemplates() {
  return fetch('/slide_templates')
    .then(res => res.json())
    .then(data => {
      (data.templates || []).forEach(t => {
        templates[t.id] = t.content;
        templateSelect.add(new Option(t.label, t.id));
      });
    })
    .catch(() => {});
}
