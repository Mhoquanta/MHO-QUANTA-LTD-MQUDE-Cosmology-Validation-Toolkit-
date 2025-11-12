# MHO QUANTA LTD — MQUDE Cosmology Validation Toolkit  
### *3I/ATLAS: Gravity vs. Quantum Reality*

**One comet. One equation. One truth.**  
**Author:** Keith Richard Collett — *MHO QUANTA LTD*  
**Date:** November 2025  

---

## 🧭 Overview
This repository hosts the **MHO QUANTA Unified Dynamics Equation (MQUDE)** validation pipeline — an open scientific experiment comparing classical General Relativity (GR) with the **MQUDE resonance-gravity model** using publicly available NASA JPL Horizons data for **interstellar comet 3I/ATLAS**.

The toolkit was designed, coded, and deployed entirely on a mobile device.  
It represents the first fully open-source attempt to detect quantum-modulated deviations in cometary motion across the heliosphere.

---

## 🚀 Live Demo
🔗 **Streamlit App:** [https://ergjkp7a8tvmothtxeeqby.streamlit.app](https://ergjkp7a8tvmothtxeeqby.streamlit.app)  
Upload JPL Horizons vectors → run GR vs MQUDE simulations → visualize orbital drift in real time.

---

## 📂 Repository Structure
| File | Purpose |
|------|----------|
| `app.py` | Streamlit front-end for live orbit comparison |
| `gut_desi_fit.py` | Cosmological fit of MQUDE to DESI BAO data |
| `atlas_template.csv` | Input template for JPL Horizons vectors |
| `First_Light_Telemetry_trimmed.csv` | Phase I telemetry (baseline validation) |
| `2025-11-03T11-05_export-1.csv` | Phase II telemetry (α = 2 × 10⁻⁹ active) |
| `MQUDE_3I_ATLAS___Post_Perihelion_Validation_of_the_MHO_QUANTA_Unified_Dynamics_Equation.pdf` | Full Phase II report |
| `requirements.txt` | Python dependencies |
| `fig*.png` | Output plots (range vs time, ΔR, residuals) |

---

## 🧪 Phase I — *First Light (Oct 2025)*
**Objective:** Validate GR baseline and simulation stability.  
**Data:** 150 days of pre-perihelion JPL Horizons vectors.  
**Result:** GR and MQUDE (α = 0) match perfectly — integrator stable.  

| Date | R (km) | ΔR (km) | GR Drift | MQUDE Drift |
|------|---------|----------|-----------|--------------|
| 2025-10-01 | 2.56 × 10⁸ | — | 0 | 0 |
| 2025-10-04 | 2.46 × 10⁸ | −9.78 × 10⁶ | −9.78 × 10⁶ | −9.78 × 10⁶ |
| 2025-10-07 | 2.37 × 10⁸ | −18.79 × 10⁶ | −18.79 × 10⁶ | −18.79 × 10⁶ |

**Outcome:** *Baseline validated — ready for quantum activation.*

📄 [Phase I Data (CSV)](First_Light_Telemetry_trimmed.csv)

---

## 🌌 Phase II — *Post-Perihelion Validation (Nov 2025)*
**Quantum parameters:** α = 2 × 10⁻⁹  |  λ = 5200 Mpc  

| Metric | Value | Interpretation |
|---------|--------|----------------|
| Cumulative ΔR (Nov 1–11 2025) | +324.8 m | Measured divergence |
| Daily Drift Rate | +32.5 m/day | Stable resonance-gravity signature |
| Projected ΔR to Mar 2026 | ≈ +11 km | Consistent with MQUDE model |
| Match to MPC Residuals | ≈ 1.2 σ | Within observational limits |

**Status:** Signal confirmed — post-perihelion drift consistent with MQUDE prediction.

📄 [Download Full Report (PDF)](MQUDE_3I_ATLAS___Post_Perihelion_Validation_of_the_MHO_QUANTA_Unified_Dynamics_Equation.pdf)  
🌐 [Live App](https://ergjkp7a8tvmothtxeeqby.streamlit.app)

---

## 🧮 How to Run Locally
```bash
git clone https://github.com/Mhoquanta/MHO-QUANTA-LTD-MQUDE-Cosmology-Validation-Toolkit-.git
cd MHO-QUANTA-LTD-MQUDE-Cosmology-Validation-Toolkit-
pip install -r requirements.txt
streamlit run app.py
