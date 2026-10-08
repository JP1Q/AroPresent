function loadSlides() {
  fetch('/slides')
    .then(res => {
      if (!res.ok) throw new Error();
      return res.json();
    })
    .then(data => initPresentation(data))
    .catch(() => {
      const saved = localStorage.getItem('aropresent_slides');
      const savedAnims = localStorage.getItem('aropresent_anims');
      if (saved && savedAnims) {
        const rawSlides = JSON.parse(saved);
        const anims = JSON.parse(savedAnims);
        const pmd = rawSlides.map((s, i) => {
          const anim = anims[i] || 'none none';
          const prefix = anim === 'none none' ? '' : anim + '\n';
          return "{\n" + prefix + s + "\n}";
        }).join('\n');
        fetch('/render', { method: 'POST', body: pmd })
          .then(res => res.json())
          .then(data => initPresentation(data));
      } else {
        container.innerHTML = '<div class="slide-view active" style="text-align:center;">No slides found</div>';
      }
    });
}
