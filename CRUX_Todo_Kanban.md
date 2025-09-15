# CRUX Project - Todo Kanban

This kanban board tracks all unchecked items from the Providers Roadmap Checklist, organized by priority and status.

Legend: [ ] = not started, [~] = in progress, [x] = done

## 🔴 CRITICAL (High Importance / High Urgency)

### Not Started
- [ ] 6. Unified timeout & cancellation strategy (standard default + overridable)

### In Progress
- [~] 4. Standardize retry policy (core RetryConfig + retry() + attempt logger hook added; Anthropic + Gemini integrated; remaining providers pending: OpenAI, Deepseek, OpenRouter, Ollama, XAI)

## 🟠 HIGH (High Importance / Medium Urgency)

### Not Started
- [ ] 7. Enrich error taxonomy (map HTTP status codes -> granular ErrorCode variants)
- [ ] 8. Capture request/response IDs when available (store in ProviderMetadata.extra)
- [ ] 9. Normalize structured logging field set (phase, emitted, tokens, structured, error_code, attempt)
- [ ] 10. Add cancellable iterator / StreamController for early consumer cancellation
- [ ] 11. Reuse / pool httpx clients (reduce per-call allocation & connection overhead)

## 🟡 MEDIUM (Medium Importance / High Enhancement Value)

### Not Started
- [ ] 12. BaseOpenAIStyleProvider abstraction (OpenAI / Deepseek / XAI shared logic)
- [ ] 13. Latency metrics: add time_to_first_token + total_duration for streaming
- [ ] 14. Token usage placeholders in metadata (even if None initially)

## 🟢 MEDIUM-LOW (Medium Importance / Low Urgency)

### Not Started
- [ ] 16. DTO validation (pydantic) for inbound ChatRequest & messages
- [ ] 17. Logging verbosity controls (suppress per-delta logs at higher levels)
- [ ] 18. Protocol / stub types to remove getattr try/except patterns

## 🔵 LOW (Low Importance / High Enhancement Value)

### Not Started
- [ ] 19. Convenience provider.simple(text, \*\*opts) helper
- [ ] 20. Capability caching (which models support JSON / tools)
- [ ] 21. OpenTelemetry tracing instrumentation (span per provider call + stream lifecycle)
- [ ] 22. Cross-provider guarantees matrix docs (README section)

## 🟣 LOW (Low Importance / Medium Enhancement Value)

### Not Started
- [ ] 23. CLI smoke tester (providers-cli test 'provider')
- [ ] 24. Benchmark harness (latency distribution, warm vs cold)
- [ ] 25. Pluggable middleware chain (pre/post hooks for metrics, redaction)

## ⚡ SMALL / QUICK WINS

### Not Started
- [ ] 26. finalize_stream(ctx, emitted_any) helper for terminal event + log consolidation
- [ ] 28. Use contextlib.ExitStack for streaming resource management readability

### In Progress
- [~] 27. Make supports_streaming() reflect SDK presence consistently

## 🛡️ DEFENSIVE HARDENING

### Not Started
- [ ] 29. Sanitize / trim empty user segments before join
- [ ] 30. Optional max input size guard / chunking for huge prompts

## 🔮 OPTIONAL FUTURE ENHANCEMENTS

### Not Started
- [ ] 31. Tool invocation routing stub (standard tool result shape)
- [ ] 32. Partial / function-call style structured output abstraction

## 💾 PROVIDER SERVICE PERSISTENCE (SQLite Migration)

### In Progress
- [~] P3. Implement SQLite repositories and connection management (WAL, timeouts) (base repos scaffolded; consolidation pending)
- [~] P4. Wire DI and refactor FastAPI controllers to be thin (partial: controllers call db helpers; full DI wiring pending)
- [~] P7. Unit tests for repos and migrator; smoke test chat + metrics (smoke + db helper tests added; edge cases & repo tests pending)
- [~] P8. Documentation updates (README and memory bank) and deprecate JSON vault after migration (docs updated; final deprecation note pending)

## 🔧 NEW COMPLEXITY & PERSISTENCE REFACTORS

### Not Started
- [ ] C11. Reduce `_infer_caps` complexity (target <=8) using table-driven inference.
- [ ] C12. Relocate `model_registry_store.py` from `service/` to `persistence/sqlite/` package (pure DB concerns) and adjust imports.
- [ ] C13. Add focused unit tests for context length parsing edge cases ("1.5k", "4,096", "8k tokens").
- [ ] C14. Add tests for capability inference patterns to prevent regression after refactor (gpt-4o, o1/o3 reasoning, embeddings, vision, search).

## 📋 ADDITIONAL COMPLEXITY REFACTORS

### Not Started
- [ ] C1. Reduce cyclomatic complexity: split `init_db` into helpers (tables, indexes, import) and `save_models_snapshot` model serialization helpers.
- [ ] C2. Refactor `migrate_from_json_vault` into discrete key/prefs import helpers; enforce CCN <= 8.
- [ ] C3. Rename `_extracted_from__from_config_12` in keys repo to meaningful helper; simplify branching.
- [ ] C4. Add edge-case tests: keys overwrite/empty/invalid names; prefs unusual types/update/remove; metrics negative duration (raise ValueError) & error status.
- [ ] C5. Enforce negative duration validation in `record_metric`.
- [ ] C6. Centralize ENV_MAP for provider env var mapping (avoid duplication in app & elsewhere).
- [ ] C7. Consolidate duplicated SQLite initialization (engine vs service/db) or clearly document separation.
- [ ] C8. Normalize structured logging field set across providers (tokens, attempt, phase, error_code).
- [ ] C9. Add capability inference unit test ensuring detection for streaming/json/listing/default model flags.

---

## 📊 Status Summary

- **Critical**: 1 not started, 1 in progress
- **High**: 5 not started
- **Medium**: 3 not started
- **Medium-Low**: 3 not started
- **Low (High Enhancement)**: 4 not started
- **Low (Medium Enhancement)**: 3 not started
- **Small/Quick Wins**: 2 not started, 1 in progress
- **Defensive Hardening**: 2 not started
- **Optional Future**: 2 not started
- **Persistence (SQLite)**: 4 in progress
- **Complexity Refactors**: 13 not started

**Total Unchecked Items**: 43

---

## 🎯 Recommended Execution Order

1. **Foundation (Priority 1)**: Items 4, 9 - Testing + retry/log normalization foundation
2. **Code Quality (Priority 2)**: Items 26, 12 - Consolidate duplicated logic  
3. **Core Functionality (Priority 3)**: Items 6, 7, 8 - Timeout, metadata & error fidelity
4. **Performance & UX (Priority 4)**: Items 10, 11, 13 - Stream ergonomics & metrics
5. **Enhancement Items**: Remaining medium/low value items as capacity allows
6. **Complexity Refactors**: C1-C14 items to improve code maintainability

---

## 📝 Notes

- Update this kanban as tasks begin/complete by moving items between sections
- Prefer adding minimal targeted tests per item when feasible
- Keep provider-specific divergences documented explicitly if unification is deferred
- Items marked [~] are already in progress and should be prioritized for completion
- Cross-reference with main Providers Roadmap Checklist for detailed context and specifications