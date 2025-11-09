# make_fig4.py
# MHO QUANTA LTD — Phase II Divergence Plot Generator
# Generates fig4_phaseII_divergence.png (dark mode, trendline, projection)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

CSV_PATH = "2025-11-03T11-05_export-1.csv"  # change if needed
FIG_PATH = "fig4_phaseII_divergence.png"

df = pd.read_csv(CSV_PATH)
df["t"] = pd.to_datetime(df["datetime_iso"])
df = df.sort_values("t")

df["residual_m"] = (df["MQUDE_drift"] - df["GR_drift"]) * 1000.0  # km→m

t0 = df["t"].iloc[0]
days = (df["t"] - t0).dt.total_seconds() / 86400.0
y = df["residual_m"].values

coef = np.polyfit(days, y, 1)
slope, intercept = coef
trend = slope * days + intercept

proj_dt = pd.to_datetime("2026-03-01")
proj_days = (proj_dt - t0).total_seconds() / 86400.0
proj_m = slope * proj_days + intercept
proj_km = proj_m / 1000.0

plt.figure(figsize=(10, 5), dpi=160)
ax = plt.gca()
ax.set_facecolor("#0f1116")
plt.grid(color="#223", linestyle="--", linewidth=0.6, alpha=0.7)
plt.plot(df["t"], df["residual_m"], "o-", linewidth=2.0, label="Residual (MQUDE − GR)")
plt.plot(df["t"], trend, "--", linewidth=2.0, label=f"Trend ≈ {slope:.2f} m/day")
plt.title("MQUDE – GR Residual (α = 2.1×10⁻⁹)", color="white")
plt.xlabel("Date", color="white")
plt.ylabel("Residual (m)", color="white")
ax.tick_params(colors="white")
for s in ax.spines.values():
    s.set_color("#445")
plt.annotate(f"Projected residual by 2026-03-01 ≈ {proj_km:,.1f} km",
             xy=(df['t'].iloc[-1], trend[-1]), xytext=(20,20),
             textcoords="offset points", color="#ddd",
             bbox=dict(boxstyle="round,pad=0.3", fc="#1b1f2a", ec="#445", alpha=0.9))
plt.legend(facecolor="#1b1f2a", edgecolor="#445", labelcolor="#ddd")
plt.tight_layout()
plt.savefig(FIG_PATH, bbox_inches="tight")
print(f"Saved {FIG_PATH}")
if __name__ == "__main__":
    print("Running Phase II plot generation…")
    exec(open("make_fig4.py").read())
