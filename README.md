# AroPresent

Lightweight markdown-based presentation app for `.pmd` files. Slides are delimited by `{` and `}` on their own lines. Use space/right arrow to advance, backspace/left arrow to go back, and escape to exit.

## .pmd format

```
{
# Title

- Bullet one
- Bullet two :sparkles:
}
{
## Code

```python
print("hello")
```
}
```

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

## Run

```bash
python -m pip install -r requirements.txt
python main.py
```

## Web editor

Starts the local editor with a slide list, templates, and live preview. Use the Present button to open the presentation view.

```bash
python main.py --mode editor
```

### Slide templates

The editor's **Add Slide** menu is built from the Markdown files in `aropresent/slide_templates/`. The number sets the order and the rest is the name, so `4-two-columns.md` shows up fourth as "Two Columns Slide". Add, edit, or delete files there and refresh the editor.

## Present a .pmd file

```bash
python main.py --mode present example.pmd
```

## Parse-only check

```bash
python main.py --parse-only example.pmd
```
