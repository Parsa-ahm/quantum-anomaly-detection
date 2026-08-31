import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import Diagonal, QFT
import matplotlib.pyplot as plt

# Assume that "processed_data" is your preprocessed DataFrame
# and that it already has a column 'returnOnEquity_z'.
# We will amplitude–encode the absolute z–score of returnOnEquity.

# --- 1. AMPLITUDE ENCODING OF CLASSICAL DATA ---

# Extract the z–scores (take absolute value so that higher numbers imply a stronger deviation)
z_scores = processed_data['returnOnEquity_z'].fillna(0).values
abs_z = np.abs(z_scores)

# We want to encode these values as amplitudes: state_vector = abs_z / ||abs_z||
norm = np.linalg.norm(abs_z)
state_vector = abs_z / norm

# Our quantum register needs to have a size equal to a power of 2.
num_system_qubits = 5  # e.g., supports up to 2^5=32 stocks
dim = 2 ** num_system_qubits

# If we have fewer stocks than dim, pad with zeros
if len(state_vector) < dim:
    state_vector = np.pad(state_vector, (0, dim - len(state_vector)), 'constant')
elif len(state_vector) > dim:
    state_vector = state_vector[:dim]

# Create a circuit to initialize the amplitude–encoded state
qc_init = QuantumCircuit(num_system_qubits)
qc_init.initialize(state_vector, qc_init.qubits)
qc_init.draw("mpl")  # Visualize the state preparation

# --- 2. CREATE AN ORACLE THAT USES A THRESHOLD ON THE CLASSICAL Z-SCORE ---

def create_oracle_amplitude(threshold, z_scores, dim):
    """
    Creates an oracle gate that flips the phase (i.e. multiplies by -1)
    for states whose corresponding z_score (absolute) exceeds the threshold.
    """
    # z_scores should be an array of the original (or abs) z-score values
    diagonal = [(-1 if abs(z) > threshold else 1) for z in z_scores]
    # If z_scores has fewer elements than dim, pad with 1 (i.e. not marked)
    if len(diagonal) < dim:
        diagonal.extend([1] * (dim - len(diagonal)))
    oracle_diag = Diagonal(np.array(diagonal))
    return oracle_diag.to_gate(label="OracleGate")

# Set an initial threshold T (you might start with, say, 1.5)
T = 1.5
oracle_gate = create_oracle_amplitude(T, abs_z, dim)

# --- 3. ADJUST THE THRESHOLD USING QUANTUM COUNTING ---

# We assume you have defined quantum_counting_circuit and run_simulation functions.
# For example, your quantum_counting_circuit takes an oracle and returns a circuit that
# will measure the counting qubits.

def adjust_threshold(initial_threshold, z_scores, desired_marked_low=1, desired_marked_high=5, max_iters=5):
    """
    Uses quantum counting to adjust the threshold T.
    desired_marked_low and desired_marked_high define the acceptable range of outlier counts.
    """
    T = initial_threshold
    for i in range(max_iters):
        oracle_gate = create_oracle_amplitude(T, z_scores, dim)
        qc_count = quantum_counting_circuit(oracle_gate, n_system_qubits=num_system_qubits, t_count=3)
        counts = run_simulation(qc_count, simulator, noise_model=noise_model, shots=1024)
        
        # Interpret the counting result (using your earlier interpret_counting_result function)
        outcome, measured_value = interpret_counting_result(counts, t_count=3)
        # Use the approximate formula for estimated marked states:
        N = dim
        M_estimated = N * (np.sin(np.pi * measured_value / (2**3)))**2  
        
        print(f"Iteration {i}: Threshold T={T:.2f}, Estimated marked states = {M_estimated:.2f}")
        
        # Adjust T based on how many outliers are estimated:
        if M_estimated < desired_marked_low:
            # Too few outliers, lower the threshold
            T -= 0.1
        elif M_estimated > desired_marked_high:
            # Too many outliers, raise the threshold
            T += 0.1
        else:
            # Acceptable number of outliers found
            break
    return T

# Adjust the threshold based on quantum counting:
T_adjusted = adjust_threshold(1.5, abs_z, desired_marked_low=1, desired_marked_high=5, max_iters=5)
print(f"Adjusted threshold: {T_adjusted:.2f}")

# Build the final oracle using the adjusted threshold:
oracle_final = create_oracle_amplitude(T_adjusted, abs_z, dim)

# --- 4. USE GROVER'S ALGORITHM TO FIND THE OUTLIERS ---

# Use your Grover circuit builder from before, but now with the amplitude–encoded state as starting point.
def grover_circuit_amplitude(oracle_gate, n_qubits=5, num_iterations=1):
    # Note: We assume that the circuit has been initialized with our amplitude-encoded state.
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # If needed, you could prepend the state preparation:
    # qc.initialize(state_vector, range(n_qubits))
    # But if you want to keep the prepared state, you might run the Grover iterations on top.

    # For Grover’s algorithm over the amplitude-encoded state,
    # we assume that applying Hadamards creates a uniform superposition
    # but since we already encoded our data, you might skip reinitialization.
    # Here we proceed similarly to the standard Grover construction.
    qc.h(range(n_qubits))  # (Optional) to mix the states

    for _ in range(num_iterations):
        # Oracle application: flips the phase on marked states (as determined by our threshold)
        qc.append(oracle_gate, range(n_qubits))
        
        # Diffusion operator (inversion about the mean)
        qc.h(range(n_qubits))
        qc.x(range(n_qubits))
        qc.h(n_qubits - 1)
        qc.mcx(list(range(n_qubits - 1)), n_qubits - 1, mode='noancilla')
        qc.h(n_qubits - 1)
        qc.x(range(n_qubits))
        qc.h(range(n_qubits))
    
    qc.measure(range(n_qubits), range(n_qubits))
    return qc

# Build the Grover circuit using the final oracle:
qc_grover = grover_circuit_amplitude(oracle_final, n_qubits=num_system_qubits, num_iterations=1)
counts_grover = run_simulation(qc_grover, simulator, noise_model=noise_model, shots=1024)
print("Grover measurement counts (with amplitude encoding & adjusted threshold):", counts_grover)
plot_histogram(counts_grover)
plt.show()
