# app.py — MQUDE vs GR: 3I/ATLAS Comparator (Full Edition)
# MHO QUANTA LTD — Streamlit Cloud ready

import io
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

APP_TITLE = "MQUDE vs GR — 3I/ATLAS Comparator"
VERSION = "v2.4 (Full)"

REQUIRED_COLS = [
    "datetime_iso","X_km","Y_km","Z_km","VX_kms","VY_kms","VZ_kms"
]

st.set_page_config(page_title=APP_TITLE, layout="centered")
st.title(APP_TITLE)
st.caption(f"MHO QUANTA LTD · {VERSION}")

with st.expander("What is this?"):
    st.write(
        "- Upload **JPL/Horizons** CSV (columns: datetime_iso, X_km, Y_km, Z_km, VX_kms, VY_kms, VZ_kms).  \n"
        "- Compare **GR** (baseline) vs **MQUDE** (α, λ).  \n"
        "- See **drift** and **residuals**.  \n"
        "- **Download** trimmed telemetry for sharing."
    )

# ──────────────────────────────────────────────────────────────────────────────
# Sidebar controls
# ──────────────────────────────────────────────────────────────────────────────
st.sidebar.header("Model Parameters")

alpha = st.sidebar.number_input(
    "Quantum coupling α", value=2.0e-9, min_value=0.0, format="%.1e",
    help="Set 0 for GR baseline; small positive values for MQUDE test."
)

lambda_km = st.sidebar.number_input(
    "Coherence length λ (km)", value=1.0e6, min_value=1e3, format="%.1e",
    help="Range over which the correction is effective."
)

show_table = st.sidebar.checkbox("Show data table", value=False)
st.sidebar.markdown("---")
st.sidebar.caption("Need a template?")
# Provide a small, ready-to-download template (10 rows)
template_rows = [
    "datetime_iso,X_km,Y_km,Z_km,VX_kms,VY_kms,VZ_kms",
    "2025-10-01 00:00:00.000,3421139.8668286013,1354419.9695172834,-255898992.33784828,-2.0708481904196095e-05,2.8548109355298405e-05,2.4540833942082774e-05",
    "2025-10-04 01:57:33.061,-5081661.352220916,13074361.301597778,-245749113.01943314,-2.070715741386488e-05,2.853747840302759e-05,2.490454408172686e-05",
    "2025-10-07 03:55:06.122,-13581152.402668461,24785908.401712798,-235444229.32009172,-2.0691849851839773e-05,2.8506508663153103e-05,2.529574626707643e-05",
    "2025-10-10 05:52:39.184,-22070949.306155324,36479812.00679882,-224973300.6493124,-2.0659392980706485e-05,2.8450779662123705e-05,2.5712994516589328e-05",
    "2025-10-13 07:50:12.245,-30543338.14665217,48144973.52429203,-214326202.18719986,-2.0606512267887115e-05,2.8365757761581253e-05,2.615321574315984e-05",
    "2025-10-16 09:47:45.306,-38989284.07269969,59768475.3817828,-203494458.4381252,-2.053010310855694e-05,2.8247194888427837e-05,2.6611409716489285e-05",
    "2025-10-19 11:45:18.367,-47398575.54601918,71335803.90781464,-192472068.9237357,-2.0427608009850637e-05,2.8091662407369793e-05,2.708051951267217e-05",
    "2025-10-22 13:42:51.429,-55760137.58055701,82831309.96675645,-181256332.27596858,-2.0297452307068422e-05,2.789716049153402e-05,2.7551586737403107e-05",
    "2025-10-25 15:40:24.490,-64062522.46958438,94238916.03671598,-169848533.1418409,-2.0139456099248526e-05,2.766368521839259e-05,2.801427232101381e-05",
]
st.sidebar.download_button(
    "Download atlas_template.csv",
    data=("\n".join(template_rows)).encode("utf-8"),
    file_name="atlas_template.csv",
    mime="text/csv"
)

# ──────────────────────────────────────────────────────────────────────────────
# File upload
# ──────────────────────────────────────────────────────────────────────────────
uploaded = st.file_uploader("📁 Upload your `atlas_template.csv`", type=["csv"])

def _ensure_cols(df: pd.DataFrame):
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

def compute(df: pd.DataFrame, alpha: float, lambda_km: float) -> pd.DataFrame:
    """Compute heliocentric range and GR/MQUDE drifts."""
    out = df.copy()

    # Parse time
    out["datetime_iso"] = pd.to_datetime(out["datetime_iso"])

    # Range from origin
    out["R_km"] = np.sqrt(out["X_km"]**2 + out["Y_km"]**2 + out["Z_km"]**2)

    # GR drift = change in R relative to first epoch
    R0 = float(out["R_km"].iloc[0])
    out["GR_drift_km"] = out["R_km"] - R0

    # Simple MQUDE correction: scale GR drift by (1 + α e^{-R/λ})
    # α = 0 → identical to GR (validates baseline)
    corr = 1.0 + alpha * np.exp(-out["R_km"] / lambda_km)
    out["MQUDE_drift_km"] = out["GR_drift_km"] * corr

    # Convenience (meters)
    out["GR_drift_m"] = out["GR_drift_km"] * 1000.0
    out["MQUDE_drift_m"] = out["MQUDE_drift_km"] * 1000.0

    # Residual (difference)
    out["Residual_km"] = out["MQUDE_drift_km"] - out["GR_drift_km"]

    return out

def make_plot_drift(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["datetime_iso"], y=df["GR_drift_km"],
        name="GR Drift", mode="lines+markers"
    ))
    fig.add_trace(go.Scatter(
        x=df["datetime_iso"], y=df["MQUDE_drift_km"],
        name="MQUDE Drift", mode="lines+markers"
    ))
    fig.update_layout(
        title="Orbital Drift Comparison (ΔR from first epoch)",
        xaxis_title="Time (UTC)", yaxis_title="ΔR (km)", hovermode="x unified"
    )
    return fig

def make_plot_range(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["datetime_iso"], y=df["R_km"],
        name="Range R", mode="lines+markers"
    ))
    fig.update_layout(
        title="Heliocentric Range vs Time",
        xaxis_title="Time (UTC)", yaxis_title="R (km)", hovermode="x unified"
    )
    return fig

def make_plot_residual(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["datetime_iso"], y=df["Residual_km"],
        name="Residual (MQUDE − GR)", mode="lines+markers"
    ))
    fig.update_layout(
        title="Residual Drift (MQUDE − GR)",
        xaxis_title="Time (UTC)", yaxis_title="Residual (km)", hovermode="x unified"
    )
    return fig

if uploaded is None:
    st.info("Upload your `atlas_template.csv` to begin.")
else:
    try:
        raw = pd.read_csv(uploaded)
        _ensure_cols(raw)
        st.success(f"Loaded {len(raw)} records from file.")

        data = compute(raw, alpha=alpha, lambda_km=lambda_km)

        # Plots (tabs)
        tab1, tab2, tab3 = st.tabs(["Drift", "Range", "Residual"])
        with tab1:
            st.plotly_chart(make_plot_drift(data), use_container_width=True)
        with tab2:
            st.plotly_chart(make_plot_range(data), use_container_width=True)
        with tab3:
            st.plotly_chart(make_plot_residual(data), use_container_width=True)

        # Summary
        st.subheader("Summary")
        final = int(len(data) - 1)
        st.write(
            f"- Points: **{len(data)}**  \n"
            f"- Final GR drift: **{data['GR_drift_km'].iloc[final]:,.3f} km**  \n"
            f"- Final MQUDE drift: **{data['MQUDE_drift_km'].iloc[final]:,.3f} km**  \n"
            f"- Final Residual (MQUDE−GR): **{data['Residual_km'].iloc[final]*1000:,.1f} m**"
        )

        if show_table:
            st.dataframe(
                data[["datetime_iso","R_km","GR_drift_km","MQUDE_drift_km","Residual_km"]],
                use_container_width=True
            )

        # Download trimmed telemetry
        trimmed = data[[
            "datetime_iso","X_km","Y_km","Z_km",
            "VX_kms","VY_kms","VZ_kms",
            "R_km","GR_drift_km","MQUDE_drift_km","Residual_km"
        ]].copy()
        trimmed["alpha"] = alpha
        trimmed["lambda_km"] = lambda_km

        csv_bytes = trimmed.to_csv(index=False).encode("utf-8")
        fname = f"{datetime.utcnow().strftime('%Y-%m-%dT%H-%M')}_export.csv"
        st.download_button(
            "⬇️ Download telemetry CSV",
            data=csv_bytes,
            file_name=fname,
            mime="text/csv"
        )

        st.caption("Tip: upload this CSV to your GitHub repo and link it in the README.")

    except Exception as e:
        st.error(f"Could not process file: {e}")
        st.exception(e)
