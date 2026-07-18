# ============================================================
# generate-cmb-snapshot.py
#
# The CMB anchor: the one sky-pattern that really is a drawn cross-section
# decoding interior physics. Writes src/data/cmb-snapshot.json.
# Requires numpy + camb (pip install camb).
#
# THE MECHANISM (computed live, a real Boltzmann solver):
#   CAMB integrates the coupled photon-baryon-dark-matter equations of the
#   early universe for the Planck 2018 best-fit LambdaCDM parameters
#   (H0=67.36, Omega_b h^2=0.02237, Omega_c h^2=0.1200, tau=0.0544,
#   A_s=2.1e-9, n_s=0.9649 — typed literature inputs, labeled) and returns
#   the lensed TT power spectrum: the acoustic peaks of the primordial
#   plasma. The peak positions and the acoustic angular scale theta* fall
#   OUT of the physics; nothing here is fit to the observed sky.
#
# THE DATA (typed literature constants, labeled as data — the science
# archives are unreachable from this sandbox, stated):
#   Observed TT peak positions ell_1 = 220.0, ell_2 = 537.5, ell_3 = 810.8
#   (Planck 2013 XVI / 2015 XIII peak fits) and the measured acoustic scale
#   100*theta* = 1.0411 (Planck 2018 VI). The check is computed-vs-observed,
#   same discipline as the Kirkwood gap centers on the orbital page.
#
# THE ROUND TRIP (the page's proof, mirroring the hologram reconstruction):
#   1. Draw ONE Gaussian random sky from the computed spectrum (seeded) by
#      direct spherical-harmonic synthesis on a Gauss-Legendre grid — a
#      statistical sibling of our sky, NOT our sky, stated as such.
#   2. Then run it backward: recover the power spectrum FROM THE MAP ALONE
#      (harmonic analysis by exact quadrature). The recovered points land
#      on the input curve, scattered by exactly the predicted cosmic
#      variance 2/(2l+1) — the reason even a perfect instrument cannot
#      beat sample variance on one sky. The measured scatter ratio is
#      stored beside its prediction.
#   Physics -> spectrum -> sky -> spectrum again. The pattern on the
#   sphere decodes back to the physics that drew it.
#
# Deterministic (seeded synthesis). CAMB's numerics are deterministic for
# fixed inputs; version stored in meta.
# ============================================================

import json
import math

import numpy as np
import camb

# ---- Planck 2018 best-fit LambdaCDM (typed literature inputs, labeled) ----
PARAMS = {
    "H0": 67.36,
    "ombh2": 0.02237,
    "omch2": 0.1200,
    "tau": 0.0544,
    "As": 2.1e-9,
    "ns": 0.9649,
}
OBSERVED = {
    "peaks_ell": [220.0, 537.5, 810.8],  # Planck 2013 XVI / 2015 XIII peak fits
    "theta100": 1.0411,                  # 100*theta_* — Planck 2018 VI
    "T_cmb_K": 2.7255,                   # COBE/FIRAS
}

LMAX_SPEC = 1500   # spectrum stored to here
LMAX_SKY = 256     # band limit of the drawn sky
NTHETA = 300       # Gauss-Legendre nodes (exact quadrature for 2*LMAX_SKY)
NPHI = 512
SEED = 7

# ---- the mechanism: CAMB ----
pars = camb.CAMBparams()
pars.set_cosmology(H0=PARAMS["H0"], ombh2=PARAMS["ombh2"], omch2=PARAMS["omch2"], tau=PARAMS["tau"])
pars.InitPower.set_params(As=PARAMS["As"], ns=PARAMS["ns"])
pars.set_for_lmax(LMAX_SPEC + 200, lens_potential_accuracy=1)
results = camb.get_results(pars)
powers = results.get_cmb_power_spectra(pars, CMB_unit="muK")
DL = powers["total"][: LMAX_SPEC + 1, 0]  # lensed TT, D_l = l(l+1)C_l/2pi, muK^2
derived = results.get_derived_params()
theta100_computed = float(derived["thetastar"])   # 100*theta_*
rstar = float(derived["rstar"])                   # sound horizon at recombination, Mpc

ells = np.arange(LMAX_SPEC + 1)

# computed peak positions: local maxima of the smooth spectrum
peaks_computed = []
for l in range(150, 1200):
    if DL[l] > DL[l - 1] and DL[l] > DL[l + 1]:
        peaks_computed.append(int(l))
peaks_computed = peaks_computed[:3]

# ---- the drawn sky: one seeded realization from the computed spectrum ----
CL = np.zeros(LMAX_SKY + 1)
CL[2:] = DL[2 : LMAX_SKY + 1] * 2 * np.pi / (ells[2 : LMAX_SKY + 1] * (ells[2 : LMAX_SKY + 1] + 1))

x_nodes, w_nodes = np.polynomial.legendre.leggauss(NTHETA)  # x = cos(theta)
theta_nodes = np.arccos(x_nodes)

rng = np.random.default_rng(SEED)

# fully-normalized associated Legendre P~_lm(x) by stable recursion, per m
def legendre_block(m, x):
    """P~_lm(x) for l = m..LMAX_SKY, shape (LMAX_SKY+1-m, len(x))."""
    out = np.zeros((LMAX_SKY + 1 - m, len(x)))
    # P~_mm
    pmm = np.full(len(x), 1.0 / math.sqrt(4 * math.pi))
    if m > 0:
        s = np.sqrt(1 - x * x)
        for k in range(1, m + 1):
            pmm = -math.sqrt((2 * k + 1) / (2 * k)) * s * pmm
    out[0] = pmm
    if m < LMAX_SKY:
        out[1] = math.sqrt(2 * m + 3) * x * pmm
        for l in range(m + 2, LMAX_SKY + 1):
            a = math.sqrt((4 * l * l - 1) / (l * l - m * m))
            b = math.sqrt(((2 * l + 1) * (l - 1 - m) * (l - 1 + m)) / ((2 * l - 3) * (l * l - m * m)))
            out[l - m] = a * x * out[l - m - 1] - b * out[l - m - 2]
    return out

# synthesis: T(theta,phi) = sum_m [c_m(theta) cos(m phi) + s_m(theta) sin(m phi)]
# with a_l0 ~ N(0, C_l) and, for m>0, sqrt(2)-normalized real pairs ~ N(0, C_l).
c_m = np.zeros((LMAX_SKY + 1, NTHETA))
s_m = np.zeros((LMAX_SKY + 1, NTHETA))
alm_store = {}
for m in range(LMAX_SKY + 1):
    P = legendre_block(m, x_nodes)
    lvals = np.arange(m, LMAX_SKY + 1)
    sig = np.sqrt(CL[lvals])
    if m == 0:
        a = rng.standard_normal(len(lvals)) * sig
        c_m[0] = a @ P
        alm_store[0] = (a, None)
    else:
        ac = rng.standard_normal(len(lvals)) * sig
        as_ = rng.standard_normal(len(lvals)) * sig
        c_m[m] = math.sqrt(2) * (ac @ P)
        s_m[m] = math.sqrt(2) * (as_ @ P)
        alm_store[m] = (ac, as_)

phis = np.linspace(0, 2 * np.pi, NPHI, endpoint=False)
mgrid = np.arange(LMAX_SKY + 1)[:, None]
cosms = np.cos(mgrid * phis[None, :])
sinms = np.sin(mgrid * phis[None, :])
sky = c_m.T @ cosms + s_m.T @ sinms  # (NTHETA, NPHI), muK

# ---- the round trip: recover C_l from the map alone ----
# phi-transform by FFT bins, theta-integral by exact Gauss-Legendre quadrature.
F = np.fft.rfft(sky, axis=1) / NPHI  # complex, (NTHETA, NPHI/2+1)
cl_hat = np.zeros(LMAX_SKY + 1)
counts = np.zeros(LMAX_SKY + 1)
for m in range(LMAX_SKY + 1):
    P = legendre_block(m, x_nodes)
    # integral over sphere: 2pi * sum_theta w * P~ * (fourier coefficient)
    fm = F[:, m]
    re = 2 * np.pi * (P * (w_nodes * fm.real)[None, :]).sum(axis=1)
    im = 2 * np.pi * (P * (w_nodes * fm.imag)[None, :]).sum(axis=1)
    lvals = np.arange(m, LMAX_SKY + 1)
    if m == 0:
        cl_hat[lvals] += re**2
        counts[lvals] += 1
    else:
        # cos/sin coefficients carry C_l each (sqrt(2) normalization above)
        cl_hat[lvals] += 2 * (re**2 + im**2)
        counts[lvals] += 2
cl_hat[2:] = cl_hat[2:] / (2 * ells[2 : LMAX_SKY + 1] + 1)

# cosmic variance check: the scatter of the recovered spectrum around the
# input should match Var(C_l_hat/C_l - 1) = 2/(2l+1)
lchk = np.arange(10, LMAX_SKY + 1)
frac = cl_hat[lchk] / CL[lchk] - 1
measured_var_ratio = float(np.mean(frac**2 / (2 / (2 * lchk + 1))))

dl_hat = cl_hat[2:] * ells[2 : LMAX_SKY + 1] * (ells[2 : LMAX_SKY + 1] + 1) / (2 * np.pi)

# ---- quantize the sky for the renderer (equirect resample) ----
NT_TEX, NP_TEX = 200, 400
theta_tex = np.linspace(0, np.pi, NT_TEX)
row_idx = np.searchsorted(-x_nodes, -np.cos(theta_tex))  # nodes sorted by x desc? handle below
order = np.argsort(theta_nodes)
theta_sorted = theta_nodes[order]
sky_sorted = sky[order]
row_idx = np.clip(np.searchsorted(theta_sorted, theta_tex), 0, NTHETA - 1)
col_idx = np.clip((np.arange(NP_TEX) * NPHI) // NP_TEX, 0, NPHI - 1)
sky_tex = sky_sorted[row_idx][:, col_idx]
amp = float(np.percentile(np.abs(sky_tex), 99))
sky_q = np.clip((sky_tex / amp + 1) / 2, 0, 1)
sky_q8 = [[int(round(v * 255)) for v in row] for row in sky_q]

# ---- store the spectrum (every 3rd ell to keep the file sane) ----
spec = [[int(l), round(float(DL[l]), 3)] for l in range(2, LMAX_SPEC + 1, 3)]
recovered = [[int(l), round(float(dl_hat[l - 2]), 3)] for l in range(10, LMAX_SKY + 1, 4)]

snapshot = {
    "meta": {
        "title": "CMB Atlas — the sky that decodes",
        "cambVersion": camb.__version__,
        "seed": SEED,
        "lmaxSky": LMAX_SKY,
        "source": (
            "generated by scripts/generate-cmb-snapshot.py — CAMB Boltzmann solver at Planck 2018 "
            "best-fit LambdaCDM (typed literature inputs, labeled); observed peak positions and "
            "acoustic scale are typed literature data (science archives unreachable from the build "
            "sandbox, stated); the drawn sky is ONE seeded realization of the computed spectrum — "
            "a statistical sibling of our sky, not our sky"
        ),
        "note": (
            "The round trip is the proof: physics -> spectrum (CAMB) -> sky (seeded harmonic "
            "synthesis) -> spectrum again (harmonic analysis of the map alone). The recovered "
            "points land on the input curve scattered by exactly the predicted cosmic variance "
            "2/(2l+1); the measured-to-predicted scatter ratio is stored. Peak positions and "
            "theta* are computed-vs-observed, the same discipline as the Kirkwood gap centers."
        ),
    },
    "params": PARAMS,
    "observed": OBSERVED,
    "computed": {
        "peaks_ell": peaks_computed,
        "theta100": round(theta100_computed, 5),
        "soundHorizonMpc": round(rstar, 2),
    },
    "cosmicVariance": {
        "measuredOverPredicted": round(measured_var_ratio, 3),
        "predictedLaw": "Var(C_l_hat/C_l - 1) = 2/(2l+1)",
    },
    "spectrum": {"ellDl": spec, "unit": "muK^2", "kind": "lensed TT, D_l"},
    "recoveredFromSky": {"ellDl": recovered, "note": "harmonic analysis of the drawn map alone"},
    "sky": {"nTheta": NT_TEX, "nPhi": NP_TEX, "amplitudeMuK": round(amp, 2), "map": sky_q8},
}

with open("src/data/cmb-snapshot.json", "w") as f:
    json.dump(snapshot, f, separators=(",", ":"))
    f.write("\n")

print(f"peaks computed: {peaks_computed} vs observed {OBSERVED['peaks_ell']}")
print(f"100*theta*: computed {theta100_computed:.5f} vs observed {OBSERVED['theta100']}")
print(f"sound horizon r*: {rstar:.2f} Mpc")
print(f"cosmic-variance scatter, measured/predicted: {measured_var_ratio:.3f} (expect ~1)")
print(f"sky map: {NT_TEX}x{NP_TEX}, amplitude scale {amp:.1f} muK")
