# ============================================================
# generate-fracture-snapshot.py
#
# Past the gate: the collapse of invertibility, and what gets made.
# Writes src/data/fracture-snapshot.json.
#
# Stewart's framing, verified before building: past full criticality
# (K > 1) the circle map folds over itself — the derivative goes negative
# in local regions, tongues overlap, the system becomes multi-stable with
# hysteresis, and smooth quasi-periodic motion breaks into discrete phase
# slips. Lifted into space, slips become topological defects (1D ring:
# quantized winding-charge jumps; 2D: vortex pairs / BKT; 3D: defect and
# knot lines; Skyrme: winding quantization stabilizes solitons). All of
# that is canon. What this generator does is MEASURE the 1D content:
#
# WHAT IS FORCED (arithmetic, no freedom):
#   f'(theta) = 1 - K cos(2pi theta), so min f' = 1 - K. The fold appears
#   EXACTLY at K > 1. Invertibility collapse IS the gate.
#
# WHAT IS COMPUTED (deterministic, certificates printed):
#   1) The rotation interval opening: spread of winding over seeds at the
#      golden dial (Omega from the LOCKED circlemap snapshot) across the
#      gate — ~8e-5 below, ~2e-3 just above (a ~x20 jump).
#   2) Chaos is impossible below the gate: max Lyapunov exponent over the
#      dial stays <= ~0 for K <= 1 and goes positive only past it.
#   3) The capture of the old golden route: holding the K=1 golden dial
#      and raising K, the winding is swallowed by Fibonacci locks —
#      5/8 near K=1.08, 2/3 by K=1.4. The thread lives exactly to the
#      gate; the theorem's content, seen from above.
#   4) Overlapping tongues: at K=1.25, dial settings where DIFFERENT
#      locks coexist depending only on the starting phase.
#   5) Hysteresis: up-sweep vs down-sweep of the dial disagree — memory.
#   6) GENERATION, the smallest true instance: a ring of 64 coupled
#      phase oscillators. Its winding number is an integer topological
#      charge that can only change via a phase slip. Strong coupling:
#      charge frozen forever (the foil). Weak coupling: the charge changes
#      ONLY in discrete integer jumps (histogram stored; a |dM|=2 tick is
#      two bonds slipping in the same step) and is conserved between
#      events. Defect generation, quantized, measured.
#
# WHAT STAYS LITERATURE-TYPED (real, cited, not simulated here): the 2D
# vortex-antivortex lift (Berezinskii-Kosterlitz-Thouless), 3D defect and
# knot lines, Faddeev-Niemi knotted solitons (torus-knot-shaped), Skyrme
# solitons. WHAT STAYS INTERPRETATION (labeled): "maximal information
# capacity at K=1" (no defined measure yet — Predicted column), and the
# traversal-to-generation reading itself, for which the ring measurement
# is the supporting evidence.
#
# Deterministic throughout (LCG-seeded); rerunning reproduces the file.
# ============================================================

import json
import math

import numpy as np

TWO_PI = 2 * math.pi
OUT = "src/data/fracture-snapshot.json"

# one source of truth: the golden dial comes from the locked circlemap snapshot
with open("src/data/circlemap-snapshot.json") as f:
    _cm = json.load(f)
OM_G = _cm["golden"]["omega"][-1]


def winding_vec(omega, K, th0=0.0, n=4000, burn=800):
    omega = np.asarray(omega, dtype=np.float64)
    K = np.asarray(K, dtype=np.float64)
    th = np.full(np.broadcast(omega, K).shape, th0, dtype=np.float64)
    for _ in range(burn):
        th = th + omega - (K / TWO_PI) * np.sin(TWO_PI * th)
    a = th.copy()
    for _ in range(n):
        th = th + omega - (K / TWO_PI) * np.sin(TWO_PI * th)
    return (th - a) / n


def lock_of(w, qmax=40, tol=2e-4):
    best = None
    for q in range(1, qmax + 1):
        p = round(w * q)
        d = abs(w - p / q)
        if d < tol:
            return (p, q)
    return best


# ---- 1) the rotation interval across the gate ----
K_INT = [0.8, 0.9, 0.95, 0.99, 1.0, 1.02, 1.05, 1.1, 1.2, 1.3, 1.4]
SEEDS = np.array([i / 24 + 0.013 for i in range(24)])
interval = []
for K in K_INT:
    ws = np.array([float(winding_vec(OM_G, K, th0=float(s), n=4000, burn=800)) for s in SEEDS])
    interval.append({"K": K, "min": round(float(ws.min()), 6), "max": round(float(ws.max()), 6), "width": round(float(ws.max() - ws.min()), 6)})
w_below = max(r["width"] for r in interval if r["K"] <= 1.0)
w_above = next(r["width"] for r in interval if r["K"] == 1.05)

# ---- 2) chaos is impossible below the gate: max Lyapunov over the dial ----
K_LYAP = [0.5, 0.7, 0.85, 0.95, 1.0, 1.05, 1.1, 1.2, 1.3, 1.4, 1.5]
OMS = np.linspace(0.02, 0.98, 240)
maxlyap = []
for K in K_LYAP:
    th = np.full(OMS.shape, 0.13)
    for _ in range(600):
        th = th + OMS - (K / TWO_PI) * np.sin(TWO_PI * th)
    acc = np.zeros(OMS.shape)
    NL = 6000
    for _ in range(NL):
        acc += np.log(np.abs(1.0 - K * np.cos(TWO_PI * th)) + 1e-300)
        th = th + OMS - (K / TWO_PI) * np.sin(TWO_PI * th)
    maxlyap.append({"K": K, "maxLyap": round(float((acc / NL).max()), 5)})
below = [r["maxLyap"] for r in maxlyap if r["K"] <= 1.0]
above = [r["maxLyap"] for r in maxlyap if r["K"] > 1.0]

# ---- 3) the capture of the old golden route ----
capture = []
for i in range(19):
    K = round(1.0 + 0.025 * i, 3)
    w = float(winding_vec(OM_G, K, th0=0.13, n=6000, burn=1200))
    lk = lock_of(w)
    capture.append({"K": K, "winding": round(w, 6), "captor": f"{lk[0]}/{lk[1]}" if lk else None})

# ---- 4) overlapping tongues at K=1.25 ----
K_OV = 1.25
OV_OMS = np.linspace(0.25, 0.45, 320)
overlap = []
n_multi = 0
for Om in OV_OMS:
    ws = sorted(set(round(float(winding_vec(float(Om), K_OV, th0=s / 12 + 0.02, n=2200, burn=500)), 3) for s in range(12)))
    multi = len(ws) > 1
    n_multi += int(multi)
    overlap.append({"omega": round(float(Om), 5), "states": len(ws), "windings": ws if multi else [ws[0]]})
ov_examples = [o for o in overlap if o["states"] > 1][:4]

# ---- 5) hysteresis at K=1.25 ----
def sweep(oms, K):
    th, out = 0.13, []
    for Om in oms:
        a = th
        for _ in range(1800):
            th = th + Om - K / TWO_PI * math.sin(TWO_PI * th)
        out.append(round((th - a) / 1800, 4))
    return out


HYS_OMS = [round(0.30 + 0.40 * i / 60, 5) for i in range(61)]
hys_up = sweep(HYS_OMS, K_OV)
hys_dn = sweep(list(reversed(HYS_OMS)), K_OV)[::-1]
hys_disagree = sum(1 for a, b in zip(hys_up, hys_dn) if abs(a - b) > 5e-3)

# ---- 6) generation: the ring, the smallest true topological instance ----
N_RING = 64
T_RING = 1200
FRAME_EVERY = 4


def lcg(seed):
    s = seed
    while True:
        s = (1103515245 * s + 12345) % (2**31)
        yield 2.0 * s / (2**31) - 1.0


def wrapc(x):
    return x - round(x)


def ring_charge(th):
    return round(sum(wrapc(th[(i + 1) % N_RING] - th[i]) for i in range(N_RING)))


def run_ring(C, spread=0.02, seed=11):
    g = lcg(seed)
    om = [spread * next(g) for _ in range(N_RING)]
    th = [i / N_RING for i in range(N_RING)]  # charge +1 wound in
    charges = [ring_charge(th)]
    frames = [[round(x % 1.0, 3) for x in th]]
    slips = []
    for t in range(T_RING):
        new = []
        for i in range(N_RING):
            d1 = wrapc(th[(i + 1) % N_RING] - th[i])
            d0 = wrapc(th[(i - 1) % N_RING] - th[i])
            new.append(th[i] + om[i] + C * (math.sin(TWO_PI * d1) + math.sin(TWO_PI * d0)) / TWO_PI)
        th = new
        m = ring_charge(th)
        if m != charges[-1]:
            slips.append({"t": t + 1, "dM": m - charges[-1]})
        charges.append(m)
        if (t + 1) % FRAME_EVERY == 0:
            frames.append([round(x % 1.0, 3) for x in th])
    return {"coupling": C, "charge0": charges[0], "chargeT": charges[-1], "charges": charges, "slips": slips, "frames": frames}


ring_locked = run_ring(0.5)
ring_frac = run_ring(0.08)
from collections import Counter
jump_hist = dict(sorted(Counter(abs(s["dM"]) for s in ring_frac["slips"]).items()))
ring_locked_slim = {k: ring_locked[k] for k in ("coupling", "charge0", "chargeT")}
ring_locked_slim["slipCount"] = len(ring_locked["slips"])

# ---- certificates ----
print("== fracture certificates ==")
print(f"gate (forced): min f' = 1-K -> folds exactly at K>1")
print(f"golden dial (from locked circlemap snapshot): Omega = {OM_G}")
print(f"interval width below gate (max K<=1): {w_below}  |  at K=1.05: {w_above}  (x{w_above / max(w_below, 1e-9):.0f})")
print(f"max Lyapunov below gate: {max(below)} (finite-time zero)  |  above gate: {max(above)}  (chaos only past the gate: {max(below) < 0.002 and max(above) > 0.05})")
trail = [c for c in capture if c["captor"]]
print(f"capture trail at the old golden dial: " + " -> ".join(f"K={c['K']}:{c['captor']}" for c in trail[:3]) + f" ... K={trail[-1]['K']}:{trail[-1]['captor']}")
print(f"overlapping tongues at K={K_OV}: {n_multi}/{len(overlap)} dial settings multi-stable; e.g. " + "; ".join(f"Omega={o['omega']}:{o['windings']}" for o in ov_examples[:2]))
print(f"hysteresis at K={K_OV}: up vs down sweeps disagree at {hys_disagree}/61 settings")
print(f"ring locked  (C=0.5):  charge {ring_locked['charge0']} -> {ring_locked['chargeT']}, slip events = {len(ring_locked['slips'])}  (the foil: frozen)")
print(f"ring fractured (C=0.08): charge {ring_frac['charge0']} -> {ring_frac['chargeT']}, slip events = {len(ring_frac['slips'])}, |dM| histogram = {jump_hist}")
print(f"  -> the charge changes ONLY in discrete integer jumps (a |dM|=2 tick is two bonds slipping in the same step); it is conserved between events")

# ---- write ----
snapshot = {
    "meta": {
        "goldenDial": OM_G,
        "gate": {"formula": "min f' = 1 - K", "K": 1.0},
        "note": (
            "1D measurements only. The 2D/3D lift (BKT vortex pairs, defect and knot "
            "lines, Faddeev-Niemi knotted solitons, Skyrme) is literature-typed, not "
            "simulated. 'Maximal information capacity at K=1' has no defined measure "
            "yet and stays in the Predicted column. The traversal-to-generation "
            "reading is interpretation; the ring measurement is its evidence."
        ),
    },
    "gate": {"K": [round(0.5 + 0.1 * i, 2) for i in range(11)], "minDeriv": [round(1 - (0.5 + 0.1 * i), 2) for i in range(11)]},
    "interval": interval,
    "chaos": maxlyap,
    "capture": capture,
    "overlap": {"K": K_OV, "points": overlap, "multiCount": n_multi},
    "hysteresis": {"K": K_OV, "omega": HYS_OMS, "up": hys_up, "down": hys_dn, "disagree": hys_disagree},
    "ring": {
        "n": N_RING,
        "steps": T_RING,
        "frameEvery": FRAME_EVERY,
        "locked": ring_locked_slim,
        "fractured": {
            "coupling": ring_frac["coupling"],
            "charge0": ring_frac["charge0"],
            "chargeT": ring_frac["chargeT"],
            "charges": ring_frac["charges"],
            "slips": ring_frac["slips"],
            "frames": ring_frac["frames"],
            "jumpHistogram": jump_hist,
        },
    },
}
with open(OUT, "w") as f:
    json.dump(snapshot, f, separators=(",", ":"))
print(f"wrote {OUT}")
