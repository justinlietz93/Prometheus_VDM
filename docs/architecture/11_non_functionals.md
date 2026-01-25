# Non-Functional Requirements Assessment

**Repository**: Prometheus_VDM  
**Commit**: ae49a391acf2183242e4d96bda49e066beec7680

---

## PERFORMANCE

### Computational Complexity
| Operation | Complexity | Evidence | Optimality |
|-----------|------------|----------|------------|
| Core step | **O(E)** | Sparse adjacency traversal | ✅ Optimal for sparse graphs |
| KNN initialization | **O(N log N)** | scipy.spatial.cKDTree | ✅ Optimal |
| Metrics computation | **O(N + E)** | NetworkX graph stats | ✅ Acceptable |
| Checkpoint save (h5) | **O(N + E)** | HDF5 compression | ✅ Acceptable |
| Checkpoint load (h5) | **O(N + E)** | HDF5 decompression | ✅ Acceptable |
| ZEMA (streaming) | **O(1)** per tick | Rolling window | ✅ Optimal |

### Benchmarks (Extrapolated from Code)
| Scale | N | E (k=12) | Step Time | Memory | Notes |
|-------|---|----------|-----------|--------|-------|
| **Toy** | 100 | 1,200 | <1ms | <10MB | Unit tests |
| **Small** | 1,000 | 12,000 | ~10ms | ~50MB | Default |
| **Medium** | 10,000 | 120,000 | ~100ms | ~500MB | Acceptable |
| **Large** | 100,000 | 1,200,000 | ~1-2s | ~5GB | Tested (sparse mode auto-enables at 20k+) |
| **Huge** | 1,000,000 | 12M | ~10-20s | ~50GB | Untested (theoretical) |

**Auto-Optimization**: Sparse mode auto-enables at N ≥ 20,000 (see `run_nexus.py:68`)

### Vectorization & Parallelism
- **NumPy**: Heavy use of vectorized operations (activation updates, field diffusion)
- **SciPy Sparse**: CSR format for O(E) edge traversal
- **GPU Acceleration**: Optional PyTorch for substrate ops (CUDA/ROCm)
  - Not enabled by default (requires manual torch install)
  - Code paths: `core/substrate/neurogenesis.py`, `core/substrate/substrate.py`
- **CPU Parallelism**: None (single-threaded main loop)
  - **Gap**: No multiprocessing or threading for scout parallelization
  - **Opportunity**: Parallelize void walkers (embarrassingly parallel)

### Memory Efficiency
- **Sparse Representation**: SciPy CSR for adjacency (efficient for k << N)
- **In-Place Updates**: Most operations modify arrays in-place (minimal allocation)
- **Checkpoint Compression**: HDF5 with gzip (factor ~3-5x)
- **Gap**: No memory pooling or custom allocators

### Performance Risks
| Risk | Severity | Impact | Mitigation |
|------|----------|--------|------------|
| **Python GIL bottleneck** | M | Limits CPU scaling | Rewrite hot path in Cython/Numba |
| **No GPU default** | M | Underutilizes HPC | Auto-detect GPU; fallback to CPU |
| **Single-threaded** | M | Wastes multi-core | Parallelize scouts (joblib/Ray) |
| **No profiling hooks** | M | Blind optimization | Add cProfile, line_profiler, nvprof wrappers |

### Recommendations
1. **Add benchmarks**: Automated benchmarks in CI (pytest-benchmark)
2. **Profile hot path**: Add `@profile` decorators; run with `kernprof`
3. **Parallelize scouts**: Use `joblib.Parallel` for void walker execution
4. **GPU by default**: Auto-detect CUDA/ROCm; enable substrate acceleration
5. **Memory profiling**: Add `memory_profiler` to detect leaks

**Performance Score**: **3/5** (Efficient sparse ops; lacks profiling and parallelism)

---

## SCALABILITY

### Horizontal Scaling
- **Current**: Single-process, single-machine
- **Limitation**: No distributed support (MPI, Ray, Dask)
- **Gap**: Cannot scale beyond single GPU or multi-core CPU

### Vertical Scaling
- **Tested**: Up to N=100k (sparse mode)
- **Theoretical**: Up to N=1M (memory-bound at ~50GB)
- **GPU**: Substrate ops support torch.cuda (tested on consumer GPUs)

### Data Scaling
- **Checkpoint Size**: O(E) for weights; ~1-10MB per 10k edges (compressed h5)
- **Telemetry Growth**: O(T) where T=ticks; ~1KB/tick → 1GB/million ticks
- **Retention**: Checkpoint pruning (keep N=5 by default)

### Scaling Bottlenecks
| Bottleneck | Current Limit | Scaling Approach |
|------------|---------------|------------------|
| **Memory** | ~50GB (N=1M) | Sharding, out-of-core (Dask arrays) |
| **Compute** | Single GPU | Multi-GPU (PyTorch DDP), MPI |
| **I/O** | Sequential h5py | Parallel HDF5 (MPI-IO) |
| **Telemetry** | Single JSONL | Distributed logging (OpenTelemetry) |

### Recommendations
1. **Shard connectome**: Distribute across nodes (graph partitioning)
2. **Multi-GPU**: PyTorch DistributedDataParallel for substrate
3. **Streaming telemetry**: Replace JSONL with Kafka/Pulsar for high-throughput
4. **Out-of-core**: Use Dask arrays for N > 10M

**Scalability Score**: **4/5** (Tested to 100k; clear path to 1M+; lacks distributed support)

---

## RELIABILITY

### Fault Tolerance
- **Checkpointing**: Periodic saves (every N ticks) enable recovery
- **Resume**: `--load-engram` restores from checkpoint (tested)
- **Gaps**:
  - No automatic retry on checkpoint write failure
  - No crash recovery (requires manual `--load-engram`)
  - No idempotency guarantees (re-running with same seed ≠ identical if checkpoint mid-run)

### Error Handling
- **Missing**: No structured error handling in hot path (core step, checkpoint I/O)
- **Fail-Fast**: Exceptions propagate to top-level (good for debugging, bad for resilience)
- **Validation**: Minimal input validation (config, engram format)

### Determinism & Reproducibility
- **Seed Support**: ✅ All RNG seeded (numpy.random.seed, random.seed)
- **Checkpoint Provenance**: ✅ Metadata includes seed, step, domain
- **Gaps**:
  - No deterministic seeding for optional GPU ops (torch.manual_seed not enforced)
  - No verification that same seed → identical trajectory (no golden run tests)

### Resilience Patterns
| Pattern | Implemented? | Gap |
|---------|--------------|-----|
| **Circuit Breaker** | ❌ | No retry logic for transient failures (I/O, GPU OOM) |
| **Bulkhead** | ❌ | Failure in one scout can crash entire step |
| **Retry** | ❌ | No exponential backoff for checkpoint writes |
| **Graceful Degradation** | ✅ (partial) | GPU optional; Redis optional |
| **Health Checks** | ✅ | HTTP status endpoint (`runtime/helpers/status_http.py`) |

### Recommendations
1. **Add retry logic**: Exponential backoff for checkpoint I/O, Redis pub
2. **Validate inputs**: JSON schema for run profiles; engram format checks
3. **Golden runs**: Add pytest tests for determinism (same seed → same output)
4. **Crash recovery**: Auto-resume from latest checkpoint on restart
5. **Circuit breakers**: Isolate scout failures; continue with degraded walkers

**Reliability Score**: **2/5** (Checkpointing works; lacks retry, validation, resilience patterns)

---

## SECURITY

### Threat Model
- **Users**: Researchers, developers (trusted)
- **Deployment**: Local workstation, HPC cluster (controlled environment)
- **Exposure**: HTTP dashboard (127.0.0.1:8060), optional Redis (localhost:6379)
- **Sensitivity**: Research data (low); potential IP in derivations (medium)

### Vulnerabilities

#### Critical
| Vuln | Severity | Evidence | Impact |
|------|----------|----------|--------|
| **Secrets in .env** | **H** | `.env` and `.env.local` committed | Credential leakage (GitHub public repo) |

#### High
| Vuln | Severity | Evidence | Impact |
|------|----------|----------|--------|
| **No secret scanning** | H | No gitleaks/truffleHog in CI | Ongoing leakage risk |
| **Redis no auth** | M | Default Redis config (no password) | Local privilege escalation |

#### Medium
| Vuln | Severity | Evidence | Impact |
|------|----------|----------|--------|
| **Path traversal** | M | File picker in frontend (unvalidated paths) | Arbitrary file read |
| **JSONL injection** | M | User text → JSONL without escaping | Log forging |
| **Dependency vulns** | M | 74 unpinned packages | Supply chain attack |

### Mitigation Actions
1. **Immediate**:
   - Remove .env from git history (`git filter-repo`)
   - Add `.env*` to `.gitignore`
   - Rotate all keys in .env (if any)
   - Add gitleaks to CI
2. **Short-term**:
   - Add Redis authentication (requirepass)
   - Validate file picker paths (sandboxing)
   - Escape user text before JSONL logging
   - Run `pip-audit` and fix high-severity CVEs
3. **Long-term**:
   - Adopt secrets manager (AWS Secrets Manager, HashiCorp Vault)
   - Add security scanning (Bandit, Snyk)

**Security Score**: **2/5** (Critical secret leakage; local deployment mitigates network exposure)

---

## PRIVACY

### Data Collection
- **User Text**: Captured in `inbox.jsonl` → `events.jsonl`
- **Telemetry**: Metrics, events, macros → JSONL
- **Checkpoints**: Full connectome state (weights, bias)

### PII Risks
- **Low**: Research setting; no production user data
- **Gap**: No anonymization if user text contains PII

### Compliance (Hypothetical)
| Regulation | Applicable? | Status |
|------------|-------------|--------|
| **GDPR** | No (research) | N/A |
| **HIPAA** | No (no health data) | N/A |
| **Export Control** | Possible (dual-use AI) | ⚠️ Review LICENSE.md |

### Recommendations
1. **Data minimization**: Don't log raw user text; hash or anonymize
2. **Retention policy**: Auto-delete runs after N days (configurable)
3. **Export control review**: Clarify dual-license terms (academic vs commercial)

**Privacy Score**: **4/5** (Low PII risk; research context; minor logging improvements needed)

---

## MAINTAINABILITY

### Code Readability
- **Strengths**: Clear module names, layering, zero cycles
- **Gaps**: Missing docstrings (~40% coverage), magic numbers

### Evolvability
- **Plugin System**: ✅ frontend/plugins/ for visualizations
- **Feature Flags**: ✅ Environment variables (FORCE_DENSE, ENABLE_EVENT_METRICS, etc.)
- **Versioning**: ⚠️ No semantic versioning; CHANGELOG exists but not tied to releases

### Technical Debt
- **Debt Ratio**: ~6 weeks to address P0-P1 items (see `10_quality_gates.md`)
- **Hotspots**: nexus.py, core_engine.py, sparse_connectome.py

### Recommendations
1. **Add docstrings**: pydocstyle in CI; >80% coverage
2. **Semantic versioning**: Tag releases (v0.1.0, v0.2.0)
3. **Deprecation policy**: Mark deprecated APIs; 2-release sunset

**Maintainability Score**: **3/5** (Good structure; lacks documentation and versioning)

---

## OPERABILITY

See `12_operability.md` for detailed analysis.

**Summary**: Strong JSONL telemetry; weak observability (no tracing, correlation IDs).

**Operability Score**: **3/5**

---

## OVERALL NON-FUNCTIONAL SCORE

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Performance | 3/5 | 20% | 0.6 |
| Scalability | 4/5 | 15% | 0.6 |
| Reliability | 2/5 | 20% | 0.4 |
| Security | 2/5 | 15% | 0.3 |
| Privacy | 4/5 | 5% | 0.2 |
| Maintainability | 3/5 | 10% | 0.3 |
| Operability | 3/5 | 15% | 0.45 |

**Total**: **2.85/5** (C+; requires hardening for production)

---

## CRITICAL PATH TO PRODUCTION

1. **Security**: Fix secret leakage, add scanning
2. **Reliability**: Add retry logic, input validation, golden runs
3. **Observability**: Correlation IDs, distributed tracing
4. **Performance**: Profiling hooks, benchmarks
5. **Testing**: Expand coverage to >50%
