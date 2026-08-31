# Grover's Algorithm for Financial Anomaly Detection

Course research project (CPS840, Quantum Computing). A hybrid quantum-classical
framework that uses **Grover's algorithm** to detect statistical outliers across
20 technology stocks, combining classical z-score preprocessing with quantum
search in Qiskit.

**Paper:** [Financial_Anomaly_Detection_with_Quantum_computers.pdf](./Financial_Anomaly_Detection_with_Quantum_computers.pdf)
— *Using Grover's Algorithm to Find Anomalies and Outliers in Financial Markets
with Classical Preprocessing.*

## Approach

- Pull historical data for 20 S&P500 tech stocks via `yfinance`.
- Compute z-scores for three metrics: trailing P/E, return on equity (ROE), and
  dividend yield; threshold them into binary outlier indicators.
- Encode indicators into 5-qubit basis states and mark outliers with a custom
  Qiskit **Diagonal gate** oracle (phase flip on marked states).
- Build a Grover circuit per metric, run on `AerSimulator` with NISQ noise
  models, and combine measurement counts into a composite anomaly score.
- A second experiment encodes z-scores directly into amplitudes and uses quantum
  counting to set the threshold inside the quantum circuit.

## Files

| File | Description |
|------|-------------|
| `Classical_And_Quantum.ipynb` | Classical preprocessing + first quantum experiment; generates the CSV |
| `Full_Quantum.ipynb` | Amplitude-encoded experiment with quantum counting |
| `Full_QuantumV1.ipynb` | Earlier version of the full-quantum notebook |
| `newCode.py` | Standalone script version of the pipeline |
| `tech_stock_data.csv` | Preprocessed metrics produced by the classical notebook |

## Running

Built for Google Colab. Install dependencies (`qiskit`, `qiskit-aer`, `yfinance`,
`pandas`, `numpy`, `matplotlib`), then run `Classical_And_Quantum.ipynb` first
(it produces `tech_stock_data.csv`) followed by `Full_Quantum.ipynb`.

## Author

Parsa Ahmadizadeh
