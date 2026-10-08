// Drag the dividers between panels to resize them, like a video editor.
// Double-click a divider to reset it. Sizes are remembered in this browser.
const layout = document.querySelector('main');
const PANEL_SIZES_KEY = 'aropresent_panel_sizes';
const MIN_PREVIEW_WIDTH = 240;

const panels = {
  sidebar: { variable: '--sidebar-width', element: document.querySelector('aside'), min: 140, max: () => 480 },
  editor: {
    variable: '--editor-width',
    element: document.querySelector('.editor-col'),
    min: 200,
    max: () => layout.clientWidth - panels.sidebar.element.offsetWidth - MIN_PREVIEW_WIDTH,
  },
};

function setPanelWidth(name, width) {
  const panel = panels[name];
  const clamped = Math.max(panel.min, Math.min(panel.max(), width));
  layout.style.setProperty(panel.variable, clamped + 'px');
  return clamped;
}

function readPanelSizes() {
  try {
    return JSON.parse(localStorage.getItem(PANEL_SIZES_KEY)) || {};
  } catch {
    return {};
  }
}

function savePanelSize(name, width) {
  const sizes = readPanelSizes();
  if (width === null) {
    delete sizes[name];
  } else {
    sizes[name] = width;
  }
  try {
    localStorage.setItem(PANEL_SIZES_KEY, JSON.stringify(sizes));
  } catch {}
}

document.querySelectorAll('.resizer').forEach((resizer) => {
  const name = resizer.dataset.panel;
  const panel = panels[name];

  resizer.addEventListener('pointerdown', (e) => {
    e.preventDefault();
    resizer.setPointerCapture(e.pointerId);
    resizer.classList.add('dragging');
    document.body.classList.add('resizing');
  });

  resizer.addEventListener('pointermove', (e) => {
    if (!resizer.hasPointerCapture(e.pointerId)) return;
    setPanelWidth(name, e.clientX - panel.element.getBoundingClientRect().left);
  });

  resizer.addEventListener('pointerup', (e) => {
    resizer.releasePointerCapture(e.pointerId);
    resizer.classList.remove('dragging');
    document.body.classList.remove('resizing');
    savePanelSize(name, panel.element.offsetWidth);
  });

  resizer.addEventListener('dblclick', () => {
    layout.style.removeProperty(panel.variable);
    savePanelSize(name, null);
  });
});

Object.entries(readPanelSizes()).forEach(([name, width]) => {
  if (panels[name]) setPanelWidth(name, width);
});
