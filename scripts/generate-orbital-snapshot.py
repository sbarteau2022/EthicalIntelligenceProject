# ============================================================
# generate-orbital-snapshot.py
#
# The orbital anchor: the one place the atlas's stability logic touches
# measurable sky. Writes src/data/orbital-snapshot.json.
#
# WHAT IS COMPUTED (the mechanism, run live):
#   The Chirikov standard map — the canonical KAM system:
#       p' = p + (K/2pi) sin(2pi theta),  theta' = theta + p'  (mod 1)
#   For each winding ratio w we measure the kick strength K at which orbits
#   first TRANSPORT ACROSS a +/-0.045 band around w (majority of phase
#   seeds crossing within 6000 kicks). While any invariant torus in the
#   band survives, crossing is impossible — an invariant circle is an
#   absolute barrier — so this measures when the band's last torus dies.
#   It is a TRANSPORT PROXY, stated as such, not Greene's residue
#   criterion: it mixes torus survival with torus deformation and
#   overshoots Greene's K_c = 0.971635 for the golden torus by ~9% (our
#   measured value is stored beside the literature one). Its conjugacy
#   error is also stored: the standard map's symmetry demands w and 1-w
#   break together, and the measured pair 1/phi vs 1-1/phi agree to ~2%.
#   The landscape that falls out is the KAM survival curve: dips at every
#   rational (resonances die first, low denominators die hardest — 1/2
#   deepest, then 1/4, 1/3, 3/7, 2/5), high ground at the nobles, topped
#   at the golden winding 1/phi — the last torus to break.
#
# WHAT IS FORCED ARITHMETIC (Kepler's third law, no freedom):
#   A p:q resonance with Jupiter means period ratio w = q/p, and Kepler
#   maps it to semi-major axis a = a_J * w^(2/3). The four main Kirkwood
#   gaps (3:1, 5:2, 7:3, 2:1) computed this way land at 2.50, 2.82, 2.96,
#   3.28 AU — beside them we store the OBSERVED gap centers from the
#   asteroid census (literature data, typed and labeled as data).
#
# WHAT IS PRESENTATION:
#   The rendered belt is a deterministic sample whose radial density is
#   carved by the computed survival curve mapped through Kepler — so the
#   gaps you see in the render are cut by the standard-map mechanism, and
#   they land where the real gaps are because the arithmetic is forced.
#   Scene scales, sample counts, jitter amplitudes are drawing decisions.
#
# HONEST SCOPE: the belt's gaps at rational resonances are real, measured
# astronomy; the standard map is the textbook mechanism for why rational
# windings die. The GOLDEN claim stays in phase space: 1/phi is the most
# irrational winding and its torus is the last to break (KAM). The real
# belt spans windings ~0.25-0.55, so the golden winding lies OUTSIDE it —
# no claim is made that any planet or asteroid sits at a golden ratio.
# Deterministic throughout (seeded PRNG); rerunning reproduces the file.
# ============================================================

import json
import math
import random

PHI = (1 + 5**0.5) / 2
PHI_INV = 1 / PHI
TWO_PI = 2 * math.pi

# ---- the standard map survival sweep ----
A_J = 5.2044  # Jupiter semi-major axis, AU (data)

BAND = 0.045              # half-width of the transport band around each winding
SEEDS = [i / 8 + 0.041 for i in range(8)]  # theta starting phases
ITERS = 6000
K_LO, K_HI = 0.05, 1.45
BISECT = 8


def crosses(w, K, th0):
    # Start below the band; an invariant circle inside it is an absolute
    # barrier, so reaching the top edge proves the band's last torus is dead.
    theta, p = th0, w - BAND
    for _ in range(ITERS):
        p += (K / TWO_PI) * math.sin(TWO_PI * theta)
        theta = (theta + p) % 1.0
        if p >= w + BAND:
            return True
    return False


def broken(w, K):
    return sum(crosses(w, K, t) for t in SEEDS) >= len(SEEDS) // 2


def break_k(w):
    lo, hi = K_LO, K_HI
    if broken(w, lo):
        return lo
    if not broken(w, hi):
        return hi
    for _ in range(BISECT):
        mid = 0.5 * (lo + hi)
        if broken(w, mid):
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


W_SAMPLES = 321
W_MIN, W_MAX = 0.05, 0.95
curve = []
for i in range(W_SAMPLES):
    w = W_MIN + (W_MAX - W_MIN) * i / (W_SAMPLES - 1)
    curve.append([round(w, 6), round(break_k(w), 5)])

k_max = max(k for _, k in curve)

golden_k = break_k(PHI_INV)
golden_mirror_k = break_k(1 - PHI_INV)  # conjugacy check: map symmetry demands equality

# Fibonacci convergents of 1/phi — each a rational grave marching toward the
# golden survivor (their breakup K measured on the same proxy).
convergents = []
fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34]
for i in range(2, len(fibs) - 1):
    q, p = fibs[i], fibs[i + 1]
    w = q / p
    convergents.append({"num": q, "den": p, "w": round(w, 6), "breakK": round(break_k(w), 5)})

# ---- the Kirkwood gaps: forced Kepler arithmetic vs observed data ----
# p:q resonance -> period ratio w = q/p -> a = a_J * w^(2/3).
OBSERVED_AU = {"3:1": 2.502, "5:2": 2.825, "7:3": 2.958, "2:1": 3.279}  # data (observed gap centers)
resonances = []
for (p_, q_) in [(3, 1), (5, 2), (7, 3), (2, 1)]:
    w = q_ / p_
    a = A_J * w ** (2.0 / 3.0)
    label = f"{p_}:{q_}"
    resonances.append(
        {
            "label": label,
            "w": round(w, 6),
            "computedAU": round(a, 4),
            "observedAU": OBSERVED_AU[label],
            "breakK": round(break_k(w), 5),
        }
    )

# ---- the rendered belt, carved by the computed survival curve ----
BELT_A_MIN, BELT_A_MAX = 2.06, 3.50
N_ASTEROIDS = 2600
rng = random.Random(7)


def curve_at(w):
    if w <= curve[0][0]:
        return curve[0][1]
    if w >= curve[-1][0]:
        return curve[-1][1]
    t = (w - W_MIN) / (W_MAX - W_MIN) * (W_SAMPLES - 1)
    i = int(t)
    f = t - i
    return curve[i][1] * (1 - f) + curve[min(i + 1, W_SAMPLES - 1)][1] * f


# Carving weight: breakup K normalized by its rolling local maximum (window
# +/-0.05 in w), raised to a power. Normalizing locally keeps the carving
# driven by each resonance's own dip rather than the curve's global tilt; the
# exponent sets gap depth (a rendering choice, stated). Gap CENTERS come from
# the computed dips; gap WIDTHS inherit the proxy's +/-0.045 band and are
# wider than the real belt's — stated in meta, observed centers overlaid.
CARVE_WINDOW = 0.05
CARVE_POWER = 6.0


def local_max(w0):
    return max(k for w, k in curve if abs(w - w0) <= CARVE_WINDOW)


def carve_weight(w):
    return (curve_at(w) / local_max(w)) ** CARVE_POWER


asteroids = []
guard = 0
while len(asteroids) < N_ASTEROIDS and guard < N_ASTEROIDS * 60:
    guard += 1
    a = BELT_A_MIN + (BELT_A_MAX - BELT_A_MIN) * rng.random()
    w = (a / A_J) ** 1.5
    weight = carve_weight(w)  # the survival landscape carves the density
    if rng.random() > weight:
        continue
    asteroids.append(
        [
            round(a + rng.uniform(-0.015, 0.015), 4),   # semi-major axis + jitter
            round(rng.uniform(0, TWO_PI), 4),            # orbital phase
            round(rng.gauss(0, 0.05), 4),                # inclination (rad)
            round(rng.uniform(0, TWO_PI), 4),            # node
        ]
    )

snapshot = {
    "meta": {
        "title": "Orbital Atlas — the KAM anchor, locked",
        "phi": PHI,
        "phiInv": PHI_INV,
        "jupiterAU": A_J,
        "greeneKc": 0.971635,
        "goldenBreakK": round(golden_k, 5),
        "goldenMirrorBreakK": round(golden_mirror_k, 5),
        "curveMaxK": round(k_max, 5),
        "source": "generated by scripts/generate-orbital-snapshot.py — standard-map survival sweep (transport-proxy breakup criterion, stated as such) + Kepler resonance arithmetic + observed Kirkwood gap centers (data)",
        "note": (
            "The survival curve is computed live: breakup K per winding on the "
            "Chirikov standard map, transport-across-a-band proxy over phase "
            "seeds (not Greene's residue method; Greene's K_c=0.971635 for the "
            "golden torus is stored beside our measured proxy value, which "
            "overshoots it — the proxy mixes torus survival with deformation). "
            "The map's conjugacy symmetry demands w and 1-w break together; the "
            "measured golden pair is stored so the proxy's error is visible. Gap "
            "positions are forced Kepler arithmetic a = a_J*(q/p)^(2/3); observed "
            "centers are literature data. The rendered belt's density is carved "
            "by the computed curve, so its gaps are cut by the mechanism and land "
            "on the data. The golden winding lies outside the belt's winding "
            "window — the golden claim stays in phase space, where it belongs."
        ),
    },
    "survival": {
        "curve": curve,
        "wMin": W_MIN,
        "wMax": W_MAX,
        "band": BAND,
        "iters": ITERS,
        "seeds": [round(s, 4) for s in SEEDS],
    },
    "golden": {"w": PHI_INV, "breakK": round(golden_k, 5), "mirrorW": 1 - PHI_INV, "mirrorBreakK": round(golden_mirror_k, 5)},
    "convergents": convergents,
    "resonances": resonances,
    "belt": {
        "aMin": BELT_A_MIN,
        "aMax": BELT_A_MAX,
        "windingWindow": [round((BELT_A_MIN / A_J) ** 1.5, 4), round((BELT_A_MAX / A_J) ** 1.5, 4)],
        "asteroids": asteroids,
    },
    "jupiter": {"a": A_J, "periodYears": 11.862},
}

with open("src/data/orbital-snapshot.json", "w") as f:
    json.dump(snapshot, f, indent=1)

print(f"survival curve: {W_SAMPLES} windings, K in [{min(k for _, k in curve)}, {k_max}]")
print(f"golden torus (w=1/phi={PHI_INV:.6f}): breakK={golden_k:.5f} (Greene K_c=0.971635; mirror w=1-1/phi breakK={golden_mirror_k:.5f})")
for r in resonances:
    print(f"  {r['label']}: w={r['w']} computed a={r['computedAU']} AU, observed {r['observedAU']} AU, breakK={r['breakK']}")
print(f"belt: {len(asteroids)} asteroids, winding window {snapshot['belt']['windingWindow']}")
