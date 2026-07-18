# ============================================================
# generate-hologram-snapshot.py
#
# The holographic anchor: "the cross-section is a hologram" — demonstrated,
# not illustrated. Writes src/data/hologram-snapshot.json. Requires numpy.
#
# THE CLAIM (Stewart's, verbatim): two bound emitters, trapped circling one
# another, projecting their inners out — and the cross-section of their
# joint field is a hologram.
#
# THE DEMONSTRATION (all computed here, no free parameters beyond stated
# scene choices):
#   1. Two point sources, PHASE-LOCKED (the coherence condition — without
#      the lock there is no hologram, only blur; the phase lock the whole
#      atlas is built around is exactly what holography requires), unit
#      amplitude, separation d, all lengths in wavelengths (lambda = 1).
#   2. Their exact interference field is evaluated on a recording plane —
#      the cross-section. Its intensity IS a hologram: it stores amplitude
#      AND phase of the pair in its fringes (Gabor's insight).
#   3. THE PROOF — the partner is the key. Because both sources sit at the
#      same depth, their cross-term phase is (paraxially) linear — the
#      classic Young fringes — so the slice alone under plane-wave
#      illumination does not refocus into points. The honest and stronger
#      statement: illuminate the recorded slice with the wave of ONE
#      partner (the reference each source is to the other), back-propagate
#      by the angular-spectrum method, and the OTHER partner reappears at
#      its true position. Keep either member of the bound pair and the
#      cross-section; the missing one is fully recoverable. The recovered
#      peak position is compared against truth and the error is stored, in
#      wavelengths. The twin-image halo of holography is present — stated,
#      visible, not hidden.
#   4. A second forced check on the recording side: the central fringe
#      period must equal lambda*Z/d (two-source interference arithmetic).
#      Predicted and measured values are both stored.
#
# THE PROPOSED LAYER (labeled as such): the golden spray. No binary emits
# at the golden angle (momentum conservation forces pair emission to 180
# degrees — stated in the snapshot). But IF a bound pair emits repeatedly
# and coverage must never self-overlap, the golden angle is the optimal
# advance, by the same most-irrational logic as the KAM curve: after N
# emissions the largest angular gap shrinks like 1/N, while any rational
# advance revisits a finite set of directions forever. Both are computed
# and stored: golden vs rational-advance directions and their measured
# largest gaps after 89 emissions.
#
# Deterministic: same inputs, byte-identical output.
# ============================================================

import json
import math

import numpy as np

PHI = (1 + 5**0.5) / 2
PHI_INV = 1 / PHI
GOLDEN_ANGLE = 2 * math.pi * (1 - PHI_INV)  # 137.5077...deg
TWO_PI = 2 * math.pi

# ---- scene (all lengths in wavelengths; drawing decisions, stated) ----
D_SEP = 12.0     # source separation
Z_PLANE = 60.0   # recording-plane distance
L_PLANE = 80.0   # recording-plane extent (square)
N_GRID = 512     # computation grid
N_STORE = 256    # stored/rendered grid (2x downsample)

K = TWO_PI  # wavenumber, lambda = 1

# ---- 1+2. the exact field of the phase-locked pair on the cross-section ----
xs = np.linspace(-L_PLANE / 2, L_PLANE / 2, N_GRID)
X, Y = np.meshgrid(xs, xs)
R1 = np.sqrt((X + D_SEP / 2) ** 2 + Y**2 + Z_PLANE**2)  # partner to RECOVER
R2 = np.sqrt((X - D_SEP / 2) ** 2 + Y**2 + Z_PLANE**2)  # partner used as the KEY
E1 = np.exp(1j * K * R1) / R1
E2 = np.exp(1j * K * R2) / R2
I = (np.abs(E1 + E2) ** 2)  # the hologram: the cross-section's intensity

# ---- 4. forced check: central fringe period ~ lambda*Z/d (paraxial) ----
predicted_period = Z_PLANE / D_SEP  # in wavelengths (lambda = 1)
center_row = I[N_GRID // 2, :]
# measure spacing of fringe maxima on the positive-x side (0..15 lambda);
# a tie tolerance keeps the near-axis peak, which falls between grid samples
side = (xs >= -0.5) & (xs <= 15.0)
row = center_row[side]
xr = xs[side]
tol = row.max() * 1e-6
peaks = [
    xr[i]
    for i in range(1, len(row) - 1)
    if row[i] >= row[i - 1] - tol and row[i] >= row[i + 1] - tol and row[i] > 0.5 * row.max()
]
# collapse plateau duplicates
dedup = [peaks[0]] if peaks else []
for p in peaks[1:]:
    if p - dedup[-1] > 1.0:
        dedup.append(p)
measured_period = float(np.mean(np.diff(dedup))) if len(dedup) > 1 else float("nan")

# ---- 3. the proof: the partner is the key ----
# Illuminate the recorded slice with partner 2's exact wave, back-propagate
# to the source plane; partner 1 reappears where it truly is.
U = I * E2
A = np.fft.fft2(U)
fx = np.fft.fftfreq(N_GRID, d=L_PLANE / N_GRID)
FX, FY = np.meshgrid(fx, fx)
arg = 1.0 - FX**2 - FY**2  # (lambda*f)^2 with lambda = 1
prop = np.where(arg > 0, np.exp(-1j * K * Z_PLANE * np.sqrt(np.maximum(arg, 0.0))), 0.0)
U_src = np.fft.ifft2(A * prop)  # field reconstructed at the source plane
R_int = (np.abs(U_src) ** 2)


def peak_pos(mask):
    masked = np.where(mask, R_int, 0.0)
    idx = np.unravel_index(np.argmax(masked), masked.shape)
    return float(xs[idx[1]]), float(xs[idx[0]])


px_l, py_l = peak_pos(X < -1.0)  # the RECOVERED partner (true pos: -d/2, 0)
px_r, py_r = peak_pos(X > 1.0)   # the supplied key, refocusing at its own seat
err_l = math.hypot(px_l + D_SEP / 2, py_l)
err_r = math.hypot(px_r - D_SEP / 2, py_r)

# ---- quantize both planes for the renderer (gamma for visibility) ----
def quantize(plane):
    p = plane[::2, ::2] if plane.shape[0] == N_GRID else plane
    p = p / p.max()
    p = np.sqrt(p)  # gamma 0.5, a display choice
    return [[int(round(v * 255)) for v in row] for row in p]

holo_q = quantize(I)
recon_q = quantize(R_int)

# ---- the golden spray (proposed layer) ----
N_EMIT = 89  # a Fibonacci number of emissions
golden_dirs = [round((n * GOLDEN_ANGLE) % TWO_PI, 6) for n in range(N_EMIT)]
RATIONAL_STEP = TWO_PI * 3 / 8
rational_dirs = [round((n * RATIONAL_STEP) % TWO_PI, 6) for n in range(N_EMIT)]
def max_gap(dirs):
    s = sorted(set(dirs))
    gaps = [s[(i + 1) % len(s)] - s[i] for i in range(len(s) - 1)] + [s[0] + TWO_PI - s[-1]]
    return max(gaps)
gap_golden = max_gap(golden_dirs)
gap_rational = max_gap(rational_dirs)

snapshot = {
    "meta": {
        "title": "Holographic Atlas — the cross-section, proven",
        "phi": PHI,
        "phiInv": PHI_INV,
        "goldenAngleDeg": round(math.degrees(GOLDEN_ANGLE), 4),
        "lambdaUnit": 1.0,
        "separation": D_SEP,
        "planeZ": Z_PLANE,
        "planeSize": L_PLANE,
        "source": "generated by scripts/generate-hologram-snapshot.py — exact two-source interference, angular-spectrum back-propagation, all checks computed (requires numpy)",
        "note": (
            "Two phase-locked point sources; their exact interference field is "
            "evaluated on a recording plane (the cross-section), whose intensity "
            "is a hologram. Proof — the partner is the key: because the pair sit "
            "at equal depth their cross-fringes are (paraxially) Young fringes, "
            "so the slice alone does not refocus; illuminate the recorded slice "
            "with EITHER partner's wave, back-propagate (angular spectrum), and "
            "the OTHER partner reappears at its true position (recovered-peak "
            "error stored, in wavelengths — the supplied key also refocuses at "
            "its own seat, as it must). The twin-image halo of holography is "
            "present and visible, not hidden. The phase lock is the coherence "
            "condition: unlocked sources leave no fringes and nothing to "
            "reconstruct. The golden-spray layer is PROPOSED, not observed: real "
            "pair emission is momentum-locked to 180 degrees; the golden angle "
            "enters only as the optimal advance for repeated non-overlapping "
            "emission, computed here against a rational control."
        ),
    },
    "checks": {
        "fringePeriodPredicted": round(predicted_period, 4),
        "fringePeriodMeasured": round(measured_period, 4),
        "recoveredPartner": [round(px_l, 3), round(py_l, 3)],
        "recoveredTruth": [-D_SEP / 2, 0.0],
        "recoveredErrorLambda": round(err_l, 3),
        "keyRefocus": [round(px_r, 3), round(py_r, 3)],
        "keyTruth": [D_SEP / 2, 0.0],
        "keyErrorLambda": round(err_r, 3),
    },
    "sources": {
        "positions": [[-D_SEP / 2, 0.0, 0.0], [D_SEP / 2, 0.0, 0.0]],
        "phaseLocked": True,
    },
    "hologram": {"n": N_STORE, "extent": L_PLANE, "z": Z_PLANE, "intensity": holo_q},
    "reconstruction": {"n": N_STORE, "extent": L_PLANE, "z": 0.0, "intensity": recon_q},
    "goldenSpray": {
        "emissions": N_EMIT,
        "goldenDirs": golden_dirs,
        "rationalDirs": rational_dirs,
        "rationalStepDeg": 135.0,
        "maxGapGoldenDeg": round(math.degrees(gap_golden), 3),
        "maxGapRationalDeg": round(math.degrees(gap_rational), 3),
        "proposed": True,
    },
}

with open("src/data/hologram-snapshot.json", "w") as f:
    json.dump(snapshot, f, separators=(",", ":"))
    f.write("\n")

print(f"fringe period: predicted {predicted_period:.4f} lambda (paraxial), measured {measured_period:.4f} lambda")
print(f"RECOVERED partner ({px_l:.3f}, {py_l:.3f}) vs truth ({-D_SEP/2}, 0) -> error {err_l:.3f} lambda")
print(f"key refocus       ({px_r:.3f}, {py_r:.3f}) vs truth ({D_SEP/2}, 0) -> error {err_r:.3f} lambda")
print(f"golden spray after {N_EMIT}: max gap {math.degrees(gap_golden):.2f} deg | rational 3/8 control: {math.degrees(gap_rational):.2f} deg")
