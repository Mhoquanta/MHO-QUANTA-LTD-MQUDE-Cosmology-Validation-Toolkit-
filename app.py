# app.py
# MHO QUANTA LTD — MQUDE vs GR Comparator for 3I/ATLAS
# © 2025 MHO QUANTA LTD – All Rights Reserved

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="MQUDE vs GR — 3I/ATLAS", layout="wide")

st.title("🪐 MQUDE vs GR Comparator — 3I/ATLAS")
st.markdown("""
Compare orbital trajectories using:
- **GR** (General Relativity only)
- **GR + NG** (non-gravitational comet jets)
- **GR + MQUDE** (quantum resonance correction)
""")

uploaded = st.file_uploader("📂 Upload your Horizons CSV", type=["csv"])
alpha = st.number_input("Quantum coupling (α)", value=2e-9, format="%.1e")
lambda_km = st.number_input("Coherence length λ (km)", value=1e6, format="%.1e")

if uploaded:
    data = pd.read_csv(uploaded)
    st.success(f"Loaded {len(data)} records from {uploaded.name}")

    # --- Calculate drift (simple proxy) ---
    data["R_km"] = np.sqrt(data["X_km"]**2 + data["Y_km"]**2 + data["Z_km"]**2)
    data["GR_drift"] = data["R_km"] - data["R_km"].iloc[0]
    data["MQUDE_drift"] = data["GR_drift"] * (1 + alpha * np.exp(-data["R_km"]/lambda_km))

    # --- Plot drift ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["datetime_iso"], y=data["GR_drift"],
                             name="GR Drift", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=data["datetime_iso"], y=data["MQUDE_drift"],
                             name="MQUDE Drift", line=dict(color="red")))
    fig.update_layout(title="Orbital Drift Comparison", xaxis_title="Date", yaxis_title="ΔR (km)")
    st.plotly_chart(fig, use_container_width=True)

    # --- Summary stats ---
    st.subheader("Summary")
    st.write(f"Mean MQUDE drift amplification: {data['MQUDE_drift'].iloc[-1]/data['GR_drift'].iloc[-1]:.6f}×")
    st.dataframe(data.head())
# --- MQUDE vs GR: Fig.4 Divergence (meters) ---
import io
import numpy as np
import matplotlib.pyplot as plt

st.subheader("Fig. 4 — MQUDE – GR divergence (meters)")

# Try to find a DataFrame from your upload step; adapt variable names if needed
# Replace `df` below with your app's actual dataframe variable if different
try:
    df_plot = df.copy()
except NameError:
    df_plot = None

if df_plot is None:
    st.info("Upload CSV first to enable the divergence plot.")
else:
    # Be robust to different column sets
    # We need a timestamp column and two drift columns (km) to compute residual in meters.
    # Your exports typically have: datetime_iso, GR_drift, MQUDE_drift
    if "datetime_iso" not in df_plot.columns:
        st.error("CSV needs a 'datetime_iso' column.")
    else:
        # Ensure datetime & sorting
        df_plot["t"] = pd.to_datetime(df_plot["datetime_iso"])
        df_plot = df_plot.sort_values("t")

        # If the app did not output GR/MQUDE drift columns (e.g., α=0 baseline),
        # create them as zeros to keep the plot logic working.
        if "GR_drift" not in df_plot.columns:
            df_plot["GR_drift"] = 0.0
        if "MQUDE_drift" not in df_plot.columns:
            df_plot["MQUDE_drift"] = 0.0

        # Residual (meters)
        df_plot["residual_m"] = (df_plot["MQUDE_drift"] - df_plot["GR_drift"]) * 1000.0

        # Time in days from first sample
        t0 = df_plot["t"].iloc[0]
        days = (df_plot["t"] - t0).dt.total_seconds() / 86400.0
        y = df_plot["residual_m"].values

        # Linear trend fit y ≈ slope * days + intercept
        if len(df_plot) >= 2 and np.isfinite(y).all():
            slope, intercept = np.polyfit(days, y, 1)
            trend = slope * days + intercept
        else:
            slope, intercept = 0.0, float(y[0] if len(y) else 0.0)
            trend = np.full_like(days, intercept)

        # Project to 2026-03-01 just for a headline number
        proj_target = pd.to_datetime("2026-03-01")
        proj_days = (proj_target - t0).total_seconds() / 86400.0
        proj_m = slope * proj_days + intercept
        proj_km = proj_m / 1000.0

        # Plot
        fig, ax = plt.subplots(figsize=(10, 4.5), dpi=150)
        ax.plot(df_plot["t"], y, "o-", linewidth=2.0, label="Residual (MQUDE − GR)")
        ax.plot(df_plot["t"], trend, "--", linewidth=2.0, label=f"Trend ≈ {slope:.2f} m/day")
        ax.set_title("MQUDE − GR residual (meters)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Residual (m)")
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend()

        st.pyplot(fig, clear_figure=True)

        # Also provide a download button for the PNG
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        st.download_button(
            "Download Fig. 4 (PNG)",
            data=buf,
            file_name="fig4_phaseII_divergence.png",
            mime="image/png"
        )

        # Show the headline projection number
        st.caption(f"Projected residual by 2026-03-01 ≈ **{proj_km:,.2f} km** (from linear trend).")
else:
    st.info("Upload your `atlas_template.csv` to begin.")
