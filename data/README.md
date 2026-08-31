# Data & Figures

Extracted numbers and assets for writing up the project (blog / web charts).

| File | What |
|------|------|
| [`figure_data.json`](./figure_data.json) | Machine-readable: raw metrics, z-scores, Grover counts, counting histograms, threshold iterations. Use this to build web charts. |
| [`PLOT_DATA.md`](./PLOT_DATA.md) | Same numbers as readable tables, mapped to each paper figure. |
| [`GATES_AND_CIRCUITS.md`](./GATES_AND_CIRCUITS.md) | Oracle / Grover / quantum-counting gate details + noise model. |
| [`original_figures/`](./original_figures/) | The original matplotlib PNGs from the notebooks (reference for redesigns). |

All numbers come from the stored notebook outputs; z-scores recomputed from
`../tech_stock_data.csv` and verified to match the notebook's outlier flags.
