# Environment notes

## Dependencies

```bash
pip install python-pptx cairosvg
```

`python-pptx` writes the .pptx. `cairosvg` rasterizes SVG for two purposes: the
PNG fallback inside each embedded graphic, and the preview images used for QA.
Nothing else is required — no Node, no LibreOffice, no headless browser.

Verify with the bundled example, which exercises every code path:

```bash
python scripts/example_deck.py /tmp/example.pptx
```

## Fonts

Two different font problems, often confused:

**1. Fonts in the .pptx** are just names. They are resolved on the machine that
opens the file, so the deck depends on the viewer having them. Arial, Calibri,
Times New Roman, Courier New ship with Office everywhere. For CJK, set
`Theme.ea_font` to a face the audience will have — Malgun Gothic (Korean
Windows), Yu Gothic (Japanese), Microsoft YaHei (Simplified Chinese), or Noto
Sans CJK where it is installed. Nothing needs to be installed locally for this
to work.

**2. Fonts for rasterizing** matter only for the preview PNGs and the fallback
images. cairosvg resolves families through fontconfig; if a family is missing
you get boxes or a substituted face in the preview, while the .pptx text stays
correct.

On WSL you can borrow the Windows fonts instead of installing any:

```bash
mkdir -p ~/.config/fontconfig
cat > ~/.config/fontconfig/fonts.conf <<'XML'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>/mnt/c/Windows/Fonts</dir>
</fontconfig>
XML
fc-cache -f
fc-match Arial          # should report arial.ttf
fc-list :lang=ko | head # should be non-empty for Korean previews
```

On a plain Linux container: `apt-get install fonts-liberation fonts-noto-cjk`
gives metric-compatible Arial (Liberation Sans) and CJK coverage.

## Rendering the actual .pptx

The preview renderer is geometry-identical, so it catches layout defects. It is
still not PowerPoint. If you want a true render and LibreOffice is available:

```bash
soffice --headless --convert-to pdf deck.pptx
pdftoppm -jpeg -r 150 deck.pdf slide      # slide-1.jpg, slide-2.jpg, …
```

If it is not available and cannot be installed (no sudo in the sandbox, which is
common), say so when handing over the deck rather than implying the file was
visually verified. Recommend the user open it once in PowerPoint — especially
to confirm CJK substitution and that SVG graphics render as vectors.

## Sandboxes with a Windows host and a Linux toolchain

When the project lives on a WSL path but the shell is PowerShell, run the build
inside WSL so the Python environment and the fonts line up:

```powershell
wsl -d <distro> bash -c "cd ~/project && ./.venv/bin/python build_deck.py"
```

Quoting gets mangled quickly when passing Python one-liners through PowerShell
into WSL. Write a small `.sh` or `.py` file and run that instead — it is faster
than debugging three layers of escaping.

## Output size

A 20-slide deck with ten embedded SVG graphics lands around 700 KB. If a deck
is far larger, something is embedding raster images at excessive resolution —
the PNG fallbacks are rendered at 2× the placement size, which is enough.
