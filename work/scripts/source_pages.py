"""Render a client's creative-direction PDFs into PNG tiles Claude can look at (onboarding).
usage: python work/scripts/source_pages.py [<client>/<style>] [--scale=0.5] [--tile=1400]
Reads every .pdf in clients/<client>/<style>/source/ (default: the active style) and writes into its style/board/:
  <pdf>_p<n>_overview.png   the whole page, long side <= 2000 px
  <pdf>_p<n>_r<row>c<col>.png  tiles of <= tile px at --scale (only when the page is bigger than one tile: e.g. a Figma board)
Then Read the overviews first and only the tiles you need. Needs pypdfium2 (requirements.txt)."""
import os, sys, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pylibs'))
import pypdfium2 as pdfium
from client_style import CLIENTS, style_dir, rel

opt = {a.split('=')[0]: a.split('=')[1] for a in sys.argv[1:] if a.startswith('--') and '=' in a}
args = [a for a in sys.argv[1:] if not a.startswith('--')]
sd = os.path.join(CLIENTS, *args[0].strip('/').split('/')) if args else style_dir()
SCALE, TILE = float(opt.get('--scale', 0.5)), int(opt.get('--tile', 1400))
out = os.path.join(sd, 'style', 'board')
os.makedirs(out, exist_ok=True)
pdfs = sorted(glob.glob(os.path.join(sd, 'source', '**', '*.pdf'), recursive=True))
if not pdfs:
    sys.exit(f'no PDF in {rel(os.path.join(sd, "source"))} (PNG/JPG exports there can be Read directly)')
for path in pdfs:
    name = os.path.splitext(os.path.basename(path))[0][:40].replace(' ', '_')
    doc = pdfium.PdfDocument(path)
    for i in range(len(doc)):
        page = doc[i]
        w, h = page.get_size()
        page.render(scale=min(2000 / max(w, h), 2.0)).to_pil().save(os.path.join(out, f'{name}_p{i + 1}_overview.png'))
        img = page.render(scale=SCALE).to_pil()
        n = 1
        if img.width > TILE or img.height > TILE:
            for r, y in enumerate(range(0, img.height, TILE)):
                for c, x in enumerate(range(0, img.width, TILE)):
                    img.crop((x, y, min(x + TILE, img.width), min(y + TILE, img.height))).save(
                        os.path.join(out, f'{name}_p{i + 1}_r{r + 1}c{c + 1}.png'))
                    n += 1
        print(f'{os.path.basename(path)} page {i + 1}: overview + {n - 1} tiles')
print('written to ' + rel(out))
