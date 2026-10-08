// Scale the fixed 1200x675 slide to the preview's current width.
const previewScreen = document.querySelector('.preview-screen');

new ResizeObserver(() => {
  previewScreen.style.setProperty('--slide-scale', previewScreen.clientWidth / 1200);
}).observe(previewScreen);
