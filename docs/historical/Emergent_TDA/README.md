# Knowledge Graph Topological Data Analysis

**Originally validated: April 2, 2025**<br>
**Author: Justin K. Lietz**<br>
***Neuroca, Inc***

*Note: These frameworks represent the foundational validation work. Subsequent private testing has led to substantial improvements and additional discoveries including self-organization and self-repair mechanisms, unified integration of SNNs with SIE and Knowledge Graph TDA findings, and the development of Resonance Enhanced Valence Gated Synaptic Plasticity (REVGSP).*

## What This Does

Analyzes neural network "shape" to discover mathematical relationships about network health. Uses topology (the study of shape) to predict when networks will work well or break down.

## Quick Start

**From main project:**
```bash
python main.py --kgtda
```

**Direct run:**
```bash
cd Implementation
python run_analysis.py
```

## Discoveries

### Finding 1: Complexity-Efficiency Trade-off
```
Correlation: r = -0.85, p = 0.002
```
**Meaning**: More complex network shapes → lower efficiency<br>
**Impact**: There's an optimal complexity level for peak performance

### Finding 2: Fragmentation-Pathology Relationship  
```
Correlation: r = 0.997, p < 1e-9
```
**Meaning**: Broken/fragmented networks → high dysfunction<br>
**Impact**: Network connectivity directly predicts health

## Understanding Results

### Healthy Network Indicators:
- **Components**: 1 (fully connected)
- **B1 Persistence**: 50-70 (moderate complexity)
- **Efficiency**: >0.85 (good performance)
- **Pathology**: <0.15 (low dysfunction)

### Warning Signs:
- **Fragmentation**: >5 components (network breakdown)
- **Over-complexity**: B1 persistence >200 (too complex)
- **High pathology**: >0.4 (serious dysfunction)

## Example Results

| Network Type | Components | B1 Persistence | Efficiency | Pathology | Status |
|--------------|------------|----------------|------------|-----------|---------|
| Healthy      | 1          | 56             | 0.886      | 0.100     | ✅ Good |
| Efficient    | 2          | 0              | 0.900      | 0.100     | ✅ Good |
| Complex      | 1          | 230            | 0.835      | 0.100     | ⚠️ Slow |
| Fragmented   | 16         | 0              | 0.900      | 0.800     | ❌ Broken |

## Performance

- **Speed**: ~0.07 seconds per 100-node network
- **Scales**: Up to 500+ node networks efficiently
- **Accuracy**: High statistical significance (p < 0.003)

## Output Files

Results saved to `results/`:
- `tda_analysis_results.txt` - Complete analysis with correlations
- Individual snapshot analysis files
- Network visualization plots

## Possible Use Cases

This topology analysis framework could substantially improve:

### **AI Safety & System Health**
- **Neural network monitoring** for large language models and AI systems
- **Early warning detection** for model degradation before failure
- **Quality assurance** for AI systems in critical applications

### **Brain & Medical Research**
- **Neurological disorder detection** through brain connectivity analysis
- **Treatment monitoring** via network topology changes over time
- **Neural implant optimization** using topology-guided design principles

### **Social Network Analysis**
- **Community health assessment** in online platforms and social networks
- **Information flow optimization** in organizational communication networks
- **Network resilience evaluation** for distributed systems

### **Infrastructure Monitoring**
- **Power grid stability assessment** using topological health metrics
- **Communication network optimization** through connectivity analysis
- **Supply chain resilience** evaluation via fragmentation detection

### **Scientific Research**
- **Protein interaction networks** in drug discovery and biology
- **Ecosystem stability analysis** through species interaction patterns
- **Materials science** for optimizing molecular network structures

## Dependencies

```bash
pip install numpy scipy networkx ripser matplotlib
```

## Scientific Impact

Provides the first quantitative framework for predicting neural network health from topology, enabling real-time monitoring and design optimization.


## License

This research is protected under a proprietary license. **Use requires written permission from Justin K. Lietz.** See [`../LICENSE`](../LICENSE) for full terms.