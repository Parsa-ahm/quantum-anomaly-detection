# Grover's Algorithm for Financial Anomaly Detection

Course research project (CPS840, Quantum Computing). A hybrid quantum-classical
framework that uses Grover's algorithm to detect statistical outliers across 20
S&P 500 technology stocks, combining classical z-score preprocessing with
quantum search in Qiskit.

**Paper:** [Financial_Anomaly_Detection_with_Quantum_computers.pdf](./Financial_Anomaly_Detection_with_Quantum_computers.pdf),
*Using Grover's Algorithm to Find Anomalies and Outliers in Financial Markets
with Classical Preprocessing.*

**Code:** [`grovers_anomaly_detection.ipynb`](./grovers_anomaly_detection.ipynb),
one notebook covering both experiments end to end, executed and with outputs
committed.

## Method

1. Load the committed Yahoo Finance snapshot of 20 tech stocks (trailing P/E,
   return on equity, dividend yield).
2. Z-score each metric, impute missing values with the metric median, and
   threshold at `|z| > 2.0` to get binary outlier indicators.
3. Map each stock to one of the 32 basis states of a 5-qubit register and mark
   the outliers with a Qiskit `Diagonal` phase-flip oracle.
4. Run one Grover iteration per metric on `AerSimulator` under a 1%
   single-qubit depolarizing noise model, and fold the measurement counts back
   onto stocks.
5. Estimate the number of marked states by quantum counting (phase estimation
   on the Grover operator, 3 counting qubits).

Two experiments:

| | Experiment 1 | Experiment 2 |
|---|---|---|
| Encoding | binary indicators in basis states | \|z\| amplitude-encoded |
| Threshold | fixed classically at 2.0 | tuned in-loop by quantum counting |
| Noise | 1% depolarizing on H and X | noiseless, to isolate the feedback loop |

## Results

- Grover amplifies exactly the six states the classical z-score benchmark
  flags: AMD, AVGO and SAP on P/E, AAPL and NVDA on ROE, HPQ on dividend yield.
- The quantum-counting feedback loop converges to a threshold of `|z| > 2.25`,
  where Grover isolates AAPL as the single most anomalous stock on ROE.
- Amplification is partial. Under depolarizing noise the marked peaks reach
  roughly a fifth of the shots rather than dominating, and confidence falls as
  circuit depth and iteration count rise.
- With 3 counting qubits the estimator resolves only `M` in
  `{0, 4.69, 16, 27.31, 32}` and cannot distinguish `M` from `N - M`, so the
  counts are useful for driving the threshold search but not as exact counts.

## Layout

| Path | Description |
|------|-------------|
| `grovers_anomaly_detection.ipynb` | The full pipeline: preprocessing, oracles, Grover, quantum counting, both experiments |
| `tech_stock_data.csv` | Yahoo Finance snapshot the paper was written against |
| `figures/` | Figures written by the notebook (SVG) |
| `requirements.txt` | Pinned environment |

## Running

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/jupyter lab grovers_anomaly_detection.ipynb
```

The notebook runs offline against the committed CSV and is seeded, so it
reproduces the numbers above. Set `REFRESH_DATA = True` in the data cell to
re-pull live fundamentals from Yahoo Finance, which changes every result
downstream.

## Author

Parsa Ahmadizadeh
