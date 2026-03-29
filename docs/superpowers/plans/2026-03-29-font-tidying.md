# Font Tidying Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace ad-hoc `ImageFont` usage with a two-level registry (font families + named presets) so that `text()` and `html()` both accept `font='preset_name'`.

**Architecture:** `font_families()` registers family names to file paths; `font_name()` registers named presets combining a family and size (in the default unit). `text()` and `html()` look up the preset, resolve it to an `ImageFont` or CSS, and cache the PIL font object inside `_font_names`.

**Tech Stack:** Python 3.12, Pillow (`ImageFont`, `ImageDraw`), pytest.

---

## Files

- Modify: `gamehelper/card_maker.py` — all font-related changes
- Modify: `tests/test_card_maker.py` — update `TestFontFamilies`, `TestText`; add `TestFontName`

---

### Task 1: Update `font_families()` to accept a list of dicts

`font_families()` currently takes a plain `dict[str, str]`. Change it to accept
`list[dict]` and store each family's data as a dict (without the `family` key).
Also fix `html()`'s `@font-face` loop which currently iterates over
`_font_families` as `(name, path)` — it must now use `(name, data)`.

**Files:**
- Modify: `gamehelper/card_maker.py`
- Modify: `tests/test_card_maker.py` (lines 816–841)

- [ ] **Step 1: Write failing tests**

Replace the body of `TestFontFamilies` in `tests/test_card_maker.py`:

```python
class TestFontFamilies:
    """Tests for font_families()."""

    def test_copy_preserves_font_families(self):
        """Copying a CardMaker should preserve the font families."""
        maker = CardMaker(width    = 100,
                          height   = 100,
                          unit     = 'mm',
                          width_px = 200,
                          )
        maker.font_families([{'family': 'MyFont', 'file': '/path/to/font.ttf'}])
        dup = maker.copy()
        assert dup._font_families == {'MyFont': {'file': '/path/to/font.ttf'}}

    def test_copy_font_families_are_independent(self):
        """Changing font families on a copy should not affect the original."""
        maker = CardMaker(width    = 100,
                          height   = 100,
                          unit     = 'mm',
                          width_px = 200,
                          )
        maker.font_families([{'family': 'MyFont', 'file': '/path/to/font.ttf'}])
        dup = maker.copy()
        dup.font_families([{'family': 'Other', 'file': '/path/to/other.ttf'}])
        assert maker._font_families == {'MyFont': {'file': '/path/to/font.ttf'}}
        assert dup._font_families   == {'Other':  {'file': '/path/to/other.ttf'}}
```

- [ ] **Step 2: Run tests to confirm they fail**

```
source .venv/bin/activate && make test
```

Expected: 2 failures in `TestFontFamilies`.

- [ ] **Step 3: Update `font_families()` in `card_maker.py`**

Replace the method body (around line 638):

```python
def font_families(self, families: list[dict]) -> None:
    """
    Register font families for use in `text()` and `html()`.
    Each entry is a dict with at least a `family` key (the family name)
    and a `file` key (path to the font file).
    """
    self._font_families = {
        f['family']: {k: v for k, v in f.items() if k != 'family'}
        for f in families
    }
```

- [ ] **Step 4: Fix the `@font-face` loop in `html()`**

`html()` iterates `self._font_families` as `(name, path)`. After the change
the value is a dict, so update it (around line 760):

```python
font_face_css = []
for name, data in self._font_families.items():
    font_face_css.append(f"@font-face {{ font-family: '{name}'; "
                         f"src: url('{data['file']}'); }}")
```

- [ ] **Step 5: Run tests to confirm they pass**

```
source .venv/bin/activate && make test
```

Expected: all 90 tests pass.

- [ ] **Step 6: Commit**

```bash
git add gamehelper/card_maker.py tests/test_card_maker.py
git commit -m "feat: update font_families() to accept list of dicts"
```

---

### Task 2: Add `font_name()` method

Add `_font_names = {}` to `__init__` and the new `font_name()` method.
Add a new `TestFontName` test class.

**Files:**
- Modify: `gamehelper/card_maker.py`
- Modify: `tests/test_card_maker.py`

- [ ] **Step 1: Write failing tests**

Add a new `TestFontName` class after `TestFontFamilies` in `tests/test_card_maker.py`:

```python
FONT_FILE = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


class TestFontName:
    """Tests for font_name()."""

    def test_font_name_stores_preset(self):
        """font_name() should store the family and size in _font_names."""
        maker = CardMaker(width    = 100,
                          height   = 100,
                          unit     = 'mm',
                          width_px = 200,
                          )
        maker.font_families([{'family': 'Test', 'file': FONT_FILE}])
        maker.font_name('title', family='Test', size=5)
        assert maker._font_names['title']['family'] == 'Test'
        assert maker._font_names['title']['size']   == 5

    def test_font_name_raises_for_unknown_family(self):
        """font_name() should raise ValueError if the family is not registered."""
        maker = CardMaker(width    = 100,
                          height   = 100,
                          unit     = 'mm',
                          width_px = 200,
                          )
        with pytest.raises(ValueError):
            maker.font_name('title', family='Unknown', size=5)

    def test_copy_preserves_font_names(self):
        """Copying a CardMaker should preserve the font names."""
        maker = CardMaker(width    = 100,
                          height   = 100,
                          unit     = 'mm',
                          width_px = 200,
                          )
        maker.font_families([{'family': 'Test', 'file': FONT_FILE}])
        maker.font_name('title', family='Test', size=5)
        dup = maker.copy()
        assert dup._font_names['title']['family'] == 'Test'
        assert dup._font_names['title']['size']   == 5

    def test_copy_font_names_are_independent(self):
        """Calling font_name() on a copy should not affect the original."""
        maker = CardMaker(width    = 100,
                          height   = 100,
                          unit     = 'mm',
                          width_px = 200,
                          )
        maker.font_families([{'family': 'Test', 'file': FONT_FILE}])
        maker.font_name('title', family='Test', size=5)
        dup = maker.copy()
        dup.font_name('body', family='Test', size=3)
        assert 'body' not in maker._font_names
        assert 'body' in dup._font_names
```

- [ ] **Step 2: Run tests to confirm they fail**

```
source .venv/bin/activate && make test
```

Expected: 4 failures in `TestFontName`.

- [ ] **Step 3: Add `_font_names` to `__init__`**

In `__init__`, after the `self._font_families = {}` line (around line 71):

```python
self._font_families = {}
self._font_names    = {}
```

- [ ] **Step 4: Add `font_name()` to `card_maker.py`**

Add this method directly after `font_families()` (after line 643):

```python
def font_name(self,
              name:   str,
              *,
              family: str,
              size:   float,
              ) -> None:
    """
    Register a named font preset for use in `text()` and `html()`.
    `family` must be a family name registered via `font_families()`.
    `size` is in the default unit of this `CardMaker`.
    """
    if family not in self._font_families:
        raise ValueError(f"Font family '{family}' is not registered. "
                         f"Call font_families() first.")
    self._font_names = {**self._font_names, name: {'family': family, 'size': size}}
```

- [ ] **Step 5: Run tests to confirm they pass**

```
source .venv/bin/activate && make test
```

Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add gamehelper/card_maker.py tests/test_card_maker.py
git commit -m "feat: add font_name() for registering named font presets"
```

---

### Task 3: Update `text()` to resolve font names

Replace the `font: ImageFont.FreeTypeFont | None` parameter with `font: str | None`.
Add a `_resolve_font_name()` helper. Add caching inside `_font_names`.
Update all existing `TestText` tests and add new ones.

**Files:**
- Modify: `gamehelper/card_maker.py`
- Modify: `tests/test_card_maker.py` (lines 844–999)

- [ ] **Step 1: Write failing tests**

Replace the `TestText` class in `tests/test_card_maker.py`.
Note: `FONT_FILE` is already defined above from Task 2.

```python
class TestText:
    """Tests for the text() method."""

    def test_text(self):
        """Tests for positioning, alignment, and width wrapping."""
        maker = CardMaker(width    = 500,
                          height   = 500,
                          unit     = 'px',
                          width_mm = 500,
                          )
        maker.font_families([{'family': 'Test', 'file': FONT_FILE}])
        maker.font_name('normal', family='Test', size=14)

        # Width and chrs_per_line cannot both be specified
        with pytest.raises(ValueError):
            maker.text("Hello world",
                       left          = 0,
                       top           = 0,
                       width         = 50,
                       chrs_per_line = 10,
                       )

        # Width wraps text to fit
        left, top, right, bottom = maker.text(
            "This is a long piece of text that should be wrapped",
            left  = 0,
            top   = 0,
            font  = 'normal',
            width = 200,
            )
        width = right - left
        assert 0 <= left <= 5
        assert 100 <= right <= 200
        assert 100 <= width <= 200

        # Left/top positioning
        left, top, right, bottom = maker.text("Hello",
                                              left = 10,
                                              top  = 20,
                                              font = 'normal',
                                              )
        width  = right - left
        height = bottom - top
        assert 10 <= left <= 15
        assert 20 <= top <= 25
        assert right > left
        assert width > 0
        assert bottom > top
        assert height > 0

        # Right-aligned text ends near the right edge
        left, top, right, bottom = maker.text("Hello",
                                              left    = 0,
                                              top     = 0,
                                              right   = 200,
                                              font    = 'normal',
                                              h_align = "right",
                                              )
        width = right - left
        assert 150 <= left <= 200
        assert 195 <= right <= 200
        assert 0 < width <= 200

        # Bottom-aligned text ends near the bottom edge
        left, top, right, bottom = maker.text("Hello",
                                              left    = 0,
                                              top     = 0,
                                              bottom  = 200,
                                              font    = 'normal',
                                              v_align = "bottom",
                                              )
        height = bottom - top
        assert 150 <= top <= 200
        assert 195 <= bottom <= 200
        assert 0 < height <= 200

        # center → h_align defaults to "center"
        left, top, right, bottom = maker.text("Hello",
                                              center = 200,
                                              top    = 0,
                                              width  = 100,
                                              font   = 'normal',
                                              )
        width = right - left
        assert 150 <= left <= 200
        assert 200 <= right <= 250
        assert 0 < width <= 100

        # middle → v_align defaults to "middle"
        left, top, right, bottom = maker.text("Hello",
                                              left   = 0,
                                              middle = 200,
                                              height = 100,
                                              font   = 'normal',
                                              )
        height = bottom - top
        assert 150 <= top <= 200
        assert 200 <= bottom <= 250
        assert 0 < height <= 100

        # right without left → h_align defaults to "right"
        left, top, right, bottom = maker.text("Hello",
                                              right = 200,
                                              top   = 0,
                                              width = 100,
                                              font  = 'normal',
                                              )
        width = right - left
        assert 150 <= left <= 200
        assert 195 <= right <= 200
        assert 0 < width <= 100

        # bottom without top → v_align defaults to "bottom"
        left, top, right, bottom = maker.text("Hello",
                                              left   = 0,
                                              bottom = 200,
                                              height = 100,
                                              font   = 'normal',
                                              )
        height = bottom - top
        assert 150 <= top <= 200
        assert 195 <= bottom <= 200
        assert 0 < height <= 100

    def test_text_center_with_chrs_per_line(self):
        """center + chrs_per_line should not raise an error."""
        maker = CardMaker(width    = 500,
                          height   = 500,
                          unit     = 'px',
                          width_mm = 500,
                          )
        maker.font_families([{'family': 'Test', 'file': FONT_FILE}])
        maker.font_name('normal', family='Test', size=14)
        left, top, right, bottom = maker.text(
            "This is a long piece of text that should be wrapped",
            center        = 250,
            top           = 0,
            font          = 'normal',
            chrs_per_line = 10,
            )
        width  = right - left
        height = bottom - top
        assert width > 0
        assert height > 0

    def test_text_wrapping_with_mm_units(self):
        """Width parameter should correctly wrap text when default unit is mm."""
        maker = CardMaker(width    = 60,
                          height   = 80,
                          unit     = 'mm',
                          width_px = 600,
                          )
        maker.font_families([{'family': 'Test', 'file': FONT_FILE}])
        maker.font_name('large', family='Test', size=3)  # 3mm = 30px
        long_text = "This is a long piece of text that should be wrapped to fit within the box"
        left, top, right, bottom = maker.text(long_text,
                                              left  = 0,
                                              top   = 0,
                                              font  = 'large',
                                              width = 55,
                                              )
        width = right - left
        assert 0 < width <= 55

    def test_text_font_none_uses_default(self):
        """text() with font=None should use PIL's default font without error."""
        maker = CardMaker(width    = 500,
                          height   = 500,
                          unit     = 'px',
                          width_mm = 500,
                          )
        left, top, right, bottom = maker.text("Hello",
                                              left = 0,
                                              top  = 0,
                                              )
        assert right > left
        assert bottom > top

    def test_text_unknown_font_raises(self):
        """text() with an unregistered font name should raise ValueError."""
        maker = CardMaker(width    = 500,
                          height   = 500,
                          unit     = 'px',
                          width_mm = 500,
                          )
        with pytest.raises(ValueError):
            maker.text("Hello",
                       left = 0,
                       top  = 0,
                       font = 'nonexistent',
                       )

    def test_text_caches_font_object(self):
        """text() should cache the ImageFont object after the first call."""
        maker = CardMaker(width    = 500,
                          height   = 500,
                          unit     = 'px',
                          width_mm = 500,
                          )
        maker.font_families([{'family': 'Test', 'file': FONT_FILE}])
        maker.font_name('normal', family='Test', size=14)
        assert 'font_obj' not in maker._font_names['normal']
        maker.text("Hello", left=0, top=0, font='normal')
        assert 'font_obj' in maker._font_names['normal']
        cached = maker._font_names['normal']['font_obj']
        maker.text("World", left=0, top=20, font='normal')
        assert maker._font_names['normal']['font_obj'] is cached
```

Also update the import at the top of `tests/test_card_maker.py` — `ImageFont` is no longer needed:

```python
# Before:
from PIL import Image, ImageFont

# After:
from PIL import Image
```

- [ ] **Step 2: Run tests to confirm they fail**

```
source .venv/bin/activate && make test
```

Expected: failures in `TestText` due to `font` type mismatch.

- [ ] **Step 3: Add `_resolve_font_name()` helper to `card_maker.py`**

Add this private method after `font_name()`:

```python
def _resolve_font_name(self, name: str) -> tuple[str, float]:
    """
    Look up a registered font preset and return `(file_path, size)`.
    `size` is in the default unit of this `CardMaker`.
    Raises `ValueError` if the name or its family is not registered.
    """
    if name not in self._font_names:
        raise ValueError(f"Font '{name}' is not registered. "
                         f"Call font_name() first.")
    preset = self._font_names[name]
    family = preset['family']
    if family not in self._font_families:
        raise ValueError(f"Font family '{family}' is not registered. "
                         f"Call font_families() first.")
    return (self._font_families[family]['file'], preset['size'])
```

- [ ] **Step 4: Update `text()` signature and implementation**

Replace the `text()` method signature and the font-resolution section.

New signature (change only the `font` parameter type):

```python
def text(self,
         text:          str                  = "Default",
         left:          float | None         = None,
         top:           float | None         = None,
         right:         float | None         = None,
         bottom:        float | None         = None,
         center:        float | None         = None,
         middle:        float | None         = None,
         width:         float | None         = None,
         height:        float | None         = None,
         h_align:       str | None           = None,
         v_align:       str | None           = None,
         fill:          tuple[int, int, int] = (0, 0, 0),
         font:          str | None           = None,
         spacing:       float | None         = None,
         chrs_per_line: int | None           = None,
         ) -> tuple[float, float, float, float]:
```

Update the docstring line about font:

```
- The font must be a name registered via `font_name()`.
  If `None`, PIL's default font is used.
```

Add font resolution just before the `if spacing is None:` line (around line 854):

```python
font_obj = None
if font is not None:
    file, size = self._resolve_font_name(font)
    preset     = self._font_names[font]
    if 'font_obj' not in preset:
        preset['font_obj'] = ImageFont.truetype(file, int(self.to_px(size)))
    font_obj = preset['font_obj']
```

Then replace every remaining occurrence of `font` (the parameter) with `font_obj`
in the body of `text()`. There are four: the call to `_calc_chrs_per_line`, the
two calls to `draw.text()` and `draw.textbbox()`. Updated calls:

```python
chrs_per_line = self._calc_chrs_per_line(text, width, chrs_per_line,
                                         font_obj, spacing)
```

```python
draw.text(xy      = (int(x_pos), int(y_pos)),
          anchor  = h_anchor + v_anchor,
          text    = text,
          fill    = fill,
          font    = font_obj,
          align   = align,
          spacing = spacing,
          )
bbox = draw.textbbox(xy      = (int(x_pos), int(y_pos)),
                     anchor  = h_anchor + v_anchor,
                     text    = text,
                     font    = font_obj,
                     align   = align,
                     spacing = spacing,
                     )
```

- [ ] **Step 5: Run tests to confirm they pass**

```
source .venv/bin/activate && make test
```

Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add gamehelper/card_maker.py tests/test_card_maker.py
git commit -m "feat: update text() to resolve fonts by registered name"
```

---

### Task 4: Update `html()` to resolve font names

Replace `font_family: str | None` and `font_size: float | None` with
`font: str | None`. `html()` requires a real browser so no unit tests are added.

**Files:**
- Modify: `gamehelper/card_maker.py`

- [ ] **Step 1: Update `html()` signature**

Replace the last two parameters in the `html()` signature (around line 720):

```python
def html(self,
         content:  str,
         left:     float | None = None,
         top:      float | None = None,
         right:    float | None = None,
         bottom:   float | None = None,
         center:   float | None = None,
         middle:   float | None = None,
         width:    float | None = None,
         height:   float | None = None,
         h_align:  str | None   = None,
         v_align:  str | None   = None,
         font:     str | None   = None,
         ) -> None:
```

Update the docstring: replace the two lines about `font_family` and `font_size` with:

```
`font` sets the document font family and size using a name registered
via `font_name()`.
```

- [ ] **Step 2: Update `html()` font CSS generation**

Replace the two lines that build `font_size_css` and `font_family_css`
(currently around lines 755–756) with:

```python
font_size_css   = ""
font_family_css = ""
if font is not None:
    file, size      = self._resolve_font_name(font)
    family          = self._font_names[font]['family']
    size_px         = int(self.to_px(size))
    font_size_css   = f'font-size:   {size_px}px;'
    font_family_css = f"font-family: '{family}';"
```

- [ ] **Step 3: Run tests to confirm nothing is broken**

```
source .venv/bin/activate && make test
```

Expected: all tests pass.

- [ ] **Step 4: Commit**

```bash
git add gamehelper/card_maker.py
git commit -m "feat: update html() to resolve fonts by registered name"
```
