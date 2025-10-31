# SIE Stability Analysis

**Originally validated: April 2, 2025**<br>
**Author: Justin K. Lietz**<br>
***Neuroca, Inc***

*Note: These frameworks represent the foundational validation work. Subsequent private testing has led to substantial improvements and additional discoveries including self-organization and self-repair mechanisms, unified integration of SNNs with SIE and Knowledge Graph TDA findings, and the development of Resonance Enhanced Valence Gated Synaptic Plasticity (REVGSP).*

## What This Does

Validates that the Self-Improvement Engine (SIE) can integrate multiple reward signals (TD error, novelty, habituation, self-benefit) without causing unstable learning or weight explosion.

## Quick Start

**From project root:**
```bash
python main.py --sie
```

**Direct run:**
```bash
cd Implementation
python simulate_sie_stability.py
```

**With custom parameters:**
```bash
python simulate_sie_stability.py --eta 0.01 --lambda_decay 0.001 --scaling_target 10.0
```

## Discovery

**Optimal Parameters**: λ=0.001, scaling_target=10.0 achieves stable multi-objective learning without weight explosion.

## Parameters You Can Adjust

- `--eta`: Learning rate (default: 0.01)
- `--lambda_decay`: Weight decay coefficient (default: 0.001) 
- `--scaling_target`: Synaptic scaling target (default: 10.0)
- `--num_neurons`: Network size (default: 100)

## Understanding Results

### Good Results Look Like:
- **Weight Norm**: Stable around 14-15 (not growing forever)
- **Total Reward**: Steady oscillations around 0.9 ± 0.1
- **Modulation Factor**: Stable around 0.42 ± 0.05
- **V(state)**: Smooth convergence to ~0.10

### Warning Signs:
- **Unbounded Growth**: Weight norm keeps increasing (λ too low)
- **Weight Collapse**: Weights approaching zero (λ too high)
- **High Variance**: Reward signals jumping around wildly
- **Non-convergence**: V(state) never stabilizes

## Mathematical Framework

The main stability equation:
```
mod_factor = 2σ(R_total) - 1
ΔW ∝ η · (1 + mod_factor) · R_total · E - λW
```

Where multiple reward components are combined into R_total.

## Performance

- **Speed**: ~6.6 seconds for 10,000 simulation steps
- **Convergence**: Stable results within 2,000-3,000 steps
- **Scalability**: Handles networks up to 1000+ neurons

## Output Files

## Possible Use Cases

This stable multi-objective learning framework could substantially improve:

### **Autonomous Vehicle Safety**
- **Adaptive cruise control** that balances speed, safety, comfort, and efficiency objectives
- **Emergency response systems** that maintain stability while learning from new scenarios
- **Fleet coordination** with stable multi-agent reward integration

### **Medical AI Systems**
- **Treatment recommendation engines** balancing efficacy, side effects, cost, and patient preferences
- **Surgical robotics** with stable learning from multiple feedback sources
- **Drug discovery optimization** across multiple competing pharmaceutical objectives

### **Financial Trading Systems**
- **Portfolio optimization** balancing returns, risk, liquidity, and ESG factors simultaneously
- **Algorithmic trading** that adapts to market changes without becoming unstable
- **Risk management systems** with stable multi-criteria decision making

### **Robotics & Manufacturing**
- **Industrial robot control** optimizing speed, precision, energy efficiency, and safety
- **Quality control systems** that learn from multiple inspection criteria
- **Supply chain optimization** balancing cost, speed, sustainability, and reliability

### **Smart Grid & Energy**
- **Power grid management** balancing load, renewable integration, cost, and stability
- **Battery management systems** optimizing charge time, lifespan, safety, and efficiency
- **Smart building controls** managing comfort, energy use, air quality, and cost

## Output Files

Results saved to `results/`:
- `sie_stability_simulation.png` - Weight dynamics visualization
- `parameter_sweep_results.txt` - Quantitative analysis
- Raw simulation data files for analysis

## Scientific Impact

First stable validation of multi-objective reward integration in spiking neural networks, proving that complex reward signals can be balanced without causing instability.

## Dependencies

```bash
pip install numpy matplotlib
```


## License

This research is protected under a proprietary license. **Use requires written permission from Justin K. Lietz.** See [`../LICENSE`](../LICENSE) for full terms.