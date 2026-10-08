// Scale the fixed 1200x675 slide to fill the window, keeping a 40px margin.
function fitStage() {
  const scale = Math.min((window.innerWidth - 80) / 1200, (window.innerHeight - 80) / 675);
  container.style.setProperty('--slide-scale', scale);
}

window.addEventListener('resize', fitStage);
fitStage();
