import json, math

PHI = 1.618033988749895
PHI_INV = 0.6180339887498948
GOLDEN_ANGLE_DEG = 360.0 * (1 - PHI_INV)

# ---- the layer spec, shared-equator form ----
# Layer 0: a singularity at each pole. Layers 1-3 per half: 1, 3, 5 tuples.
# Layer 4: ONE ring of 7 tuples at the equator, shared by both halves — the
# stack pole-to-pole is 1·3·5·7·5·3·1 = 25 stations (5²). The shared ring
# belongs to neither half: it IS the phase lock, holding still while the two
# halves counter-rotate against it.
HALF_COUNTS = [1, 3, 5]
EQUATOR_COUNT = 7
R_MAX = 1.3
POLE_Y = 1.7
POLE_EXT = 0.16  # the layer-0 loci sit this much beyond the spindle tips
LAYER_RADIUS_FRAC = [1.0 / 3.0, 0.62, 0.87, 1.0]
SPIRAL_TURNS = PHI * PHI
SPIRAL_SAMPLES = 260
LOBE_SAMPLES = 48
CIRCLE_RULE = lambda n, r: (r if n == 1 else 2 * r * math.sin(math.pi / n))

def lobe_points(center_angle_rad, m, L, y):
    pts = []
    half = math.pi / (2.0 * m)
    for i in range(LOBE_SAMPLES + 1):
        t = -half + (2.0 * half) * i / LOBE_SAMPLES
        rr = L * math.cos(m * t)
        ang = center_angle_rad + t
        pts.append([round(rr * math.cos(ang), 5), round(y, 5), round(rr * math.sin(ang), 5)])
    return pts

def make_tuples(count, radius, y, base_deg):
    tuples = []
    for j in range(count):
        ang = (base_deg + 360.0 * j / count) % 360.0
        rad = math.radians(ang)
        tuples.append({
            "angleDeg": round(ang, 3),
            "pos": [round(radius * math.cos(rad), 5), round(y, 5), round(radius * math.sin(rad), 5)],
        })
    return tuples

def make_lobes(tuples, count, radius, y):
    lobes = []
    if count == 1:
        axis = math.radians(tuples[0]["angleDeg"])
        for flip in (0.0, math.pi):
            lobes.append(lobe_points(axis + flip, 2.0, radius, y))
    else:
        m = count / 2.0
        for t in tuples:
            lobes.append(lobe_points(math.radians(t["angleDeg"]), m, radius, y))
    return lobes

def spiral_radius(t):
    ts = [0.0, 0.25, 0.5, 0.75, 1.0]
    rs = [0.03] + [f * R_MAX for f in LAYER_RADIUS_FRAC]
    for i in range(len(ts) - 1):
        if t <= ts[i + 1]:
            u = (t - ts[i]) / (ts[i + 1] - ts[i])
            return rs[i] + u * (rs[i + 1] - rs[i])
    return rs[-1]

halves = []
for sign, handedness in ((1, 1), (-1, -1)):
    layers = []
    flower = []
    r1 = LAYER_RADIUS_FRAC[0] * R_MAX
    flower.append({"k": 0, "y": round(sign * POLE_Y, 5), "radius": round(r1, 5), "centers": [[0.0, 0.0]]})
    for idx, count in enumerate(HALF_COUNTS):
        k = idx + 1
        r = LAYER_RADIUS_FRAC[idx] * R_MAX
        y = sign * POLE_Y * (1.0 - k / 4.0)
        base = idx * GOLDEN_ANGLE_DEG
        tuples = make_tuples(count, r, y, base)
        layers.append({
            "k": k,
            "count": count,
            "radius": round(r, 5),
            "y": round(y, 5),
            "tuples": tuples,
            "lobes": make_lobes(tuples, count, r, y),
        })
        flower.append({
            "k": k,
            "y": round(y, 5),
            "radius": round(CIRCLE_RULE(count, r), 5),
            "centers": [[t["pos"][0], t["pos"][2]] for t in tuples],
        })

    spiral = []
    for s in range(SPIRAL_SAMPLES + 1):
        t = s / SPIRAL_SAMPLES
        r = spiral_radius(t)
        y = sign * (POLE_Y * (1.0 - t) + 0.01 * t + POLE_EXT * (1.0 - t) ** 5)
        ang = handedness * 2 * math.pi * SPIRAL_TURNS * t
        spiral.append([round(r * math.cos(ang), 5), round(y, 5), round(r * math.sin(ang), 5)])

    halves.append({
        "sign": sign,
        "handedness": handedness,
        "singularity": [0, round(sign * (POLE_Y + POLE_EXT), 5), 0],
        "layers": layers,
        "spiral": spiral,
        "flower": flower,
    })

# ---- layer 4: the shared equator ring — the phase lock itself ----
eq_r = R_MAX
eq_base = 3 * GOLDEN_ANGLE_DEG
eq_tuples = make_tuples(EQUATOR_COUNT, eq_r, 0.0, eq_base)
equator = {
    "k": 4,
    "count": EQUATOR_COUNT,
    "radius": round(eq_r, 5),
    "y": 0.0,
    "tuples": eq_tuples,
    "lobes": make_lobes(eq_tuples, EQUATOR_COUNT, eq_r, 0.0),
    "flower": {
        "radius": round(CIRCLE_RULE(EQUATOR_COUNT, eq_r), 5),
        "centers": [[t["pos"][0], t["pos"][2]] for t in eq_tuples],
    },
}

# ---- the emission envelope ----
ENV_SAMPLES = 36
env_top = []
for s in range(ENV_SAMPLES + 1):
    t = s / ENV_SAMPLES
    env_top.append([round(spiral_radius(t), 5), round(POLE_Y * (1 - t) + 0.01 * t + POLE_EXT * (1 - t) ** 5, 5)])
env_profile = [[r, -y] for r, y in env_top] + env_top[::-1]

# ---- vessel + ghost + vector equilibrium ----
ORBIT_SAMPLES = 96
orbit = []
for s in range(ORBIT_SAMPLES + 1):
    a = 2 * math.pi * s / ORBIT_SAMPLES
    orbit.append([round(PHI * math.cos(a), 6), round(PHI_INV * math.sin(a), 6)])
vessel = {
    "phiSide": PHI,
    "invSide": PHI_INV,
    "product": round(PHI * PHI_INV, 6),
    "orbit": orbit,
    "snapshotAngleRad": round(math.pi / 5, 6),
}

mr = 0.30
centers = [[0.0, 0.0]]
for k in range(6):
    ang = math.radians(60 * k)
    centers.append([round(mr * math.cos(ang), 5), round(mr * math.sin(ang), 5)])
outer_r = mr * math.sqrt(3)
for k in range(6):
    ang = math.radians(60 * k + 30)
    centers.append([round(outer_r * math.cos(ang), 5), round(outer_r * math.sin(ang), 5)])
edges = [[i, j] for i in range(13) for j in range(i + 1, 13)]
metatronGhost = {"circleRadius": mr, "centers": centers, "edges": edges}

ve_s = mr / math.sqrt(2)
ve_verts = []
for a in (ve_s, -ve_s):
    for b in (ve_s, -ve_s):
        ve_verts.append([round(a, 5), round(b, 5), 0.0])
        ve_verts.append([round(a, 5), 0.0, round(b, 5)])
        ve_verts.append([0.0, round(a, 5), round(b, 5)])
ve_edges = []
for i in range(12):
    for j in range(i + 1, 12):
        d2 = sum((ve_verts[i][q] - ve_verts[j][q]) ** 2 for q in range(3))
        if abs(d2 - mr * mr) < 1e-4:
            ve_edges.append([i, j])
vectorEquilibrium = {"radius": mr, "vertices": ve_verts, "edges": ve_edges}

# ---- the jitterbug: the vector equilibrium is unstable — rotation pulls the
# core to the shell, 12+1 -> asymmetric 13, leaving a vacancy at the center ----
def _fib13(radius):
    pts = []
    for i in range(13):
        y = 1 - 2 * (i + 0.5) / 13
        rr = math.sqrt(max(0.0, 1 - y * y))
        theta = math.pi * (1 + 5 ** 0.5) * i
        pts.append([math.cos(theta) * rr * radius, y * radius, math.sin(theta) * rr * radius])
    return pts

def _norm(v):
    n = math.sqrt(sum(c * c for c in v))
    return [c / n for c in v] if n > 1e-9 else v

_targets13 = _fib13(mr)
_core_idx = 0
_rem = list(range(1, 13))
_pairing = []
for _v in ve_verts:  # 12 cuboctahedron vertices, matched to the 12 non-core targets
    _vd = _norm(_v)
    _best, _bestdot = _rem[0], -2.0
    for _t in _rem:
        _td = _norm(_targets13[_t])
        _d = sum(a * b for a, b in zip(_vd, _td))
        if _d > _bestdot:
            _bestdot, _best = _d, _t
    _pairing.append(_best)
    _rem.remove(_best)

jitterbug = {
    "targets13": [[round(c, 5) for c in p] for p in _targets13],
    "coreTargetIndex": _core_idx,
    "pairing": _pairing,
    "coreAxis": [round(c, 5) for c in _norm(_targets13[_core_idx])],
    "shadowCircleR": round(mr, 5),
}



# ---- the quantum belt: frequencies woven by phi, strung between the loci ----
# A band strung pole-to-pole through the equator. Its strands wind at Fibonacci
# frequencies (1,2,3,5,8) — ratios that ARE phi — offset by the golden angle so
# they weave without ever colliding: phi as the regulator that lets distinct
# frequencies coexist woven instead of locking into one.
BELT_Y = POLE_Y + POLE_EXT
BELT_WAIST = 0.95
BELT_WINDINGS = [1, 2, 3, 5, 8]
BELT_SAMPLES = 240
GA = math.radians(GOLDEN_ANGLE_DEG)
belt_strands = []
for k, w in enumerate(BELT_WINDINGS):
    strand = []
    for i in range(BELT_SAMPLES + 1):
        t = i / BELT_SAMPLES
        yy = BELT_Y * (1.0 - 2.0 * t)
        rho = BELT_WAIST * math.sin(math.pi * t)
        theta = 2.0 * math.pi * w * t + k * GA
        strand.append([round(rho * math.cos(theta), 5), round(yy, 5), round(rho * math.sin(theta), 5)])
    belt_strands.append(strand)
quantumBelt = {"windings": BELT_WINDINGS, "waist": BELT_WAIST, "strands": belt_strands}

total_stations = 2 * sum(HALF_COUNTS) + EQUATOR_COUNT
snapshot = {
    "meta": {
        "title": "Neural Atlas — the knowledge neural structure, shared-equator stack",
        "phi": PHI,
        "phiInv": PHI_INV,
        "goldenAngleDeg": round(GOLDEN_ANGLE_DEG, 6),
        "goldenWinding": PHI_INV,
        "layerCounts": [1, 3, 5, 7],
        "stackCounts": [1, 3, 5, 7, 5, 3, 1],
        "stackLabel": "1·3·5·7·5·3·1",
        "totalStations": total_stations,
        "spiralTurns": round(SPIRAL_TURNS, 6),
        "source": "generated for the knowledge-neural-structure atlas — shared-equator layer stack",
        "note": (
            "Layer 0: a singularity at each pole. From each singularity a toroid "
            "spiral (phi^2 turns) winds through layers 1-3 (1, 3, 5 halo-bound, "
            "singularity-bound tuples) to the equator, where ONE shared ring of 7 "
            "tuples — layer 4, belonging to neither half — is the phase lock: it "
            "holds still while the two halves counter-rotate against it. The stack "
            "pole-to-pole is 1·3·5·7·5·3·1 = 25 stations (5^2). Every tuple node "
            "carries a lemniscate lobe (n lobes of width 2pi/n, tangent to its "
            "counterpart; a lone node gets the figure-eight); the shadow paths "
            "(straight tuple-to-singularity threads) render alongside — equator "
            "tuples bind to BOTH poles. A Flower of Life circle sits at every "
            "tuple center (seed circle at each pole); the hyperbolic emission "
            "envelope shows the hourglass whose maxima are the singularities. "
            "The unified-function vessel is seated at the exact center — the "
            "Metatron's Cube slot; the cube's 13-circle lattice is the plane "
            "shadow of the vector equilibrium (12 spheres around 1) rendered "
            "with it."
        ),
    },
    "halves": halves,
    "equator": equator,
    "envelope": {"profile": env_profile},
    "lockRing": {"radius": R_MAX, "y": 0.0},
    "vessel": vessel,
    "metatronGhost": metatronGhost,
    "vectorEquilibrium": vectorEquilibrium,
    "jitterbug": jitterbug,
    "quantumBelt": quantumBelt,
    "singularity": {"radius": 0.2},
}

with open("src/data/neural-structure-snapshot.json", "w") as f:
    json.dump(snapshot, f, indent=1)

print(f"stations: {total_stations} = 2*(1+3+5) + 7 | per-half layers: {HALF_COUNTS} | equator: {EQUATOR_COUNT} shared")
