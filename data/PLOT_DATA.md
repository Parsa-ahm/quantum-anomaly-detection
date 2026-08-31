# Plot Data

Exact numbers behind every figure in the paper, pulled from the notebook
outputs. Machine-readable version: [`figure_data.json`](./figure_data.json).

Setup: 20 tech stocks, 5 system qubits (32 basis states), 1024 shots,
`AerSimulator` with `depolarizing_error(0.01)` on H and X gates. Classical
outlier threshold = 2.0; quantum-adjusted threshold = 2.25.

---

## Figure 1.1 / 1.3 — Grover measurement counts per stock & metric

Higher count = more strongly flagged as an outlier for that metric. Sorted by total.

| Ticker | PE | ROE | Dividend | Total |
|--------|----:|----:|---------:|------:|
| AAPL | 20 | 231 | 28 | 279 |
| HPQ | 6 | 21 | 248 | 275 |
| AMD | 216 | 19 | 28 | 263 |
| AVGO | 218 | 22 | 22 | 262 |
| NVDA | 11 | 224 | 22 | 257 |
| SAP | 216 | 13 | 25 | 254 |
| QCOM | 19 | 17 | 38 | 74 |
| ORCL | 15 | 23 | 29 | 67 |
| GOOG | 15 | 19 | 25 | 59 |
| AMZN | 13 | 19 | 25 | 57 |
| ADP | 10 | 21 | 24 | 55 |
| CSCO | 10 | 21 | 24 | 55 |
| ACN | 16 | 17 | 22 | 55 |
| IBM | 7 | 17 | 29 | 53 |
| ADBE | 17 | 17 | 19 | 53 |
| CRM | 9 | 17 | 26 | 52 |
| MSFT | 12 | 14 | 23 | 49 |
| DELL | 13 | 12 | 23 | 48 |
| TXN | 7 | 20 | 20 | 47 |
| INTC | 7 | 13 | 25 | 45 |

The six clear peaks (AMD/AVGO/SAP on PE, AAPL/NVDA on ROE, HPQ on dividend)
are exactly the classically flagged outliers — Grover amplified their amplitudes.

---

## Figure 1.2 — Classical z-scores vs. quantum-adjusted threshold

Red line in the paper = quantum-adjusted threshold **2.25**. Bars = z-scores.
Full per-metric z-scores are in `figure_data.json`; the outlier-crossing values:

**returnOnEquity (ROE) z-scores**

| Ticker | z | Outlier (\|z\|>2) |
|--------|----:|:--:|
| AAPL | +2.4916 | yes |
| NVDA | +2.0474 | yes |
| ORCL | +1.6521 | |
| ADP | +1.1393 | |
| INTC | -1.4629 | |

**trailingPE outliers:** AMD +2.4398, SAP +2.1846, AVGO +2.0587
**dividendYield outlier:** HPQ +2.3111

Classical outlier flags @ threshold 2.0 (6 total): PE → AMD, SAP, AVGO · ROE →
AAPL, NVDA · Dividend → HPQ. Composite-flagged stocks: AAPL, NVDA, HPQ, AMD, AVGO, SAP.

---

## Quantum counting histograms (3 counting qubits, per oracle)

Raw measurement counts over the 3-qubit counting register (1024 shots):

| Outcome | PE | ROE | Dividend |
|---------|---:|----:|---------:|
| 000 | 33 | 30 | 60 |
| 001 | 20 | 23 | 17 |
| 010 | 25 | 37 | 34 |
| 011 | 410 | 356 | 198 |
| 100 | 56 | 216 | 462 |
| 101 | 440 | 301 | 186 |
| 110 | 22 | 40 | 46 |
| 111 | 18 | 21 | 21 |

Estimated marked states, `M = 32·sin²(π·v/8)`:

| Oracle | Peak outcome | Estimated marked / 32 |
|--------|:---:|:---:|
| trailingPE | 101 | 27.31 |
| returnOnEquity | 011 | 16.00 |
| dividendYield | 100 | 4.69 |

---

## Dynamic threshold adjustment (full-quantum experiment)

Quantum counting drives the threshold until 1–6 states stay marked:

| Iteration | Threshold | Estimated marked |
|:---:|:---:|:---:|
| 0 | 1.50 | 16.00 |
| 1 | 1.75 | 27.31 |
| 2 | 2.00 | 27.31 |
| 3 | 2.25 | 4.69 |
| 4 | 2.25 | 4.69 |

Converged threshold: **2.25**.

---

## Composite amplitude experiment — top measurement counts

Amplitude-encoded ROE run; measured 5-qubit states → stock index:

| State | Index | Count | Stock |
|-------|:---:|---:|:---:|
| 00000 | 0 | 279 | AAPL |
| 01101 | 13 | 275 | HPQ |
| 10000 | 16 | 263 | AMD |
| 10001 | 17 | 262 | AVGO |
| 00111 | 7 | 257 | NVDA |
| 10010 | 18 | 254 | SAP |
| 01100 | 12 | 74 | QCOM |
