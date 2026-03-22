# qiskit_origin.py
# Only the primitive bifurcation law — run with python vdm_pure_law_qiskit.py

from qiskit import QuantumCircuit, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, entropy
import numpy as np

class VDM_PureLaw:
    def __init__(self):
        self.qr = QuantumRegister(1, 'inv')
        self.qc = QuantumCircuit(self.qr)
        self.qc.h(0)                    # unresolved superposition (CF000 origin)
        self.sim = AerSimulator()
        self.history = []

    def saturation_check(self):
        state = Statevector.from_instruction(self.qc)
        rho = state.to_density_matrix()
        S = entropy(rho)
        max_S = np.log2(self.qc.num_qubits)
        return S > max_S - 0.01          # saturated while borne

    def compute_emergent_half_turn(self):
        if self.qc.num_qubits < 2:
            return 0.0
        # Dynamic angle derived from current burden (entropy proxy)
        burden_proxy = entropy(Statevector.from_instruction(self.qc).to_density_matrix())
        dtheta = burden_proxy / (self.qc.num_qubits + 1)
        theta = 0.0
        test_qc = self.qc.copy()
        while theta < 100:
            test_qc.ry(dtheta, 0)        # lawful continuation
            state = Statevector.from_instruction(test_qc)
            fidelity_opposite = abs(state.data[0])**2  # |<0|ψ>|² near opposite
            theta += dtheta
            if fidelity_opposite >= 0.999:
                break
            dtheta = burden_proxy / (self.qc.num_qubits + 1)
        return theta

    def step(self):
        if self.saturation_check():
            # Universal Trigger Law
            new_qr = QuantumRegister(1, f'axis_{self.qc.num_qubits}')
            self.qc.add_register(new_qr)
            self.qc.cx(0, self.qc.num_qubits - 1)  # orthogonal burden inheritance
            print(f">>> SATURATION + VOID DEBT → NEW ORTHOGONAL QUBIT | qubits = {self.qc.num_qubits}")
        
        else:
            # Same-class continuation
            burden_proxy = entropy(Statevector.from_instruction(self.qc).to_density_matrix())
            self.qc.ry(burden_proxy / (self.qc.num_qubits + 1), 0)

        # Record
        S = entropy(Statevector.from_instruction(self.qc).to_density_matrix())
        self.history.append((self.qc.num_qubits, S))
        return self.qc.num_qubits

sim = VDM_PureLaw()
for step in range(200):
    qubits = sim.step()
    pi_em = sim.compute_emergent_half_turn()
    if step % 20 == 0 or qubits > 5:
        print(f"Step {step:3d} | qubits={qubits} | entropy={sim.history[-1][1]:.4f} | emergent_π≈{pi_em:.8f}")

print("\nVDM demo quantum run complete")
