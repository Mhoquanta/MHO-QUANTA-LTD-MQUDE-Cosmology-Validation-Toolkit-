# 🌠 MQUDE vs GR: Is 3I/ATLAS Being Pushed by *Something Else*?

**One equation. One comet. One phone.**

> **Live orbital comparator** — General Relativity vs. cometary jets vs. **MQUDE resonance gravity**  
> Built by a **solo citizen scientist** using **public NASA/ESA data**

[![Run on Streamlit](https://img.shields.io/badge/Streamlit-Live_Demo-red)](https://your-app.streamlit.app)  
[![arXiv](https://img.shields.io/badge/arXiv-Coming_Soon-blue)](#)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 The Question
Is **interstellar comet 3I/ATLAS** following **pure gravity**...  
or is something **nudging it off course**?

- **GR**: Perfect prediction (if no outgassing)  
- **GR + Jets**: Sudden kicks at perihelion  
- **GR + MQUDE**: Slow, persistent drift from **resonance-modified spacetime**

We built a tool to **find out — in real time**.

---

## ⚙️ What This Repo Does

| Tool | Input | Output |
|------|-------|--------|
| `gut_desi_fit.py` | DESI BAO/H(z) | Fits **MQUDE** to cosmology **without dark energy** |
| `atlas_template.csv` | NASA JPL Horizons | Daily state vectors (Oct 2025 – Mar 2026) |
| `compare_orbits.py` *(coming)* | Your model | **O-C residuals** vs. IAWN/MPC |

---

## 🎯 Run the DESI Fit (2 minutes)

```bash
pip install numpy pandas matplotlib scipy

python gut_desi_fit.py
