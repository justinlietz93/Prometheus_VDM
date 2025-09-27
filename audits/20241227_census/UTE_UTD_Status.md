# UTE/UTD Pipeline Reality

## UTE (Universal Temporal Encoder)

### Architecture
**Location**: `fum_rt/io/ute.py`
**Class**: `UTE`
**Purpose**: Feeds inbound messages into queue for Nexus polling

### Input Sources
- **stdin**: Line-based text input (threading.Thread daemon)
- **Inbox file**: JSONL chat inbox tailer (optional)
- **Synthetic ticker**: Heartbeat generator (always active)

### Queue Interface
```python
self.q = queue.Queue(maxsize=1024)  # Bounded queue
{'type': 'text', 'msg': line}       # Message format
```

### Timescale Filters
**Not detected** - No explicit rhythm/oscillation feature extraction
**Gap**: UTE operates as simple message router, no temporal signal processing

### Missing UTE Features
- No frequency domain analysis
- No rhythm pattern recognition
- No oscillation feature surfacing to walkers/scoreboard
- No temporal correlation detection

## UTD (Universal Transduction Decoder)

### Architecture  
**Location**: `fum_rt/io/utd.py`
**Class**: `UTD`
**Purpose**: Opportunistic output emission with macro board support

### Output Sinks
- **stdout**: Direct text emission
- **JSONL files**: `utd_events.jsonl` (rolling or zip-compressed)
- **Macro board**: `macro_board.json` (persistent macro registry)

### API Surface
```python
emit_text(payload: dict, score: float=1.0)
register_macro(name: str, meta: dict | None=None) -> bool
list_macros() -> list[str]
emit_macro(name: str, args: dict | None=None, score: float=1.0)
```

### Gating Integration
**Environment Variables**:
- `FUM_ZIP_SPOOL=1` - Enable zip compression for output
- No explicit gate binding detected in UTD

## Pipeline Stages Analysis

### Current Reality vs Expected Stages

#### ✅ Present Stages
1. **Input Routing** (UTE): stdin → queue → Nexus
2. **Output Emission** (UTD): payload → stdout/files
3. **Macro System** (UTD): Named macro registration and invocation

#### ❌ Missing Stages
1. **Pointer-First**: No evidence of pointer-based message routing
2. **Draft**: No draft/preview stage before commitment
3. **Repair**: No error correction or message repair mechanisms
4. **Commit**: Simple emission, no transactional commit semantics

### Expected vs Actual Gate Binding

#### Expected Gate Integration
- Gates should control pipeline stage progression
- B1 signals should influence encoding/decoding decisions
- Territory boundaries should affect message routing

#### Actual Gate Integration
**Very Limited**:
- No explicit gate integration in UTE/UTD
- No B1 signal consumption
- No ADC territory-aware routing
- No walker feedback into pipeline

## Stage Diagram (Current Reality)

```
Input Sources          UTE Queue           Nexus Poll         Processing
┌─────────────┐       ┌─────────────┐     ┌─────────────┐   ┌─────────────┐
│   stdin     │──────▶│             │────▶│             │──▶│  connectome │
│   inbox     │       │ Queue(1024) │     │  poll()     │   │   walkers   │
│   ticker    │       │             │     │             │   │    GDSP     │
└─────────────┘       └─────────────┘     └─────────────┘   └─────────────┘

Processing Result      UTD Emission       Output Sinks
┌─────────────┐       ┌─────────────┐     ┌─────────────┐
│  analysis   │──────▶│  emit_text  │────▶│   stdout    │
│  decisions  │       │ emit_macro  │     │ JSONL files │
│  responses  │       │             │     │ macro_board │
└─────────────┘       └─────────────┘     └─────────────┘
```

## Known Gaps

### Missing Pipeline Intelligence
1. **No Text Analysis**: UTE passes through raw text without parsing
2. **No Semantic Routing**: Messages aren't routed based on content
3. **No Context Preservation**: No conversation or session state
4. **No Quality Gates**: No filtering of low-quality inputs/outputs

### Missing Gate Bindings
1. **B1 Integration**: B1 signals don't influence text processing
2. **Territory Routing**: ADC territories don't affect message handling
3. **Walker Feedback**: Walker discoveries don't influence encoding
4. **GDSP Coordination**: No structural feedback into text pipeline

### Missing Error Handling
1. **No Message Repair**: Corrupted inputs aren't fixed
2. **No Retry Logic**: Failed processing isn't retried
3. **No Fallback Routing**: No alternative paths for failed messages
4. **No Quality Metrics**: No assessment of pipeline health

## Integration Points (Current)

### UTE → Nexus
- Polling interface: `ute.q.get_nowait()`
- Message types: `{'type': 'text', 'msg': str}`
- No backpressure beyond queue size (1024)

### Nexus → UTD  
- Direct emission: `utd.emit_text(payload, score)`
- Macro system: `utd.emit_macro(name, args, score)`
- No filtering or preprocessing

### File System Integration
- **Input**: Optional JSONL inbox tailing
- **Output**: Rolling JSONL or zip-compressed logs
- **Persistence**: Macro board JSON storage

## Recommendations

### Short-term Improvements
1. **Add B1 Gate Binding**: Use B1 signals to modulate emission thresholds
2. **Territory-Aware Routing**: Route messages based on ADC territory context
3. **Quality Scoring**: Implement content quality assessment
4. **Error Recovery**: Add basic message repair and retry logic

### Long-term Vision
1. **Semantic Pipeline**: Parse and understand text content
2. **Context Preservation**: Maintain conversation/session state
3. **Multi-Stage Processing**: Implement draft/review/commit workflow
4. **Adaptive Gating**: Dynamic gate thresholds based on system state

### Current Limitations
- Pipeline is essentially input/output routing with no intelligence
- No integration with core VDM systems (B1, ADC, GDSP)
- Missing most expected pipeline stages (pointer-first, draft, repair, commit)
- No quality assurance or error recovery mechanisms