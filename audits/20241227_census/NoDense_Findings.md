# Dense-Scan Regression Audit

## Summary
Found 10 operations that imply global or near-global passes, with varying severity levels. Most concerning are the weight matrix operations and full-N iterations in hot paths.

## High Severity (Hot Path Concerns)

### 1. Global Weight Statistics
**File**: `fum_rt/core/metrics.py:24`
```python
"avg_weight": float(connectome.W.mean()),
```
**Issue**: Computes mean over entire weight matrix without masking
**Impact**: O(|E|) or O(N²) operation in metrics hot path

### 2. Dense Adjacency Neighbor List Construction  
**File**: `fum_rt/core/void_b1.py:262`
```python
nbrs = [np.where(A[i] > 0)[0].astype(np.int32) for i in range(N)]
```
**Issue**: Scans entire adjacency matrix to build neighbor lists
**Impact**: O(N²) dense scan, defeats sparse data structure benefits

### 3. GPU-CPU Weight Transfer
**File**: `fum_rt/core/substrate/neurogenesis.py:53`
```python 
W_cpu = substrate.W.cpu().numpy()
```
**Issue**: Full weight matrix transfer from GPU memory to CPU
**Impact**: Expensive memory transfer, blocks GPU pipeline

## Medium Severity (Maintenance/Analysis Paths)

### 4. Degree Vector Operations
**File**: `fum_rt/core/metrics.py:41,47`
```python
total = deg.sum()
return float(-(p * np.log(p)).sum())
```
**Issue**: Global sums over degree/probability vectors
**Impact**: O(N) operations, acceptable for analysis but could accumulate

### 5. Component Analysis Iterations
**File**: `fum_rt/core/sparse_connectome.py:292,294`
```python
neigh_sets: List[Set[int]] = [set() for _ in range(N)]
for i in range(N):
```
**Issue**: Full-N iterations for connectivity analysis
**Impact**: O(N) initialization + iteration, used in component tracking

### 6. Active Vertex Counting  
**File**: `fum_rt/core/void_b1.py:215`
```python
V_active = int((deg > 0).sum())
```
**Issue**: Sum over degree vector to count active vertices
**Impact**: O(N) but necessary for B1 calculations

## Low Severity (Initialization/Fallback)

### 7. Sparse Connectome Initialization
**File**: `fum_rt/core/sparse_connectome.py:61`
```python
self.adj: List[np.ndarray] = [np.zeros(0, dtype=np.int32) for _ in range(self.N)]
```
**Issue**: Creates N empty arrays during initialization
**Impact**: One-time O(N) cost, acceptable for setup

### 8. Walker Fallback Seeds
**File**: `fum_rt/core/cortex/void_walkers/void_cycle_scout.py:99,101`
```python
tuple(range(N))
```
**Issue**: Creates full node range when no priority seeds available  
**Impact**: Fallback behavior, used with budget constraints

## Hot Path Analysis

**High Risk** - Operations that could occur in main simulation loop:
- `connectome.W.mean()` - Called during metrics collection
- `nbrs = [np.where(A[i] > 0)[0]...` - B1 calculation hot path
- `W.cpu().numpy()` - GPU-CPU transfer during neurogenesis

**Medium Risk** - Maintenance/analysis operations:
- Component connectivity analysis
- Degree-based statistics
- Territory boundary calculations

**Low Risk** - Initialization and rare fallbacks:
- Data structure setup
- Walker seed fallbacks with budgets

## Recommendations

1. **Immediate**: Replace `W.mean()` with sampled statistics or EWMA
2. **Short-term**: Cache neighbor lists, avoid rebuilding from dense adjacency  
3. **Long-term**: Implement sparse-native B1 calculation avoiding `np.where(A[i] > 0)`

## Void-Faithful Violations

The most serious violations of "no dense scans" are:
1. Global weight statistics without sampling bounds
2. Dense adjacency matrix scanning for sparse neighbor extraction
3. Full GPU weight matrix transfers

These break the void-faithful contract of local, bounded operations.