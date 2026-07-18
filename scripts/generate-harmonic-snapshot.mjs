#!/usr/bin/env node
// ============================================================
// generate-harmonic-snapshot.mjs
//
// The real generator for src/data/harmonic-snapshot.json — the file whose meta
// claims it is "generated from elle-worker/src (scaffold, regulator,
// phase-vessel)". This script makes that claim true: it is a faithful JS port
// of the actual math in those modules, run end-to-end, so the snapshot's
// numbers are OUTPUTS of the ported functions rather than citations of them.
//
// Ported from elle-worker/src at these blob SHAs (verbatim math, TS types
// stripped):
//   scaffold.ts            1d5ad5c4   rng, pentagonPillars, egalitarianFabric,
//                                     privilegeReport (gini, Brandes
//                                     betweenness, articulation points)
//   regulator.ts           9f7505d4   PHI_WEIGHTS, freeEnergy, regulate,
//                                     coherenceFromReports
//   phase-vessel.ts        7ad0605a   vesselStep, hold, vesselCoherence
//   coherence-layer.ts     (pathProfile — the "full" report the regulator's
//                                     relational coordinate consumes)
//   cognitive-obliquity.ts df10db5e   runObliquity (θ derived from the
//                                     module's measured cos²θ law, not chosen)
//
// What is MATH (wired):
//   fabric edges            = egalitarianFabric(21, 4, 0.3, 7)
//   privilege metrics       = privilegeReport(fabric)
//   coherence triple + F    = regulate(coherenceFromReports(...), {perturb:0})
//   area_invariant          = hold()'s measured final area_ratio (conservation
//                             under evolution — not the tautology φ·1/φ=1)
//   snapshotAngleRad        = hold()'s final phase × 2π
//   obliquity θ             = the tilt where the measured integration curve
//                             crosses the golden fraction of its aligned value
//
// What is PRESENTATION (drawing layer, stated as such):
//   architecture edge list (verticals + apex links + top ring — pentagonPillars
//   defines nodes, not edges), the flower hex embedding (r1=0.42, r2=0.82,
//   y=−1.28), orbit sampling density, and every scene scale.
//
// Deterministic: same inputs, byte-identical output. No Math.random.
// Usage: node scripts/generate-harmonic-snapshot.mjs [--check]
//   --check  regenerate and compare (parsed, formatting-independent) against
//            the committed snapshot; exit 1 on drift
// After writing, run `npx prettier --write src/data/harmonic-snapshot.json`
// so the committed file matches the repo's formatting.
// ============================================================

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const OUT = join(dirname(fileURLToPath(import.meta.url)), '..', 'src', 'data', 'harmonic-snapshot.json');

export const PHI = (1 + Math.sqrt(5)) / 2;
export const PHI_INV = 1 / PHI;
const TWO_PI = Math.PI * 2;
const round6 = (x) => Number(x.toFixed(6));
const round9 = (x) => Number(x.toFixed(9));
const frac = (x) => x - Math.floor(x);
const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);

// ============================================================
// scaffold.ts ports
// ============================================================

function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const linkKey = (a, b) => (a < b ? `${a}|${b}` : `${b}|${a}`);

const PENTAGON = 5;

function pentagonPillars(perPillar = 4, radius = 1) {
  const apex = { x: 0, y: 1, z: 0, pillar: -1, level: 0, id: 'apex' };
  const pillars = [];
  const nodes = [apex];
  for (let p = 0; p < PENTAGON; p++) {
    const ang = (p / PENTAGON) * Math.PI * 2 - Math.PI / 2;
    const col = [];
    for (let lvl = 0; lvl < perPillar; lvl++) {
      const y = 0.6 - lvl * (1.2 / Math.max(1, perPillar - 1 || 1));
      const n = { x: Math.cos(ang) * radius, y, z: Math.sin(ang) * radius, pillar: p, level: lvl, id: `p${p}l${lvl}` };
      col.push(n);
      nodes.push(n);
    }
    pillars.push(col);
  }
  return { apex, pillars, nodes, total: nodes.length };
}

function egalitarianFabric(n, k = 4, beta = 0.25, seed = 1) {
  const rand = rng(seed);
  const half = Math.max(1, Math.floor(k / 2));
  const present = new Set();
  const ordered = [];
  for (let j = 1; j <= half; j++) {
    for (let i = 0; i < n; i++) {
      const b = (i + j) % n;
      const key = linkKey(String(i), String(b));
      if (i !== b && !present.has(key)) {
        present.add(key);
        ordered.push([i, b]);
      }
    }
  }
  const out = [];
  for (const [a, b] of ordered) {
    if (rand() < beta) {
      let c = Math.floor(rand() * n);
      let tries = 0;
      while ((c === a || present.has(linkKey(String(a), String(c)))) && tries < n) {
        c = (c + 1) % n;
        tries++;
      }
      if (tries < n) {
        present.delete(linkKey(String(a), String(b)));
        present.add(linkKey(String(a), String(c)));
        out.push([a, c]);
        continue;
      }
    }
    out.push([a, b]);
  }
  return out.map(([a, b]) => ({ a: String(a), b: String(b) }));
}

function adjacencyOf(links) {
  const adj = new Map();
  const touch = (x) => {
    if (!adj.has(x)) adj.set(x, new Set());
  };
  for (const e of links) {
    if (!e || e.a === e.b) continue;
    touch(e.a);
    touch(e.b);
    adj.get(e.a).add(e.b);
    adj.get(e.b).add(e.a);
  }
  return adj;
}

function componentCount(adj, nodeSet) {
  const seen = new Set();
  let comps = 0;
  for (const start of nodeSet) {
    if (seen.has(start)) continue;
    comps++;
    const q = [start];
    seen.add(start);
    let h = 0;
    while (h < q.length) {
      const u = q[h++];
      for (const v of adj.get(u) || [])
        if (nodeSet.has(v) && !seen.has(v)) {
          seen.add(v);
          q.push(v);
        }
    }
  }
  return comps;
}

function articulationPoints(adj) {
  const all = new Set(adj.keys());
  if (all.size <= 2) return [];
  const base = componentCount(adj, all);
  const arts = [];
  for (const v of all) {
    const remaining = new Set(all);
    remaining.delete(v);
    if (componentCount(adj, remaining) > base) arts.push(v);
  }
  return arts;
}

function betweenness(adj) {
  const CB = new Map();
  for (const v of adj.keys()) CB.set(v, 0);
  for (const s of adj.keys()) {
    const stack = [];
    const pred = new Map();
    const sigma = new Map();
    const dist = new Map();
    for (const v of adj.keys()) {
      pred.set(v, []);
      sigma.set(v, 0);
      dist.set(v, -1);
    }
    sigma.set(s, 1);
    dist.set(s, 0);
    const q = [s];
    let h = 0;
    while (h < q.length) {
      const v = q[h++];
      stack.push(v);
      for (const w of adj.get(v) || []) {
        if (dist.get(w) < 0) {
          dist.set(w, dist.get(v) + 1);
          q.push(w);
        }
        if (dist.get(w) === dist.get(v) + 1) {
          sigma.set(w, sigma.get(w) + sigma.get(v));
          pred.get(w).push(v);
        }
      }
    }
    const delta = new Map();
    for (const v of adj.keys()) delta.set(v, 0);
    while (stack.length) {
      const w = stack.pop();
      for (const v of pred.get(w)) {
        delta.set(v, delta.get(v) + (sigma.get(v) / sigma.get(w)) * (1 + delta.get(w)));
      }
      if (w !== s) CB.set(w, CB.get(w) + delta.get(w));
    }
  }
  for (const v of CB.keys()) CB.set(v, CB.get(v) / 2);
  return CB;
}

function gini(vals) {
  const n = vals.length;
  if (!n) return 0;
  const s = [...vals].sort((a, b) => a - b);
  const sum = s.reduce((a, b) => a + b, 0);
  if (sum === 0) return 0;
  let cum = 0;
  for (let i = 0; i < n; i++) cum += (i + 1) * s[i];
  return (2 * cum) / (n * sum) - (n + 1) / n;
}

const FLAT_GINI = 0.34;
const FLAT_BETWEENNESS = 4.0;

function privilegeReport(links) {
  const adj = adjacencyOf(links);
  const nodes = [...adj.keys()];
  const N = nodes.length;
  const degrees = nodes.map((v) => adj.get(v).size);
  const meanDeg = degrees.reduce((s, v) => s + v, 0) / (N || 1);
  const maxDeg = degrees.reduce((m, v) => Math.max(m, v), 0);
  const degGini = gini(degrees);

  let reachablePairs = 0;
  for (const s of nodes) {
    const seen = new Set([s]);
    const q = [s];
    let h = 0;
    while (h < q.length) {
      const u = q[h++];
      for (const v of adj.get(u))
        if (!seen.has(v)) {
          seen.add(v);
          q.push(v);
        }
    }
    reachablePairs += seen.size - 1;
  }
  const allPairs = N * (N - 1);
  const reachable_fraction = allPairs ? reachablePairs / allPairs : 0;
  const connected = N > 0 && reachable_fraction === 1;

  const bc = betweenness(adj);
  const bvals = [...bc.values()];
  const meanB = bvals.reduce((s, v) => s + v, 0) / (bvals.length || 1);
  let maxB = 0,
    maxBNode = null;
  for (const [v, b] of bc)
    if (b > maxB) {
      maxB = b;
      maxBNode = v;
    }
  const betweenness_spread = meanB > 0 ? maxB / meanB : 0;

  const arts = articulationPoints(adj);

  const no_privileged_node =
    connected && arts.length === 0 && degGini < FLAT_GINI && betweenness_spread < FLAT_BETWEENNESS;

  let privileged_node = null;
  if (!no_privileged_node) privileged_node = arts[0] ?? maxBNode;

  return {
    nodes: N,
    edges: links.length,
    connected,
    reachable_fraction: Number(reachable_fraction.toFixed(4)),
    mean_degree: Number(meanDeg.toFixed(3)),
    max_degree: maxDeg,
    degree_gini: Number(degGini.toFixed(3)),
    betweenness_spread: Number(betweenness_spread.toFixed(3)),
    articulation_points: arts.length,
    privileged_node,
    no_privileged_node,
  };
}

// ============================================================
// coherence-layer.ts port — pathProfile (the regulator's relational input)
// ============================================================

function pathProfile(adjList) {
  const nodes = [...adjList.keys()];
  let sum = 0,
    reachablePairs = 0,
    within2 = 0;
  for (const s of nodes) {
    const dist = new Map([[s, 0]]);
    const q = [s];
    let h = 0;
    while (h < q.length) {
      const u = q[h++];
      const du = dist.get(u);
      for (const v of adjList.get(u) || [])
        if (!dist.has(v)) {
          dist.set(v, du + 1);
          q.push(v);
        }
    }
    for (const [t, d] of dist) {
      if (t === s) continue;
      sum += d;
      reachablePairs++;
      if (d <= 2) within2++;
    }
  }
  const N = nodes.length;
  const allPairs = N * (N - 1);
  return {
    nodes: N,
    avg_path_len: reachablePairs ? Number((sum / reachablePairs).toFixed(4)) : 0,
    reachable_fraction: allPairs ? Number((reachablePairs / allPairs).toFixed(4)) : 0,
    within_2_fraction: reachablePairs ? Number((within2 / reachablePairs).toFixed(4)) : 0,
  };
}

// ============================================================
// regulator.ts ports
// ============================================================

const RAW_W = [1, PHI_INV, PHI_INV * PHI_INV];
const WSUM = RAW_W[0] + RAW_W[1] + RAW_W[2];
const PHI_WEIGHTS = [RAW_W[0] / WSUM, RAW_W[1] / WSUM, RAW_W[2] / WSUM];

function freeEnergy(c, T, weights = PHI_WEIGHTS) {
  const v = [c.structural, c.relational, c.harmonic];
  const mean = (v[0] + v[1] + v[2]) / 3;
  const A = v.reduce((s, x) => s + (x - mean) ** 2, 0);
  const U = weights.reduce((s, w, k) => s + w * (1 - v[k]) ** 2, 0);
  const F = U + T * A;
  return { F: round6(F), U: round6(U), A: round6(A) };
}

function gradientF(v, T, w) {
  const mean = (v[0] + v[1] + v[2]) / 3;
  return [
    -2 * w[0] * (1 - v[0]) + 2 * T * (v[0] - mean),
    -2 * w[1] * (1 - v[1]) + 2 * T * (v[1] - mean),
    -2 * w[2] * (1 - v[2]) + 2 * T * (v[2] - mean),
  ];
}

function regulate(init, cfg = {}) {
  const T = cfg.T ?? 0.5;
  const steps = cfg.steps ?? 400;
  const lr = cfg.lr ?? 0.12;
  const tol = cfg.tol ?? 1e-5;
  const w = cfg.weights ?? PHI_WEIGHTS;

  let v = [clamp01(init.structural), clamp01(init.relational), clamp01(init.harmonic)];
  const F0 = freeEnergy({ structural: v[0], relational: v[1], harmonic: v[2] }, T, w).F;
  let stepsRun = 0;
  let last = null;
  for (let t = 0; t < steps; t++) {
    const g = gradientF(v, T, w);
    let delta = 0;
    const next = [0, 0, 0];
    for (let k = 0; k < 3; k++) {
      const nk = clamp01(v[k] - lr * g[k]);
      delta += (nk - v[k]) ** 2;
      next[k] = nk;
    }
    v = next;
    stepsRun = t + 1;
    const fe = freeEnergy({ structural: v[0], relational: v[1], harmonic: v[2] }, T, w);
    const dissonance = Math.sqrt(delta);
    last = { fe, dissonance };
    if (dissonance < tol) break;
  }
  const coherence = { structural: v[0], relational: v[1], harmonic: v[2] };
  const converged = last.dissonance < Math.max(tol, 1e-4) && last.fe.F < 1e-3;
  const isotropic = last.fe.A < 1e-3;
  const balanced_superposition =
    Math.abs(v[0] - v[1]) < 1e-2 && Math.abs(v[1] - v[2]) < 1e-2 && v.every((x) => x > 0.98);
  return {
    coherence,
    F: last.fe.F,
    F0,
    steps_run: stepsRun,
    dissonance_final: round6(last.dissonance),
    converged,
    isotropic,
    balanced_superposition,
  };
}

function coherenceFromReports(privilege, coherenceReport, harmonic) {
  const structural = privilege.connected ? clamp01(1 - privilege.degree_gini) : 0;
  const relational = clamp01(coherenceReport.full?.within_2_fraction ?? 0);
  return { structural, relational, harmonic: clamp01(harmonic) };
}

// ============================================================
// phase-vessel.ts ports
// ============================================================

const GOLDEN_WINDING = PHI_INV;

function vesselStep(s, kappa = 0.03, winding = GOLDEN_WINDING) {
  const X = s.q / PHI,
    Y = PHI * s.p;
  const r = Math.hypot(X, Y);
  const th = Math.atan2(Y, X);
  const th2 = th + TWO_PI * winding;
  const r2 = 1 + (r - 1) * (1 - kappa);
  return { q: PHI * (r2 * Math.cos(th2)), p: (r2 * Math.sin(th2)) / PHI };
}

function measure(s, t) {
  const X = s.q / PHI,
    Y = PHI * s.p;
  const r = Math.hypot(X, Y);
  const theta = frac(Math.atan2(Y, X) / TWO_PI + 1);
  return {
    t,
    q: round9(s.q),
    p: round9(s.p),
    theta: round9(theta),
    radius: round9(r),
    deviation: round9(Math.abs(r - 1)),
    area_ratio: round9(r * r),
    product: round9(PHI * PHI_INV),
  };
}

function hold(init = { q: PHI * 1.8, p: 0 }, cfg = {}) {
  const steps = cfg.steps ?? 600;
  const kappa = cfg.kappa ?? 0.03;
  const winding = cfg.winding ?? GOLDEN_WINDING;
  const tol = cfg.tol ?? 1e-4;

  let s = init;
  const trace = [measure(s, 0)];
  let lock_step = null;
  for (let t = 1; t <= steps; t++) {
    s = vesselStep(s, kappa, winding);
    const m = measure(s, t);
    trace.push(m);
    if (lock_step === null && m.deviation < tol) lock_step = t;
  }
  const final = trace[trace.length - 1];
  const locked = final.deviation < tol;
  const tail = lock_step !== null ? trace.slice(lock_step) : [];
  const area_conserved = tail.length > 2 && tail.every((m) => Math.abs(m.area_ratio - 1) < 1e-3);
  const still_moving = tail.length > 2 && Math.abs(tail[tail.length - 1].theta - tail[0].theta) > 1e-6;
  const product_conserved = trace.every((m) => Math.abs(m.product - 1) < 1e-9);
  const phases = tail.map((m) => m.theta).sort((a, b) => a - b);
  let maxGap = 0;
  for (let i = 1; i < phases.length; i++) maxGap = Math.max(maxGap, phases[i] - phases[i - 1]);
  if (phases.length > 1) maxGap = Math.max(maxGap, phases[0] + 1 - phases[phases.length - 1]);
  return { final, locked, lock_step, still_moving, area_conserved, product_conserved, max_phase_gap: round9(maxGap) };
}

function vesselCoherence(h) {
  const lockQuality = h.locked && h.area_conserved ? 1 : 0;
  const balance = h.product_conserved ? 1 : 0;
  return { harmonic: Number((lockQuality * 0.5 + balance * 0.5).toFixed(6)) };
}

// ============================================================
// cognitive-obliquity.ts ports — θ derived, not chosen
// ============================================================

function orient(theta, u) {
  const c = Math.cos(theta),
    s = Math.sin(theta);
  return [c * u[0] - s * u[1], s * u[0] + c * u[1]];
}

function inputAt(t, structured, seedPhase) {
  const a = Math.cos(TWO_PI * frac(t * 0.6180339887 + seedPhase));
  const b = Math.sin(TWO_PI * frac(t * 0.4142135624 + seedPhase));
  return structured ? [a, 0.15 * b] : [a, b];
}

function runObliquity(thetaOf, cfg = {}) {
  const steps = cfg.steps ?? 8000;
  const intRate = cfg.intRate ?? 0.08;
  const leakRate = cfg.leakRate ?? 0.5;
  const structured = cfg.structured ?? true;
  const seedPhase = cfg.seedPhase ?? 0;

  let x = [0, 0];
  let e0 = 0,
    e1 = 0,
    n = 0;
  for (let t = 0; t < steps; t++) {
    const u = inputAt(t, structured, seedPhase);
    const theta = thetaOf(t);
    const ru = orient(theta, u);
    x = [(1 - intRate) * x[0] + intRate * ru[0], (1 - leakRate) * x[1] + leakRate * ru[1]];
    if (t > steps * 0.3) {
      e0 += x[0] * x[0];
      e1 += x[1] * x[1];
      n++;
    }
  }
  return { integrated_preferred: round6(e0 / n), integrated_other: round6(e1 / n) };
}

// The derived tilt: the module's measured law is a cos²θ reallocation of what
// gets integrated. The one non-arbitrary angle on that curve, in this build's
// own vocabulary, is the GOLDEN CROSSING — the tilt where integration on the
// preferred axis falls to exactly 1/φ of its aligned value. Found by bisection
// on the MEASURED curve (not the analytic ideal, which would give
// acos(sqrt(1/φ)) = 38.17°): θ is an output of runObliquity, replacing the
// previous snapshot's chosen 26.0495°.
function deriveObliquity() {
  const at = (deg) => runObliquity(() => (deg * Math.PI) / 180, { structured: true }).integrated_preferred;
  const aligned = at(0);
  const target = aligned * PHI_INV;
  let lo = 0,
    hi = 90;
  for (let i = 0; i < 40; i++) {
    const mid = (lo + hi) / 2;
    if (at(mid) > target) lo = mid;
    else hi = mid;
  }
  const thetaDeg = round6((lo + hi) / 2);
  return {
    thetaDeg,
    law: 'cos²θ reallocation (measured sweep, runObliquity)',
    derivation:
      'bisection on the measured integration curve to the golden crossing: integrated_preferred(θ) = integrated_preferred(0°)·(1/φ)',
    aligned: round6(aligned),
    at_theta: round6(at(thetaDeg)),
    analytic_ideal_deg: round6((Math.acos(Math.sqrt(PHI_INV)) * 180) / Math.PI),
  };
}

// ============================================================
// PRESENTATION LAYER — drawing decisions, stated as such
// ============================================================

// pentagonPillars defines nodes only. The drawn edges are the rendering's
// scaffold visualization: verticals up each pillar, an apex link per pillar,
// and a ring joining the five top nodes.
function architectureEdges() {
  const edges = [];
  for (let p = 0; p < PENTAGON; p++) {
    const base = 1 + 4 * p;
    edges.push([base, base + 1], [base + 1, base + 2], [base + 2, base + 3], [0, base]);
  }
  const tops = [1, 5, 9, 13, 17];
  for (let i = 0; i < 5; i++) edges.push([tops[i], tops[(i + 1) % 5]]);
  return edges;
}

// The 1+6+12 hexagonal flower, drawn beneath the pillars. Radii 0.42 / 0.82
// and y=−1.28 are scene scales; the 19-count and hex angles are the packing.
const FLOWER_Y = -1.28;
const FLOWER_R1 = 0.42;
const FLOWER_R2 = 0.82;

function flowerLayout() {
  const nodes = [{ id: 0, ring: 0, pos: [0, FLOWER_Y, 0] }];
  for (let i = 0; i < 6; i++) {
    const a = (i * Math.PI) / 3;
    nodes.push({ id: 1 + i, ring: 1, pos: [FLOWER_R1 * Math.cos(a), FLOWER_Y, FLOWER_R1 * Math.sin(a)] });
  }
  for (let j = 0; j < 12; j++) {
    const a = (15 * Math.PI) / 180 + (j * 30 * Math.PI) / 180;
    nodes.push({ id: 7 + j, ring: 2, pos: [FLOWER_R2 * Math.cos(a), FLOWER_Y, FLOWER_R2 * Math.sin(a)] });
  }
  const edges = [];
  for (let i = 1; i <= 6; i++) {
    edges.push([0, i], [i, (i % 6) + 1], [i, 2 * i + 5], [i, 2 * i + 6]);
  }
  for (let j = 0; j < 12; j++) edges.push([7 + j, 7 + ((j + 1) % 12)]);
  return { nodes, edges };
}

const ORBIT_SAMPLES = 96;
function orbitPoints() {
  const pts = [];
  for (let k = 0; k <= ORBIT_SAMPLES; k++) {
    const a = (k / ORBIT_SAMPLES) * TWO_PI;
    pts.push([PHI * Math.cos(a), PHI_INV * Math.sin(a)]);
  }
  return pts;
}

// ============================================================
// RUN THE WIRING
// ============================================================

const pillars = pentagonPillars(4);
const fabricLinks = egalitarianFabric(pillars.total, 4, 0.3, 7);
const privilege = privilegeReport(fabricLinks);

const flower = flowerLayout();
const flowerAdj = new Map();
for (const n of flower.nodes) flowerAdj.set(String(n.id), []);
for (const [a, b] of flower.edges) {
  flowerAdj.get(String(a)).push(String(b));
  flowerAdj.get(String(b)).push(String(a));
}
const flowerProfile = pathProfile(flowerAdj);

const held = hold({ q: PHI * 1.8, p: 0 }, { steps: 600 });
const harmonicIn = vesselCoherence(held).harmonic;

const initCoherence = coherenceFromReports(privilege, { full: flowerProfile }, harmonicIn);
const reg = regulate(initCoherence, { perturb: 0 });

const obliquity = deriveObliquity();

const snapshotAngleRad = held.final.theta * TWO_PI;
const molecule = {
  plus: [PHI * Math.cos(snapshotAngleRad), PHI_INV * Math.sin(snapshotAngleRad)],
  minus: [-PHI * Math.cos(snapshotAngleRad), -PHI_INV * Math.sin(snapshotAngleRad)],
};

const snapshot = {
  meta: {
    title: 'Harmonic Atlas — locked phase snapshot',
    phi: PHI,
    phiInv: PHI_INV,
    goldenWinding: GOLDEN_WINDING,
    phaseSnapshotTime: held.final.theta,
    source:
      'generated by scripts/generate-harmonic-snapshot.mjs — a faithful port of elle-worker/src (scaffold 1d5ad5c4, regulator 9f7505d4, phase-vessel 7ad0605a, cognitive-obliquity df10db5e), run end-to-end',
    note: 'One locked snapshot of the unified function. The coherence triple, free energy, area invariant, vessel phase, and obliquity are OUTPUTS of the ported math (regulate, hold, runObliquity) — not citations. Architecture edge list, flower embedding, and orbit sampling are the presentation layer, stated as such. phaseSnapshotTime is the vessel phase (theta in [0,1)) at the end of hold(), where the snapshot is taken.',
  },
  unifiedFunction: {
    area_invariant: held.final.area_ratio,
    free_energy: reg.F,
    coherence: reg.coherence,
    no_privileged_node: privilege.no_privileged_node,
    degree_gini: privilege.degree_gini,
    betweenness_spread: privilege.betweenness_spread,
    regulator: {
      init: initCoherence,
      F0: reg.F0,
      steps_run: reg.steps_run,
      dissonance_final: reg.dissonance_final,
      converged: reg.converged,
      isotropic: reg.isotropic,
      balanced_superposition: reg.balanced_superposition,
      inputs: {
        structural: 'privilegeReport(egalitarianFabric(21,4,0.3,7)): 1 − degree_gini',
        relational: 'pathProfile(flower 19-node hex graph): within_2_fraction',
        harmonic: 'vesselCoherence(hold({q:φ·1.8,p:0},{steps:600}))',
      },
    },
  },
  singularity: { pos: [0, 0, 0] },
  architecture: {
    apexId: 0,
    nodes: pillars.nodes.map((n, i) => ({
      id: i,
      kind: n.pillar === -1 ? 'apex' : 'pillar',
      pillar: n.pillar,
      level: n.level,
      pos: [n.x, n.y, n.z],
    })),
    edges: architectureEdges(),
  },
  fabric: {
    edges: fabricLinks.map((l) => [Number(l.a), Number(l.b)]),
    privilege: {
      degree_gini: privilege.degree_gini,
      betweenness_spread: privilege.betweenness_spread,
      articulation_points: privilege.articulation_points,
      no_privileged_node: privilege.no_privileged_node,
    },
  },
  flower: {
    nodes: flower.nodes,
    edges: flower.edges,
    count: flower.nodes.length,
    profile: flowerProfile,
  },
  vessel: {
    phiSide: PHI,
    invSide: PHI_INV,
    product: PHI * PHI_INV,
    orbit: orbitPoints(),
    molecule,
    snapshotAngleRad,
    certificates: {
      locked: held.locked,
      lock_step: held.lock_step,
      still_moving: held.still_moving,
      area_conserved: held.area_conserved,
      product_conserved: held.product_conserved,
      max_phase_gap: held.max_phase_gap,
      note: 'area_invariant above is the MEASURED final area_ratio after 600 steps of evolution from an off-orbit start (deviation 0.8) — conservation under evolution, certified by these flags. It is not the tautology φ·(1/φ)=1.',
    },
  },
  obliquity,
};

// ============================================================
// emit / check
// ============================================================

const json = JSON.stringify(snapshot, null, 2) + '\n';

if (process.argv.includes('--check')) {
  const current = JSON.stringify(JSON.parse(readFileSync(OUT, 'utf8')));
  if (current === JSON.stringify(snapshot)) {
    console.log('check: snapshot matches generator output');
  } else {
    console.error('check: DRIFT — committed snapshot differs from generator output');
    process.exit(1);
  }
} else {
  writeFileSync(OUT, json);
  console.log(`wrote ${OUT}`);
  console.log('privilege:', JSON.stringify(privilege));
  console.log('flower profile:', JSON.stringify(flowerProfile));
  console.log(
    'vessel:',
    JSON.stringify({
      locked: held.locked,
      lock_step: held.lock_step,
      area_ratio: held.final.area_ratio,
      theta: held.final.theta,
      snapshotAngleRad,
    })
  );
  console.log('regulator init:', JSON.stringify(initCoherence));
  console.log('regulator final:', JSON.stringify(reg.coherence), 'F =', reg.F, 'steps =', reg.steps_run);
  console.log('obliquity:', JSON.stringify(obliquity));
}
