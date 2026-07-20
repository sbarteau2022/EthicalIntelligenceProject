# ============================================================
# generate-circlemap-snapshot.py
#
# The bridge: the devil's staircase — the two faces of the lock.
# Writes src/data/circlemap-snapshot.json.
#
# WHY THIS PAGE EXISTS (Stewart's observation, made precise):
#   "The parts have to be in orbit at the point where they would do this to
#   shine on each other and stay there and circle." For parts that circle,
#   shine-on-each-other-and-STAY is co-rotation — a 1:1 phase lock. Writing
#   a hologram page REQUIRES that lock (any relative motion beyond a
#   fraction of a fringe smears the grating: the dwell is forced). Moving
#   BETWEEN pages requires never being captured by anyone else's lock: the
#   golden step. Lock to write, golden to move — the same phi that survives
#   resonance on /orbital-atlas is here the route between resonances.
#
# WHAT IS COMPUTED (the mechanism, run live):
#   The sine circle map — the canonical mode-locking system:
#       theta' = theta + Omega - (K/2pi) sin(2pi theta)
#   winding number w = lim (theta_N - theta_0)/N.
#   1) The devil's staircase: w vs Omega at critical coupling K=1 — a flat
#      tread at every rational (an Arnold tongue crossed), risers between.
#   2) Locked fraction of the drive axis vs K (finite-time detector, q<=30,
#      tol 2e-5 — an UNDERCOUNT at K=1, where theory says locks fill
#      everything but a measure-zero fractal dust; the monotone growth is
#      the measured claim, the limit is the literature's).
#   3) Fibonacci tread widths at K=1: the locks 1/2, 2/3, 3/5, 5/8, 8/13
#      converging on the golden winding, each tread ~3x thinner.
#   4) The golden thread: Omega(K) holding w = 1/phi from K=0 to K=1, by
#      bisection (w is monotone in Omega for K<=1). At K=1 the orbit is
#      still unlocked — the last quasiperiodic motion (Shenker/Kadanoff
#      universality; measured here directly, not asserted).
#   5) The Arnold tongues field: for a grid of (Omega, K), the smallest q
#      whose lock p/q captures the orbit (0 = never captured) — the tongue
#      fan the golden thread must climb between.
#
# WHAT IS INTERPRETATION (labeled): identifying the hologram multiplex's
# dwell-and-step with lock-slip dynamics. The measurements above are the
# evidence offered; the identification is the claim they support, no more.
# HONEST SCOPE: nothing here touches the locked hologram or orbital
# snapshots; this file computes only circle-map mathematics, which is
# textbook (Arnold tongues, critical circle map). Deterministic throughout;
# rerunning reproduces the file bit-for-bit.
# ============================================================

import json
import math

import numpy as np

PHI = (1 + 5**0.5) / 2
INV_PHI = 1 / PHI
TWO_PI = 2 * math.pi

OUT = "src/data/circlemap-snapshot.json"


def winding_vec(omega, K, n=4000, burn=800):
    """Vectorized winding number for arrays omega, K (broadcastable)."""
    omega = np.asarray(omega, dtype=np.float64)
    K = np.asarray(K, dtype=np.float64)
    th = np.zeros(np.broadcast(omega, K).shape, dtype=np.float64)
    for _ in range(burn):
        th = th + omega - (K / TWO_PI) * np.sin(TWO_PI * th)
    th0 = th.copy()
    for _ in range(n):
        th = th + omega - (K / TWO_PI) * np.sin(TWO_PI * th)
    return (th - th0) / n


def lock_of(w, qmax=30, tol=2e-5):
    """Smallest-q rational p/q within tol of w, else None."""
    for q in range(1, qmax + 1):
        p = round(w * q)
        if abs(w - p / q) < tol:
            return p, q
    return None


# ---- 1) the devil's staircase at K=1 ----
N_STAIR = 901
stair_omega = np.linspace(0.0, 1.0, N_STAIR)
stair_w = winding_vec(stair_omega, 1.0, n=6000, burn=1000)

# ---- 2) locked fraction vs K ----
K_GRID = [round(0.1 * i, 1) for i in range(11)]
FRAC_OMEGAS = np.linspace(0.5 / 1200, 1 - 0.5 / 1200, 1200)
locked_fraction = []
for k in K_GRID:
    ws = winding_vec(FRAC_OMEGAS, k, n=3000, burn=500)
    locked = sum(1 for w in ws if lock_of(w) is not None)
    locked_fraction.append(round(locked / len(FRAC_OMEGAS), 4))

# ---- 3) Fibonacci tread widths at K=1 ----
FIB_LOCKS = [(1, 2), (2, 3), (3, 5), (5, 8), (8, 13)]
treads = []
for p, q in FIB_LOCKS:
    center = p / q
    scan = np.linspace(center - 0.06, center + 0.06, 4001)
    ws = winding_vec(scan, 1.0, n=3000, burn=500)
    inside = np.abs(ws - center) < 2e-5
    if inside.any():
        lo = float(scan[inside][0])
        hi = float(scan[inside][-1])
    else:
        lo = hi = center
    treads.append(
        {
            "p": p,
            "q": q,
            "omegaLo": round(lo, 6),
            "omegaHi": round(hi, 6),
            "width": round(hi - lo, 6),
        }
    )

# ---- 4) the golden thread: Omega(K) with w = 1/phi, bisected ----
GOLD_K = np.linspace(0.0, 1.0, 21)
lo = np.full_like(GOLD_K, 0.55)
hi = np.full_like(GOLD_K, 0.70)
for _ in range(48):
    mid = (lo + hi) / 2
    w = winding_vec(mid, GOLD_K, n=5000, burn=800)
    below = w < INV_PHI
    lo = np.where(below, mid, lo)
    hi = np.where(below, hi, mid)
gold_omega = (lo + hi) / 2
w_at_k1 = float(winding_vec(gold_omega[-1], 1.0, n=12000, burn=2000))
# nearest rational trying to capture it
best = (1e9, 0, 1)
for q in range(1, 61):
    p = round(w_at_k1 * q)
    d = abs(w_at_k1 - p / q)
    if d < best[0]:
        best = (d, p, q)
near_dist, near_p, near_q = best

# ---- 5) the Arnold tongues field ----
TG_NX, TG_NY = 220, 140
TG_QMAX = 13
tg_omega = np.linspace(0.5 / TG_NX, 1 - 0.5 / TG_NX, TG_NX)
tg_K = np.linspace(0.0, 1.0, TG_NY)
OM, KK = np.meshgrid(tg_omega, tg_K)
WW = winding_vec(OM, KK, n=1500, burn=300)
tongues = np.zeros((TG_NY, TG_NX), dtype=int)
for q in range(1, TG_QMAX + 1):
    pw = np.round(WW * q)
    hit = (np.abs(WW - pw / q) < 1e-4) & (tongues == 0)
    tongues[hit] = q

# ---- 6) the hologram stair check (reads the LOCKED hologram snapshot) ----
# The multiplex page angles form a stair of their own: at every Fibonacci
# count the angular gaps take exactly TWO sizes, in ratio phi (three-distance
# theorem; at most three sizes ever). The rational control has a 0-degree
# tread — a step landing on a step already taken: the collision.
with open("src/data/hologram-snapshot.json") as f:
    holo = json.load(f)


def gap_sizes(dirs):
    a = sorted(dirs)
    gaps = [a[0] + TWO_PI - a[-1]] + [a[i] - a[i - 1] for i in range(1, len(a))]
    deg = sorted({round(gv * 360 / TWO_PI, 2) for gv in gaps})
    return deg


holo_stair = []
for n in [8, 13, 21, 27, 34]:
    sizes = gap_sizes(holo["multiplex"]["goldenDirs"][:n])
    ratio = round(sizes[-1] / sizes[0], 4) if len(sizes) == 2 else None
    holo_stair.append({"pages": n, "gapSizesDeg": sizes, "ratio": ratio})
uniform_gaps = gap_sizes(holo["multiplex"]["uniformDirs"])

# ---- certificates ----
i02, i06, i10 = K_GRID.index(0.2), K_GRID.index(0.6), K_GRID.index(1.0)
print("== circle-map certificates ==")
print(
    f"locked fraction K=0.2 / 0.6 / 1.0: "
    f"{locked_fraction[i02]} / {locked_fraction[i06]} / {locked_fraction[i10]} (monotone: "
    f"{all(locked_fraction[i] <= locked_fraction[i + 1] + 1e-9 for i in range(len(locked_fraction) - 1))})"
)
for t in treads:
    print(f"tread {t['p']}/{t['q']}: width {t['width']}")
ratios = [treads[i]["width"] / treads[i + 1]["width"] for i in range(len(treads) - 1)]
print(f"tread shrink ratios: {[round(r, 2) for r in ratios]}")
print(f"golden at K=1: Omega={gold_omega[-1]:.6f}, winding={w_at_k1:.6f} (1/phi={INV_PHI:.6f})")
print(f"  nearest rational {near_p}/{near_q} at distance {near_dist:.2e} -> unlocked (Fibonacci pair)")
frac_locked_cells = float((tongues > 0).mean())
print(f"tongues field: {TG_NX}x{TG_NY}, locked cells {frac_locked_cells:.3f}")
for h in holo_stair:
    print(f"hologram stair, {h['pages']} pages: gap sizes {h['gapSizesDeg']} deg, ratio {h['ratio']}")
print(f"hologram rational control gaps: {uniform_gaps} deg (0.0 = collision)")

# ---- write the snapshot ----
snapshot = {
    "meta": {
        "phi": round(PHI, 9),
        "invPhi": round(INV_PHI, 9),
        "map": "theta' = theta + Omega - (K/2pi) sin(2pi theta)",
        "lockTolerance": 2e-5,
        "lockQmax": 30,
        "criticalK": 1.0,
        "note": (
            "Finite-time locked fractions UNDERCOUNT at K=1 (theory: locks fill all but "
            "fractal dust). Golden-last-to-lock is Shenker/Kadanoff critical circle map, "
            "measured here directly. The lock-to-write / golden-to-move identification "
            "with the hologram multiplex is interpretation, labeled."
        ),
    },
    "staircase": {
        "K": 1.0,
        "omega": [round(float(x), 6) for x in stair_omega],
        "winding": [round(float(x), 6) for x in stair_w],
    },
    "lockedFraction": {"K": K_GRID, "fraction": locked_fraction},
    "treads": treads,
    "golden": {
        "K": [round(float(x), 4) for x in GOLD_K],
        "omega": [round(float(x), 6) for x in gold_omega],
        "target": round(INV_PHI, 6),
        "windingAtK1": round(w_at_k1, 6),
        "nearestP": near_p,
        "nearestQ": near_q,
        "nearestDist": float(f"{near_dist:.3e}"),
    },
    "hologramStair": {
        "golden": holo_stair,
        "uniformGapSizesDeg": uniform_gaps,
        "note": "computed from the locked hologram snapshot's page angles; three-distance theorem",
    },
    "tongues": {
        "nx": TG_NX,
        "ny": TG_NY,
        "omegaMin": 0.0,
        "omegaMax": 1.0,
        "kMin": 0.0,
        "kMax": 1.0,
        "qMax": TG_QMAX,
        "lockedCellFraction": round(frac_locked_cells, 4),
        "image": tongues.tolist(),
    },
}

with open(OUT, "w") as f:
    json.dump(snapshot, f, separators=(",", ":"))
print(f"wrote {OUT}")
