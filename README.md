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

## Present a .pmd file

```bash
python main.py --mode present example.pmd
```

## Parse-only check

```bash
python main.py --parse-only example.pmd
```
