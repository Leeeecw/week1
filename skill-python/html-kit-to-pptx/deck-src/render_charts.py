import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cairosvg
import charts

OUT_SVG = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "deck-assets")
OUT_PNG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_preview")
os.makedirs(OUT_SVG, exist_ok=True)
os.makedirs(OUT_PNG, exist_ok=True)

SIZES = {                       # charts that should fill the 1104px content column
    "forecast-ranges": dict(w=1104, h=404),
    "gpt-contribution": dict(w=1104, h=340),
    "ai-conditions": dict(w=1104, h=190),
    "hulten-compare": dict(w=1104, h=330),
    "shaft-to-unit": dict(w=1104, h=300),
}

for name, fn in charts.ALL.items():
    s = fn(**SIZES.get(name, {}))
    p = os.path.join(OUT_SVG, name + ".svg")
    open(p, "w", encoding="utf-8").write(s)
    m = re.search(r'width="(\d+)" height="(\d+)"', s)
    w, h = int(m.group(1)), int(m.group(2))
    bg = "#272729" if name == "shaft-to-unit" else "#ffffff"
    cairosvg.svg2png(bytestring=s.encode("utf-8"),
                     write_to=os.path.join(OUT_PNG, name + ".png"),
                     output_width=w * 2, output_height=h * 2,
                     background_color=bg)
    print("ok", name, w, h)
