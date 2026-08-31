# Gates & Circuits

Reference for the quantum building blocks, for writing up the method / drawing
circuit diagrams on the blog. Code lives in the notebooks.

## Register layout

- **5 system qubits** → 2^5 = 32 basis states. Each stock maps to one basis
  state (20 stocks, remaining 12 states padded).
- Quantum counting adds **3 counting qubits** (t_count = 3), so the counting
  circuit uses 8 qubits total.
- All runs: 1024 shots on `qiskit_aer.AerSimulator`, circuits `transpile`d first.

## Noise model (NISQ)

```python
error = depolarizing_error(0.01, 1)          # 1% single-qubit depolarizing
noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(error, ['h', 'x'])
```

Applied to every H and X gate. This is what makes the amplified peaks fall short
of 100% confidence and what drives the noise-vs-confidence discussion.

## Oracle — Qiskit `Diagonal` gate

The oracle is a diagonal unitary that phase-flips (×-1) the basis states
corresponding to outliers, leaving all others untouched:

```python
diagonal = [(-1 if val > threshold else 1) for val in z_values]   # +1 normal, -1 outlier
Diagonal(np.array(diagonal)).to_gate(label="OracleGate")
```

Diagonal-matrix construction avoids building deep multi-controlled logic — key
for keeping circuit depth low under NISQ noise. Two encodings are used:

- **Experiment 1 (binary indicators):** `threshold` applied to classical z-scores;
  one oracle each for PE, ROE, dividend yield.
- **Experiment 2 (amplitude encoding):** the actual |z| values are amplitude-
  encoded and the threshold is tuned inside the quantum loop.

## Grover operator (oracle + diffusion)

```python
grover.append(oracle_gate, range(n))         # phase flip on marked states
grover.h(range(n)); grover.x(range(n))       # diffusion (inversion about mean)
grover.h(n-1)
grover.mcx(list(range(n-1)), n-1, mode='noancilla')
grover.h(n-1)
grover.x(range(n)); grover.h(range(n))
```

Grover circuit: H^n initialization → 1 iteration (oracle + diffusion) → measure.
`num_iterations = 1`, aligned with quantum counting's estimate of the optimal
iteration count for a small number of marked states.

## Quantum counting

Phase-estimation on the Grover operator to estimate how many states are marked:

```python
qc.h(counting_qubits); qc.h(system_qubits)
for i in range(t_count):                     # controlled-Grover^(2^i)
    for _ in range(2**i):
        qc.append(grover_gate.control(1), [counting_qubits[i]] + system_qubits)
qc.append(QFT(t_count, do_swaps=True).inverse(), counting_qubits)
qc.measure(counting_qubits, range(t_count))
```

Estimate from the peak counting outcome `v`:

```
M = N · sin²(π · v / 2^t_count) = 32 · sin²(π · v / 8)
```

Used both to set Grover's iteration count and, in experiment 2, to auto-tune the
outlier threshold (keep 1–6 marked states → converges to T = 2.25).

## Pipeline summary

1. Pull 20 tech stocks via `yfinance`; take trailing P/E, ROE, dividend yield.
2. z-score each metric (fill missing with median); threshold → binary outlier flags.
3. Build a `Diagonal` oracle per metric marking the flagged states.
4. Quantum counting → estimate marked count → set Grover iterations.
5. Run Grover per metric under NISQ noise; combine measurement counts into a
   composite anomaly score per stock.
