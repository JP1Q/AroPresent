# AroPresent

Lightweight markdown-based presentation app for `.pmd` files. Slides are delimited by `{` and `}` on their own lines. Use space/right arrow to advance, backspace/left arrow to go back, and escape to exit.

## .pmd format

````
{
# Title

- Bullet one
- Bullet two :sparkles:
}
{ fade anim-pop
## Code

```python
print("hello")
```
}
````

Anything after the `{` sets the slide's transitions: first how the slide appears, then how its items appear one by one.

| Slide transition | Text animation |
| --- | --- |
| `fade`, `popup`, `slide-right` | `anim-fade`, `anim-pop`, `anim-right` |

`{ popup` alone sets just the slide transition. With a text animation, each press of space/right arrow reveals the next item before moving to the next slide.

## Commands

Each command goes on its own line inside a slide. Commands inside code blocks are left alone.

| Command | What it does |
| --- | --- |
| `\col1`, `\col2`, ... | Start a column; the slide (or box) is split into equal columns. See [Columns](#columns) |
| `\d` | Start a styled box. See [Styled boxes](#styled-boxes) |
| `\end` | Close the current box (optional at the end of a slide) |
| `\fontsize{N}` | Text size in pixels at presentation size (36 is normal) |
| `\color{red}` | Text color (any CSS color) |
| `\bg{#222}` | Background color |
| `\align{center}` | Text alignment: `left`, `center`, `right` |
| `\style{...}` | Any CSS, e.g. `\style{border: 1px solid; padding: 8px}` |

Style commands apply to the box they're in; outside a box they apply to the current column, or to the whole slide.

## Emoticons

Use GitHub-style aliases like `:smile:` or `:sparkles:`. They are converted to emojis.

## Images

Images shrink automatically to fit inside the slide. To set a size, add attributes after the image:

```
![Logo](logo.png){ width=300 }
![Chart](chart.png){ width=50% }
![Photo](photo.jpg){ style="height:200px" }
```

## Columns

Put `\col1`, `\col2`, ... on their own lines to split a slide into columns. Anything before the first marker (like the title) stays full width above them.

```
{
## Pros and cons

\col1
- Fast
- Light

\col2
- No undo
- Dark mode only
}
```

## Styled boxes

`\d` starts a box and `\end` closes it. Style lines apply to the box they're in, or to the whole slide or a column when used outside a box:

```
{
# Cats

\d
\fontsize{20}
\color{orange}
I LIKE CATS YK
\end

Normal text again.
}
```

The style commands are listed under [Commands](#commands).

Boxes can be nested, and `\col1`, `\col2`, ... inside a box split that box into columns.

## Run

```bash
python -m pip install -r requirements.txt
python main.py
```

## Web editor

Starts the local editor with a slide list, templates, and live preview. Use the Present button to open the presentation view.

Drag the dividers between the panels to resize them; double-click a divider to reset it. Hover the **?** button in the top right for a quick reference of the commands.

```bash
python main.py --mode editor
```

### Slide templates

The editor's **Add Slide** menu is built from the Markdown files in `aropresent/slide_templates/`. Their order and menu labels come from `templates.json` in the same folder:

```json
[
  { "file": "empty.md", "label": "Empty Slide" },
  { "file": "title.md", "label": "Title Slide" }
]
```

To add a template, create the `.md` file and add a line for it to `templates.json`; to reorder, move the lines. Refresh the editor to see changes.

## Present a .pmd file

```bash
python main.py --mode present example.pmd
```

## Parse-only check

```bash
python main.py --parse-only example.pmd
```
