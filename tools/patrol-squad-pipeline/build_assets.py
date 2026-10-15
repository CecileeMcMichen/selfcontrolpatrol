"""Export the chosen Patrol Squad cuts as clean, trimmed, truly transparent PNGs.

Usage: python3 -I tools/build_assets.py <cuts_dir> <out_assets_dir> <report.json>
"""
import sys, os, json, numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from picks import PICKS, REJECTED
from clean_v2 import clean_v2

cuts, out, report_path = sys.argv[1], sys.argv[2], sys.argv[3]
EIGHT = np.ones((3, 3), bool)


def load(name):
    return np.array(Image.open(os.path.join(cuts, name + '.png')).convert('RGBA'))


def clean(arr):
    """Drop speck fragments (<0.5% of the main body) and fully zero hidden RGB."""
    a = arr[..., 3]
    mask = a > 8
    lab, n = ndi.label(mask, structure=EIGHT)
    removed = 0
    if n > 1:
        sizes = ndi.sum(mask, lab, range(1, n + 1))
        main = sizes.max()
        for i, s in enumerate(sizes, 1):
            if s < main * 0.015:
                arr[lab == i] = 0
                removed += int(s)
    # faint alpha <=8 left over from the sheet is invisible noise; clear it fully
    arr[a <= 8] = 0
    return arr, removed


def trim(arr, pad=1):
    ys, xs = np.nonzero(arr[..., 3])
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    t = arr[y0:y1, x0:x1]
    return np.pad(t, ((pad, pad), (pad, pad), (0, 0)))


def split(arr, side):
    a = arr[..., 3].astype(float)
    w = a.shape[1]
    cols = a.sum(0)
    lo, hi = int(w * 0.3), int(w * 0.7)
    cut = lo + int(np.argmin(cols[lo:hi]))
    part = arr[:, :cut].copy() if side == 'left' else arr[:, cut:].copy()
    # keep only the largest body on that side
    m = part[..., 3] > 8
    lab, n = ndi.label(m, structure=EIGHT)
    if n > 1:
        sizes = ndi.sum(m, lab, range(1, n + 1))
        keep = 1 + int(np.argmax(sizes))
        part[(lab != keep) & m] = 0
    return part, cut


report = {"characters": {}, "rejected": REJECTED}
for char, groups in PICKS.items():
    report["characters"][char] = {}
    for group, items in groups.items():
        folder = os.path.join(out, char, group)
        os.makedirs(folder, exist_ok=True)
        rows = {}
        for name, src in items.items():
            note = ''
            if src.startswith('rows:'):
                _, cut_name, row = src.split(':')
                arr = load(cut_name).copy(); arr[:int(row)] = 0
                note = f'rows {row}+ of {cut_name}'
                src_name = cut_name
            elif src.startswith('split:'):
                _, cut_name, side = src.split(':')
                arr, at = split(load(cut_name), side)
                note = f'split from {cut_name} at x={at} ({side})'
                src_name = cut_name
            else:
                arr = load(src)
                src_name = src
            arr, removed = clean(arr)
            # v2 best-cut pass (neighbour slivers, haze, baked glow). The canvas is
            # cropped to the v1 bounding box so board fitting and pose heights hold.
            ys, xs = np.nonzero(arr[..., 3]); box = (ys.min(), ys.max() + 1, xs.min(), xs.max() + 1)
            arr = np.pad(clean_v2(arr)[box[0]:box[1], box[2]:box[3]], ((1, 1), (1, 1), (0, 0)))
            fname = f'{char}-{name}.png'
            Image.fromarray(arr).save(os.path.join(folder, fname), optimize=True)
            a = arr[..., 3]
            rows[name] = {
                "file": f'assets/patrol-squad/{char}/{group}/{fname}',
                "source": src_name, "w": int(arr.shape[1]), "h": int(arr.shape[0]),
                "cornersTransparent": bool(a[0, 0] == 0 and a[0, -1] == 0 and a[-1, 0] == 0 and a[-1, -1] == 0),
                "borderTransparent": bool(a[0].max() == 0 and a[-1].max() == 0 and a[:, 0].max() == 0 and a[:, -1].max() == 0),
                "speckPixelsRemoved": removed, **({"note": note} if note else {}),
            }
        report["characters"][char][group] = rows
json.dump(report, open(report_path, 'w'), indent=1)
total = sum(len(r) for c in report["characters"].values() for r in c.values())
bad = [(c, g, n) for c, gs in report["characters"].items() for g, rs in gs.items() for n, r in rs.items() if not r["borderTransparent"]]
print('exported', total, 'sprites; non-transparent borders:', bad)

# ---- @2x display copies for runtime layers (poses, expressions, accessories) ----
from upscale import up2
n2 = 0
for char, groups in report["characters"].items():
    for group in ('poses', 'expressions', 'accessories'):
        for name, row in groups.get(group, {}).items():
            src = os.path.join(out, char, group, os.path.basename(row["file"]))
            dst = src[:-4] + '@2x.webp'
            up2(Image.open(src)).save(dst, 'WEBP', quality=90, alpha_quality=100, method=6)
            row["display"] = row["file"][:-4] + '@2x.webp'
            n2 += 1
json.dump(report, open(report_path, 'w'), indent=1)
print('display @2x copies:', n2)
