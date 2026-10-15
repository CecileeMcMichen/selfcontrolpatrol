"""Best-cut cleaner v2 for Patrol Squad sprites.

1. Fragments: components (alpha>40, 8-connected) that are not the main body are
   dropped when they are slivers on the cut's border (neighbouring sprites) or
   tiny specks. Detached props drawn with the figure (a held clipboard) are kept.
2. Haze: faint pixels (alpha<=40) far from any kept body are cleared.
3. Halo: the soft dark glow baked around master-sheet figures is tapered so the
   edge keeps a normal 1-2 px anti-aliased fringe. Opaque and thin line art
   (alpha>=120) is never touched.
"""
import numpy as np
from scipy import ndimage as ndi
EIGHT = np.ones((3, 3), bool)

def clean_v2(arr, halo=True, stats=None):
    arr = arr.copy()
    a = arr[..., 3].astype(np.float32)
    H, W = a.shape
    body = a > 40
    lab, n = ndi.label(body, structure=EIGHT)
    keep = np.zeros_like(body)
    dropped = 0
    if n:
        sizes = ndi.sum(body, lab, range(1, n + 1))
        main_i = int(np.argmax(sizes)) + 1
        main_area = sizes.max()
        main = lab == main_i
        dist_main = ndi.distance_transform_edt(~main)
        for i, s in enumerate(sizes, 1):
            comp = lab == i
            if i == main_i:
                keep |= comp; continue
            ys, xs = np.nonzero(comp)
            w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
            on_border = xs.min() <= 1 or xs.max() >= W - 2 or ys.min() <= 1 or ys.max() >= H - 2
            near = dist_main[comp].min()
            sliver = on_border and min(w, h) <= 12 and s < 0.05 * main_area
            speck = s < 0.004 * main_area
            far_small = near > 8 and s < 0.03 * main_area
            if sliver or speck or far_small:
                dropped += int(s)
            else:
                keep |= comp
    # faint pixels: keep only within 3px of a kept body
    near_keep = ndi.distance_transform_edt(~keep) <= 3
    faint = (a > 0) & ~keep
    clear = faint & ~near_keep
    a[clear] = 0
    # also kill everything belonging to dropped components
    a[body & ~keep] = 0
    if halo:
        core = a >= 150
        d = ndi.distance_transform_edt(~core)
        factor = np.clip((3.5 - d) / 2.0, 0, 1)   # 1 up to 1.5px, 0 by 3.5px
        soft = a < 120
        a = np.where(soft, a * factor, a)
    a[a < 6] = 0
    arr[..., 3] = a.round().astype(np.uint8)
    arr[arr[..., 3] == 0] = 0
    if stats is not None:
        stats['dropped'] = dropped
    return arr
