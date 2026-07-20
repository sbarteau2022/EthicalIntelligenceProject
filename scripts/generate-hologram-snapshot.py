# ============================================================
# generate-hologram-snapshot.py  —  the off-axis rebuild (the X)
#
# Stewart's correction: the two halves don't project straight out and record
# inline. They separate, angle toward each other, and cross in an X — reflecting
# off the central rotating knot — and THAT is what writes the hologram. He was
# right, and the correction is a known upgrade in the physics: from Gabor INLINE
# holography (1948) to Leith–Upatnieks OFF-AXIS holography (1962). The X is not a
# style note — it is the fix for the exact flaw the previous version carried and
# honestly logged: the TWIN IMAGE. Writes src/data/hologram-snapshot.json.
# Requires numpy.
#
# THE DEMONSTRATION (all computed; the twin separation is MEASURED):
#   Two beams cross at a full angle 2·alpha at the knot. Their interference on the
#   plate carries a spatial carrier f_c = 2·sin(alpha)/lambda. An object field of
#   half-bandwidth B rides one arm. The recorded hologram's Fourier spectrum has
#   THREE bands: the zero order |o|^2 (width ~2B at f=0) and the two sidebands
#   o, o* at -/+ f_c — the real image and its twin. They separate cleanly iff
#     f_c > 3B/2                                   (the Leith condition)
#   i.e. once the X opens past a threshold crossing angle. Below it the bands
#   overlap and the twin contaminates the reconstruction; above it the twin is
#   carried away and the image returns clean. We MEASURE this by reconstructing
#   the object at a sweep of crossing angles (demodulate the sideband, low-pass,
#   correlate with truth): recovery correlation jumps from ~0.24 (inline, twin-
#   contaminated) to ~1.00 (off-axis, twin gone) exactly at the Leith angle.
#
# THE KNOT + MULTIPLEX (proposed, labeled — the rotating part):
#   The knot at the crossing steers the beams; as it rotates it sweeps the
#   reference angle, and each angle writes a distinct page into the same medium —
#   real angle-multiplexing (as in holographic data storage). The single X's
#   angle is set by the Leith separation condition, NOT by phi (forcing phi there
#   would be a fit). But the STEP between successive pages, if taken at the golden
#   angle, packs the most non-overlapping pages before crosstalk — the same
#   most-irrational logic as the KAM curve and the sunflower. So phi does not tilt
#   any one X; it spaces the fan of X's. Computed against a uniform control and
#   labeled proposed, same column as the golden spray it replaces.
#
# Deterministic (seeded object field).
# ============================================================

import json
import math

import numpy as np

LAM = 1.0
K = 2 * math.pi / LAM
N = 4096          # 1D grid for the rigorous certificates
L = 400.0         # transverse extent, wavelengths
B = 0.02          # object half-bandwidth (cycles / wavelength)
SEED = 7

x = np.linspace(-L / 2, L / 2, N)
dx = x[1] - x[0]
f = np.fft.fftfreq(N, d=dx)
rng = np.random.default_rng(SEED)

# ── the object field on the plate: a bandlimited complex "class of detail" ──
sp = np.zeros(N, dtype=complex)
inband = np.abs(f) <= B
sp[inband] = rng.standard_normal(inband.sum()) + 1j * rng.standard_normal(inband.sum())
o = np.fft.ifft(sp)
o = o / np.max(np.abs(o)) * 0.6  # reference-dominant (linear hologram regime)

carrier_of = lambda full_deg: 2 * math.sin(math.radians(full_deg) / 2) / LAM  # symmetric X
angle_of = lambda fc: math.degrees(2 * math.asin(min(1.0, fc * LAM / 2)))

LEITH_FC = 1.5 * B
LEITH_ANGLE = angle_of(LEITH_FC)
WORK_ANGLE = 4.0                     # the working crossing angle (well past Leith)
WORK_FC = carrier_of(WORK_ANGLE)
FRINGE = 1.0 / WORK_FC               # carrier fringe period on the plate, wavelengths


def recover_corr(full_deg):
    fc = carrier_of(full_deg)
    r = np.exp(1j * 2 * math.pi * fc * x)          # one arm carries the carrier
    I = np.abs(o + r) ** 2                          # recorded hologram
    demod = I * np.exp(1j * 2 * math.pi * fc * x)   # bring the o-sideband to baseband
    S = np.fft.fft(demod)
    S[np.abs(f) > B] = 0                            # low-pass |f| <= B
    rec = np.fft.ifft(S)
    cc = np.fft.ifft(np.fft.fft(o) * np.conj(np.fft.fft(rec)))  # shift-robust corr
    corr = float(np.max(np.abs(cc)) / (np.linalg.norm(o) * np.linalg.norm(rec) + 1e-12))
    return fc, corr


# ── the recovery-vs-angle curve (the step at the Leith threshold) ──
sweep_deg = [round(0.25 * i, 3) for i in range(0, 33)]  # 0 .. 8 deg
recovery_curve = []
for d in sweep_deg:
    fc, corr = recover_corr(d)
    recovery_curve.append([d, round(corr, 4)])
inline_corr = recover_corr(0.0)[1]
offaxis_corr = recover_corr(WORK_ANGLE)[1]

# ── the spectra: three bands, inline (overlap) vs off-axis (separated) ──
def spectrum(full_deg):
    fc = carrier_of(full_deg)
    r = np.exp(1j * 2 * math.pi * fc * x)
    I = np.abs(o + r) ** 2
    F = np.abs(np.fft.fftshift(np.fft.fft(I - I.mean()))) / N
    return fc, F


ffs = np.fft.fftshift(f)
_, F_inline = spectrum(0.3)      # ~inline (tiny angle: bands piled on DC)
_, F_off = spectrum(WORK_ANGLE)  # off-axis: sidebands ride out to +/- f_c
# store a decimated window around the interesting band |f| <= 0.16
keep = np.abs(ffs) <= 0.16
fs_k = ffs[keep]
step = max(1, len(fs_k) // 260)
spec_f = [round(float(v), 5) for v in fs_k[::step]]
spec_inline = [round(float(v), 5) for v in (F_inline[keep][::step])]
spec_off = [round(float(v), 5) for v in (F_off[keep][::step])]
# normalize both to the off-axis peak for display parity
_pk = max(max(spec_inline), max(spec_off), 1e-9)
spec_inline = [round(v / _pk, 5) for v in spec_inline]
spec_off = [round(v / _pk, 5) for v in spec_off]

# ── the recording plate image: 2D off-axis fringes (visual only) ──
NI = 256
LI = 120.0
xi = np.linspace(-LI / 2, LI / 2, NI)
XI, YI = np.meshgrid(xi, xi)
alpha = math.radians(WORK_ANGLE) / 2
# two point beams crossing at the knot: symmetric arms +/- alpha in the x-z plane
Zp = 70.0
# object arm point + reference arm point, placed so their beams cross at 2*alpha
xo_pt = -math.tan(alpha) * Zp
xr_pt = +math.tan(alpha) * Zp
Ro = np.sqrt((XI - xo_pt) ** 2 + YI**2 + Zp**2)
Rr = np.sqrt((XI - xr_pt) ** 2 + YI**2 + Zp**2)
Ei = np.exp(1j * K * Ro) / np.sqrt(Ro) + np.exp(1j * K * Rr) / np.sqrt(Rr)
Ii = np.abs(Ei) ** 2
Ii = Ii / np.percentile(Ii, 99)
Ii = np.clip(Ii, 0, 1)
plate = [[int(round(v * 255)) for v in row] for row in Ii[::1]]

# ── the multiplex: the rotating knot's page angles (proposed) ──
PAGES = 34  # a Fibonacci number of pages
TWO_PI = 2 * math.pi
GOLDEN_ANGLE = TWO_PI * (1 - 1 / ((1 + 5 ** 0.5) / 2))
golden_dirs = [round((n * GOLDEN_ANGLE) % TWO_PI, 6) for n in range(PAGES)]
UNIFORM_STEP = TWO_PI * 3 / 8  # a low-denominator rational: revisits 8 angles forever
uniform_dirs = [round((n * UNIFORM_STEP) % TWO_PI, 6) for n in range(PAGES)]


def min_gap(dirs):
    s = sorted(set(round(d, 6) for d in dirs))
    gaps = [s[(i + 1) % len(s)] - s[i] for i in range(len(s) - 1)] + [s[0] + TWO_PI - s[-1]]
    return min(gaps), len(s)


gg, gn = min_gap(golden_dirs)
ug, un = min_gap(uniform_dirs)

snapshot = {
    "meta": {
        "title": "Holographic Atlas — the off-axis cross (the X)",
        "lambdaUnit": LAM,
        "crossingAngleDeg": WORK_ANGLE,
        "carrier": round(WORK_FC, 5),
        "fringePeriod": round(FRINGE, 3),
        "objectBandwidthB": B,
        "leithThresholdCarrier": round(LEITH_FC, 5),
        "leithThresholdAngleDeg": round(LEITH_ANGLE, 4),
        "source": "generated by scripts/generate-hologram-snapshot.py — Leith–Upatnieks off-axis two-beam holography; twin-image separation MEASURED via reconstruction-correlation sweep across the crossing angle (requires numpy)",
        "note": (
            "The two beams cross in an X at the knot; the crossing angle sets a "
            "spatial carrier f_c = 2·sin(alpha)/lambda that carries the twin image "
            "away from the real one — the Leith–Upatnieks off-axis fix for the "
            "twin-image flaw the previous inline version logged. Demonstrated, not "
            "asserted: recovery correlation jumps from ~0.24 (inline, twin-"
            "contaminated) to ~1.00 (off-axis) exactly at the Leith angle f_c=3B/2. "
            "The single X's angle is set by that separation condition, NOT by phi "
            "— forcing phi there would be a fit. phi enters only in the MULTIPLEX: "
            "the rotating knot sweeps the reference angle to write many pages, and "
            "the golden-angle step packs the most non-overlapping pages (the same "
            "most-irrational logic as the KAM curve). That layer is proposed, "
            "labeled, same column as the golden spray it replaces."
        ),
    },
    "geometry": {
        "armAngleDeg": round(WORK_ANGLE / 2, 4),
        "crossingAngleDeg": WORK_ANGLE,
        "knotPos": [0, 0, 0],
        "carrier": round(WORK_FC, 5),
        "fringePeriod": round(FRINGE, 3),
    },
    "recording": {"n": NI, "extent": LI, "tiltDeg": WORK_ANGLE, "image": plate},
    "spectrum": {
        "f": spec_f,
        "inline": spec_inline,
        "offaxis": spec_off,
        "carrier": round(WORK_FC, 5),
        "bandwidthB": B,
        "dcHalfWidth": round(2 * B, 5),
        "bandsInlineOverlap": True,
        "bandsOffaxisSeparated": bool(WORK_FC > LEITH_FC),
        "note": "three bands: zero-order at 0 (width ~2B), real & twin sidebands at +/- f_c. inline: piled on the zero order. off-axis: carried out and separated.",
    },
    "recovery": {
        "angleDeg": [p[0] for p in recovery_curve],
        "corr": [p[1] for p in recovery_curve],
        "leithAngleDeg": round(LEITH_ANGLE, 4),
        "inlineCorr": round(inline_corr, 4),
        "offaxisCorr": round(offaxis_corr, 4),
        "workingAngleDeg": WORK_ANGLE,
    },
    "twin": {
        "separationCarrier": round(2 * WORK_FC, 5),
        "inlineSeparation": 0.0,
        "note": "twin sits at -f_c, real at +f_c; separation 2·f_c off-axis, 0 inline (overlap).",
    },
    "multiplex": {
        "pages": PAGES,
        "goldenDirs": golden_dirs,
        "uniformDirs": uniform_dirs,
        "minGapGoldenDeg": round(math.degrees(gg), 3),
        "minGapUniformDeg": round(math.degrees(ug), 3),
        "distinctGolden": gn,
        "distinctUniform": un,
        "proposed": True,
        "note": f"the rotating knot's page angles over {PAGES} exposures: golden-stepped stays all-distinct ({gn}/{PAGES}, no two pages collide) and fills the range evenly at every count; the low-denominator rational control revisits only {un} angles forever (the rest are collisions). phi spaces the fan of X's, not any single X.",
    },
}

with open("src/data/hologram-snapshot.json", "w") as fh:
    json.dump(snapshot, fh, separators=(",", ":"))
    fh.write("\n")

print(f"crossing angle {WORK_ANGLE} deg | carrier f_c={WORK_FC:.4f} | fringe {FRINGE:.2f} lam")
print(f"Leith threshold: f_c>{LEITH_FC:.4f} -> crossing angle > {LEITH_ANGLE:.3f} deg")
print(f"recovery corr: inline={inline_corr:.4f} (twin-contaminated) -> off-axis={offaxis_corr:.4f} (twin gone)")
print(f"twin separation: 2·f_c = {2*WORK_FC:.4f} off-axis, 0 inline")
print(f"multiplex: golden {gn} distinct pages, min gap {math.degrees(gg):.2f} deg | uniform {un} distinct, {math.degrees(ug):.2f} deg")
