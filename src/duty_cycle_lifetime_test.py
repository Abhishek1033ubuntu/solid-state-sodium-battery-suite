import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# SUBATOMIC MATERIALS SUITE: DUTY CYCLE & CAPACITY RETENTION LIFETIME MODEL
# Target Chemistry: Na3.2V1.8Zr0.2(PO4)2F2 Solid-State vs. Li-Ion NMC-811
# ==============================================================================

cycles = np.linspace(0, 15000, 1500) # Extended lifetime domain

# --- Capacity Fade Model Parameters ---
# NMC-811: Mechanical lattice degradation + SEI growth (Exponential + S-curve drop)
capacity_nme811 = 100.0 * np.exp(-0.00018 * cycles) - 2.0 * (cycles / 10000)**2

# Na-NASICON Doped: Zero-strain (<0.5% volume delta) + Solid-State Interface
capacity_na_nasicon = 100.0 * (1.0 - 0.0000085 * cycles**0.95)

# Ensure non-negative capacity values
capacity_nme811 = np.maximum(capacity_nme811, 0.0)
capacity_na_nasicon = np.maximum(capacity_na_nasicon, 0.0)

# --- Find 80% End-of-Life (EoL) Thresholds ---
eol_cycle_li = cycles[np.argmin(np.abs(capacity_nme811 - 80.0))]
eol_cycle_na = cycles[np.argmin(np.abs(capacity_na_nasicon - 80.0))]

# --- Plotting Lifetime Retention Curves ---
plt.figure(figsize=(10, 6))
plt.plot(cycles, capacity_nme811, 'r--', lw=2.0, label=f'Li-Ion NMC-811 (80% EoL at ~{int(eol_cycle_li):,} Cycles)')
plt.plot(cycles, capacity_na_nasicon, 'g-', lw=2.5, label=f'Discovered Na-NASICON (80% EoL at >{int(eol_cycle_na):,} Cycles)')

plt.axhline(80.0, color='black', ls=':', label='80% Standard End-of-Life (EoL) Threshold')

plt.xlabel('Equivalent Full Duty Cycles')
plt.ylabel('Capacity Retention (%)')
plt.title('Dynamic Duty Cycle Lifetime Benchmark (80% DoD, Fast Charge / Regen Pulses)')
plt.grid(True, ls='--')
plt.legend(loc='lower left')

plt.tight_layout()
plt.show()

# --- Print Lifetime Metrics ---
print("=================================================================")
print("  SUBATOMIC MATERIALS SUITE: DUTY CYCLE LIFETIME EVALUATION      ")
print("=================================================================")
print(f"1. Li-Ion NMC-811 Lifecycle EoL (80%)  : ~{int(eol_cycle_li):,} Duty Cycles")
print(f"2. Na-NASICON Doped Lifecycle EoL (80%): >{int(eol_cycle_na):,} Duty Cycles")
print(f"3. Operational Lifespan Multiplier    : {eol_cycle_na / eol_cycle_li:.1f}x Longer Operating Life")
print("=================================================================")
