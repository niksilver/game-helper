# Font Tidying Design

## Overview

Tidy up font handling in `CardMaker` so that fonts are registered once and
referenced by name in `text()` and `html()`. Two registration levels: font
families (name → file path + metadata) and named presets (name → family +
size).

## Registration

### `font_families(families)`

Updated to accept a list of dicts instead of a single dict.

```python
maker.font_families([
    {'family': 'Bookman', 'file': '/path/to/Bookman.otf'},
])
```

Stored internally as `_font_families: dict[str, dict]`, keyed by family name
with the full dict as the value:

```python
{'Bookman': {'file': '/path/to/Bookman.otf'}}
```

The value dict is designed to be extensible — future keys such as `style` or
`weight` may be added without changing the structure.

### `font_name(name, *, family, size)`

New method. Registers a named preset combining a family and a size. `size` is
in the default unit of the `CardMaker` (mm or px). Raises an error if the
referenced family has not been registered via `font_families()`.

```python
maker.font_name('title', family='Bookman', size=5)
maker.font_name('body',  family='Bookman', size=3)
```

Stored internally as `_font_names: dict[str, dict]`:

```python
{'title': {'family': 'Bookman', 'size': 5}}
```

`font_name()` replaces `_font_names` with a new dict rather than mutating it,
so copies remain independent (see Copy Behaviour below).

## Usage

### `text()`

The `font: ImageFont.FreeTypeFont | None` parameter is replaced with
`font: str | None`, accepting a registered preset name. No `font_size`
parameter — size is taken from the preset.

```python
maker.text("Hello", font='title', left=0, top=0)
```

Resolution:
1. Look up preset name in `_font_names` → `{'family': 'Bookman', 'size': 5}`
2. Look up family in `_font_families` → `{'file': '/path/to/Bookman.otf'}`
3. Convert size to pixels
4. Call `ImageFont.truetype(file, size_px)` and cache the result

`font=None` remains valid and falls back to PIL's default font.

### `html()`

The `font_family: str | None` and `font_size: float | None` parameters are
replaced with `font: str | None`, accepting a registered preset name.

```python
maker.html("<b>Hi</b>", font='title', left=0, top=0)
```

Resolution:
1. Look up preset name in `_font_names` → family and size
2. Look up family in `_font_families` → file path for `@font-face`
3. Convert size to pixels for CSS `font-size`

`font=None` remains valid and omits font styling entirely.

## Font Cache

The resolved `ImageFont.FreeTypeFont` object is cached inside `_font_names`
under the key `'font_obj'`:

```python
{'title': {'family': 'Bookman', 'size': 5, 'font_obj': <ImageFont>}}
```

The cache is populated lazily on first use by `text()`. Since `copy()` shares
`_font_names` by reference, copies benefit from already-cached fonts without
any extra work.

## Copy Behaviour

`copy()` continues to use `copy.copy()` (shallow copy). This means:

- `_font_families` is shared by reference. Since `font_families()` always
  replaces the dict entirely, copies remain independent.
- `_font_names` is shared by reference. Since `font_name()` always replaces
  the dict entirely, copies remain independent. The shared reference also
  means cached `ImageFont` objects are available to all copies.

No changes to `copy()` are needed.

## Error Handling

- `font_name()` raises `ValueError` if the referenced family is not registered.
- `text()` and `html()` raise `ValueError` if the font preset name is not found
  in `_font_names`.
- `text()` and `html()` raise `ValueError` if the family referenced by the
  preset is not found in `_font_families`.

## Tests

- `font_families()` stores the full dict per family, keyed by family name
- `font_name()` stores a preset correctly
- `font_name()` raises `ValueError` if the referenced family is not registered
- `text()` uses a named preset to draw text correctly
- `text()` caches the `ImageFont` object in `_font_names` after first use
- `text()` raises `ValueError` for an unknown font name
- `text(font=None)` works using PIL's default font
- `copy()` preserves `_font_families` and `_font_names`
- After `copy()`, calling `font_name()` on either original or copy does not
  affect the other
- `html()` font behaviour is not unit-tested (requires a real browser),
  consistent with existing test approach
