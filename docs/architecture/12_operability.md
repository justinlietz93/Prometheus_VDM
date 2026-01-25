# Operability & Observability Assessment

**Repository**: Prometheus_VDM  
**Commit**: ae49a391acf2183242e4d96bda49e066beec7680

---

## LOGGING

### Current Implementation

| Aspect | Implementation | Assessment |
|--------|----------------|------------|
| **Format** | JSONL (newline-delimited JSON) | ✅ Machine-readable, tail-friendly |
| **Destination** | Filesystem (`runs/{timestamp}/events.jsonl`) | ✅ Persistent, simple |
| **Centralization** | `utils/logging_setup.get_logger()` | ✅ Single factory |
| **Structured Fields** | tick, event_type, payload, extra | ✅ Queryable |
| **Rotation** | `io/logging/rolling_jsonl.RollingJsonlWriter` | ✅ Prevents unbounded growth |
| **Correlation** | ❌ No run_id or trace_id | ❌ Cannot correlate across runs |
| **Sampling** | ❌ All events logged | ⚠️ High-frequency events flood logs |

### Log Files

| File | Purpose | Format | Retention |
|------|---------|--------|-----------|
| `events.jsonl` | All proprioception events + metrics | JSONL | Per-run (manual cleanup) |
| `macros.jsonl` | Emergent text outputs | JSONL | Per-run |
| `thoughts.jsonl` | Internal thoughts (optional) | JSONL | Per-run |
| `inbox.jsonl` | User text input (if file-based) | JSONL | Per-run |

### Sample Event (events.jsonl)
```json
{
  "timestamp": "2025-01-25T10:30:45.123Z",
  "tick": 1234,
  "event_type": "VTTouch",
  "payload": {
    "scout_id": "heat_scout_0",
    "neuron_idx": 42,
    "depth": 5
  },
  "extra": {
    "domain": "biology_consciousness",
    "N": 1000
  }
}
```

### Gaps & Recommendations

| Gap | Severity | Recommendation |
|-----|----------|----------------|
| **No correlation ID** | M | Add `run_id` UUID to all events |
| **No trace context** | M | Add `trace_id`, `span_id` for distributed tracing |
| **High-frequency flooding** | M | Sample events (e.g., log 1% of VTTouch) |
| **No log aggregation** | L | Integrate with Loki, ELK, or Splunk |
| **No alerting** | L | Add alerts for anomalies (e.g., ZEMA spike) |

**Logging Score**: **3.5/5** (Solid structured logging; lacks correlation and sampling)

---

## TRACING

### Current State
- **Distributed Tracing**: ❌ Not implemented
- **Instrumentation**: ❌ No OpenTelemetry, Jaeger, or Zipkin
- **Call Stack Context**: ⚠️ Python traceback on exceptions only

### Desired State (Production)
- **Trace per Run**: Unique `trace_id` for entire run (init → shutdown)
- **Spans**:
  - Root span: `run_loop()` (duration = total runtime)
  - Child spans: `compute_step()`, `save_checkpoint()`, `emit_telemetry()`
- **Context Propagation**: Pass trace context through function calls

### Implementation Recommendation
```python
# Pseudo-code using OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

tracer = trace.get_tracer(__name__)

def run_loop(...):
    with tracer.start_as_current_span("run_loop") as span:
        span.set_attribute("N", config.N)
        span.set_attribute("domain", config.domain)
        for tick in range(start_step, total_ticks):
            with tracer.start_as_current_span("compute_step"):
                compute_step_and_metrics(...)
```

**Tracing Score**: **0/5** (Not implemented; critical for production debugging)

---

## METRICS

### Current Metrics

| Metric | Source | Frequency | Storage |
|--------|--------|-----------|---------|
| **ZEMA** (topology Z-score) | `core/metrics.StreamingZEMA` | Every tick | events.jsonl |
| **Clustering Coefficient** | `core/metrics.compute_metrics()` | Every tick | events.jsonl |
| **Avg Path Length** | `core/metrics.compute_metrics()` | Every tick | events.jsonl |
| **Degree Distribution** | `core/metrics.compute_metrics()` | Every tick | events.jsonl |
| **Event Counts** | `core/proprioception.EventDrivenMetrics` | Every tick | events.jsonl |
| **Novelty Score** | `io/cognition/speaker.novelty_and_score()` | On speak | macros.jsonl |

### Metrics Dashboard
- **Frontend**: Plotly charts in `vdm_live.py` dashboard
- **Real-Time**: Polling JSONL files (1s interval)
- **Historical**: Full replay from events.jsonl

### Gaps & Recommendations

| Gap | Severity | Recommendation |
|-----|----------|----------------|
| **No runtime metrics** | M | Add CPU%, memory, GPU utilization |
| **No latency histograms** | M | Add p50, p95, p99 for core_step() |
| **No error rates** | M | Track exception counts, types |
| **No cardinality limits** | L | Cap degree_dist to top-k (avoid explosion) |
| **No Prometheus export** | L | Add `/metrics` endpoint for Prometheus scraping |

### Recommended Metrics (Production)
```prometheus
# Runtime performance
vdm_core_step_duration_seconds{quantile="0.5"} 0.012
vdm_core_step_duration_seconds{quantile="0.95"} 0.023

# Resource utilization
vdm_memory_bytes{type="connectome"} 524288000
vdm_gpu_memory_bytes{device="0"} 8589934592

# Domain metrics
vdm_zema_score 2.34
vdm_events_total{type="VTTouch"} 123456

# Error rates
vdm_errors_total{type="checkpoint_write_failed"} 0
```

**Metrics Score**: **4/5** (Rich domain metrics; lacks runtime/infra metrics)

---

## CONFIGURATION MANAGEMENT

### Current Mechanisms

| Mechanism | Location | Precedence | Pros | Cons |
|-----------|----------|------------|------|------|
| **Argparse** | `cli/args.py` | 1 (highest) | CLI-friendly | ~50 flags; unwieldy |
| **JSON Profiles** | `run_profiles/*.json` | 2 | Versioned, shareable | No schema validation |
| **Environment Variables** | `.env`, `.env.local` | 3 (lowest) | Deploy flexibility | **Secrets committed** (H risk) |

### Configuration Sources
1. **CLI**: `python run_nexus.py --neurons 1000 --hz 10 --seed 42`
2. **Profile**: `python run_nexus.py --profile run_profiles/03_jlietz_fuvdm.json`
3. **Env**: `RUNS_ROOT=/mnt/data/runs DASH_HOST=0.0.0.0 python vdm_live.py`

### Validation
- **Runtime**: Minimal (argparse type coercion only)
- **Schema**: ❌ No JSON Schema for profiles
- **Secrets**: ❌ No redaction in logs

### Gaps & Recommendations

| Gap | Severity | Recommendation |
|-----|----------|----------------|
| **Config fragmentation** | M | Consolidate to Pydantic Settings |
| **No schema validation** | M | Add JSON Schema for run profiles |
| **Secrets in .env** | **H** | Move to secrets manager (AWS, Vault) |
| **No config versioning** | M | Add `config_version` field to profiles |
| **No defaults manifest** | L | Generate `defaults.json` from argparse |

### Recommended Approach (Pydantic)
```python
from pydantic import BaseSettings, Field

class VDMConfig(BaseSettings):
    N: int = Field(1000, ge=10, le=1_000_000)
    k: int = Field(12, ge=1, le=100)
    hz: int = Field(10, ge=1, le=1000)
    domain: str = Field("biology_consciousness")
    seed: int = Field(0, ge=0)
    run_dir: Path = Field(Path("runs"))
    
    class Config:
        env_prefix = "VDM_"  # Read from VDM_N, VDM_K, etc.
        json_schema_extra = {
            "version": "0.1.0"
        }
```

**Configuration Score**: **2/5** (Fragmented; lacks validation; secrets leak)

---

## FEATURE FLAGS

### Current Flags (Environment Variables)

| Flag | Default | Purpose |
|------|---------|---------|
| `FORCE_DENSE` | 0 | Use dense connectome (validation only) |
| `ENABLE_EVENT_METRICS` | 1 | Enable EventDrivenMetrics |
| `ENABLE_COLD_SCOUTS` | 1 | Enable ColdScout void walkers |
| `B1_HALF_LIFE_TICKS` | 50 | Bias signal decay rate |
| `B1_HYSTERESIS` | 1.0 | Bias signal hysteresis threshold |
| `PYTHONUNBUFFERED` | 1 | Unbuffered stdout (set by runtime) |
| `RUNS_ROOT` | `./runs` | Root directory for run artifacts |
| `DASH_HOST` | `127.0.0.1` | Dash server host |
| `DASH_PORT` | 8060 | Dash server port |

### Feature Flag System
- **Mechanism**: `os.getenv("FLAG", default)` scattered across codebase
- **Discovery**: Grep for `os.getenv` (no central registry)
- **Validation**: None (values not type-checked)

### Gaps & Recommendations

| Gap | Severity | Recommendation |
|-----|----------|----------------|
| **No central registry** | M | Create `FeatureFlags` dataclass |
| **No runtime toggle** | L | Add `/admin/flags` endpoint for live updates |
| **No A/B testing** | L | Add percentage-based rollout (e.g., 10% get flag) |
| **No flag deprecation** | L | Track flag lifetime; warn on deprecated |

### Recommended Approach
```python
@dataclass
class FeatureFlags:
    force_dense: bool = False
    enable_event_metrics: bool = True
    enable_cold_scouts: bool = True
    b1_half_life_ticks: int = 50
    
    @classmethod
    def from_env(cls):
        return cls(
            force_dense=bool(int(os.getenv("FORCE_DENSE", "0"))),
            enable_event_metrics=bool(int(os.getenv("ENABLE_EVENT_METRICS", "1"))),
            ...
        )
```

**Feature Flags Score**: **2/5** (Present but primitive; no registry or validation)

---

## HEALTH CHECKS & STATUS

### Current Endpoints

| Endpoint | Implementation | Purpose |
|----------|----------------|---------|
| **HTTP Status** | `runtime/helpers/status_http.py` | Optional status server |
| **status.json** | Written to `runs/{timestamp}/status.json` | Polled by frontend |

### Status Payload (status.json)
```json
{
  "tick": 1234,
  "uptime_s": 123.45,
  "N": 1000,
  "k": 12,
  "hz": 10,
  "domain": "biology_consciousness",
  "last_checkpoint": "state_1200.h5",
  "events_count": 54321
}
```

### Health Check Endpoints (Desired)
```
GET /health
  → 200 OK if running
  → 503 Service Unavailable if crashed

GET /readiness
  → 200 OK if connectome initialized
  → 503 if still loading engram

GET /liveness
  → 200 OK if main loop responsive
  → 500 if deadlocked
```

### Gaps & Recommendations

| Gap | Severity | Recommendation |
|-----|----------|----------------|
| **No standard health checks** | M | Add `/health`, `/readiness`, `/liveness` |
| **No heartbeat** | M | Update status.json every tick (timestamp) |
| **No crash detection** | M | Watchdog process to monitor heartbeat |
| **No graceful shutdown** | L | Handle SIGTERM to flush logs, save checkpoint |

**Health Checks Score**: **2/5** (Basic status.json; no standard probes)

---

## DEPLOYMENT & CONTAINERS

### Current Deployment
- **Method**: Manual `python run_nexus.py` on workstation or HPC
- **Dependencies**: `pip install -r requirements.txt` (unpinned)
- **No Container**: ❌ No Dockerfile or docker-compose.yaml

### Recommended Containerization
```dockerfile
# Dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y git build-essential
COPY requirements-lock.txt /app/
RUN pip install --no-cache-dir -r /app/requirements-lock.txt
COPY vdm_rt /app/vdm_rt
COPY run_profiles /app/run_profiles
WORKDIR /app
ENTRYPOINT ["python", "vdm_rt/run_nexus.py"]
```

### Orchestration (Kubernetes)
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vdm-runner
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: vdm
        image: prometheus-vdm:latest
        args: ["--profile", "run_profiles/05_10k_fuvdm.json"]
        resources:
          limits:
            memory: "8Gi"
            nvidia.com/gpu: 1
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 30
```

**Deployment Score**: **1/5** (No containerization; manual setup only)

---

## ALERTING & MONITORING

### Current State
- **No Alerting**: ❌ No integration with PagerDuty, Slack, email
- **Monitoring**: Manual dashboard observation (vdm_live.py)

### Desired Alerts (Production)

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| **ZEMA Spike** | zema_score > 5.0 | Warning | Log, notify |
| **Checkpoint Failure** | checkpoint_write_failed > 0 | Critical | Retry, alert |
| **Memory Leak** | memory_bytes increasing trend | Warning | Investigate |
| **Core Step Slow** | step_duration_p95 > 2 * baseline | Warning | Profile |
| **Crash** | Heartbeat timeout (60s) | Critical | Restart, alert |

### Implementation Recommendation
- **Prometheus + Alertmanager**: Scrape `/metrics` endpoint
- **Grafana**: Visualize metrics, set thresholds
- **Alertmanager**: Route to Slack, PagerDuty

**Alerting Score**: **0/5** (Not implemented)

---

## OVERALL OPERABILITY SCORE

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Logging | 3.5/5 | 25% | 0.875 |
| Tracing | 0/5 | 15% | 0.0 |
| Metrics | 4/5 | 20% | 0.8 |
| Configuration | 2/5 | 15% | 0.3 |
| Feature Flags | 2/5 | 5% | 0.1 |
| Health Checks | 2/5 | 10% | 0.2 |
| Deployment | 1/5 | 5% | 0.05 |
| Alerting | 0/5 | 5% | 0.0 |

**Total Operability Score**: **2.325/5** (D+; requires significant investment)

---

## CRITICAL GAPS (Priority Order)

1. **Secrets Leakage** (P0): Remove .env from git; add secrets manager
2. **Correlation IDs** (P1): Add run_id to all logs
3. **Health Checks** (P1): Implement /health, /readiness, /liveness
4. **Config Consolidation** (P1): Pydantic Settings
5. **Distributed Tracing** (P2): OpenTelemetry integration
6. **Alerting** (P2): Prometheus + Alertmanager
7. **Containerization** (P2): Dockerfile + docker-compose
8. **Runtime Metrics** (P3): CPU, memory, GPU tracking
