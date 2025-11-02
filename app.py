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

else:
    st.info("Upload your `atlas_template.csv` to begin.")
