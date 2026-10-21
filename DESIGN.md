# Profile artwork

The profile README uses native GitHub Markdown, linked SVG artwork, and
`picture` sources for light/dark appearance. The header also has a narrow-screen
variant. Project descriptions remain selectable text outside images.

## Regenerate

Use Python 3.10+ and install `fonttools` and `brotli` in a virtual environment:

```sh
python -m venv .venv
# Activate the environment using your shell's standard activation command.
python -m pip install fonttools brotli
python gen.py
```

The original profile's embedded font subsets are preserved in
`design/typefaces.json`, and its original handwritten name artwork is preserved
in `design/signature.svg`. The generator uses these exact glyphs: serif for
project titles, the original sans/CJK faces for body text, the original tight
face for the Latin name, and the original mono face for technical labels.
Missing glyphs fail explicitly instead of silently substituting another font.
The native Markdown paragraphs use GitHub's own typography.

The generated SVG files contain outlined lettering and require no remote fonts,
JavaScript, or external images. Source text is editable in `gen.py`; image titles,
labels, and README alt text provide text alternatives. Layered metallic ribbons,
fine-grain texture, light sweeps, kinetic typography, and a dart trajectory provide
motion without cartoon characters. CSS animations respect reduced-motion preferences.

`assets/readme-cat*.svg` and `assets/readme-dsh*.svg` are companion repository
cover exports. They can be copied to each repository as `docs/img/readme-cover.svg`
and `docs/img/readme-cover-light.svg`.

## Visual checks

- Inspect the README in GitHub light and dark modes, at desktop and phone widths.
- Keep all `picture` sources and their fallback image together when editing.
- Confirm links and project descriptions against their source repositories.
- The existing contribution-snake workflow and output branch are independent
  of the profile artwork generator.

Reference: Vincentwei1021's profile informed the project-by-project presentation.
The new illustrations, layout, palette and generator are original; the typography
and handwritten signature are retained from this profile's previous revision.
