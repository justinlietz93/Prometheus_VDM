#pragma once
//
// VDM Nexus — Domain Models (plain data only; no framework imports)
// References:
//   - Architecture seams (§12.4): ../../NEXUS_ARCHITECTURE.md
//   - Execution plan (Phase 2.1.2 models list): ../../VDM_Nexus/TODO_CHECKLIST.md
//
// Rules:
//   - POD/POJO style structs; no Qt/DB/Python includes.
//   - No thresholds or equations derived from Markdown canon; thresholds are resolved by ISchemaCatalog from spec/schema.
//   - Keep serialization/persistence out of domain (handled by application/infrastructure).
//

#include <string>
#include <vector>
#include <map>
#include <optional>
#include <cstdint>

namespace vdm_nexus {
namespace domain {

// Unique experiment identity within the repository policy.
struct ExperimentId {
  std::string domain;   // e.g., "thermo_routing", "metriplectic"
  std::string script;   // e.g., "run_kg_energy_oscillation.py"
  std::string tag;      // prereg/run tag string
};

// Reference to the canonical spec and its governing schema (paths only).
struct RunnerSpecRef {
  std::string spec_path;    // Derivation/code/physics/.../*.json (spec)
  std::string schema_path;  // Derivation/code/physics/.../*.schema.json
};

// Minimal Experiment record tying identity to spec and provenance commit.
struct Experiment {
  ExperimentId id;
  RunnerSpecRef spec;
  std::string repo_commit;  // git commit hash for provenance
};

// Gate definition shell (labels only; thresholds resolved by ISchemaCatalog).
struct GateDef {
  std::string id;           // KPI/gate identifier key
  std::string anchor;       // markdown anchor into VALIDATION_METRICS.md (definitions only)
  std::optional<double> threshold;   // optional echo for UI; authoritative source is spec/schema
  std::optional<std::string> relation; // e.g., "<=", ">=", "=="
};

// KPI value container (no computation here; adapters fill values from runner JSON).
struct KPIValue {
  std::string id;           // KPI key (matches spec/schema fields)
  double value {0.0};
  std::optional<bool> passed; // UI may populate after comparing to spec-derived thresholds
};

// Canonical artifact descriptor (read in place; never relocated).
struct Artifact {
  std::string path;                         // repo-relative or absolute
  std::string type;                         // "png" | "csv" | "json" | "vti" | ...
  std::optional<std::string> sha256;      // optional content hash
  std::optional<std::uint64_t> size;      // optional size in bytes
};

// Approval receipts (provenance only; writes occur via CLI, not GUI).
struct ApprovalReceipt {
  std::string approver;       // human-readable identity
  std::string hmac;           // script-scoped HMAC ID
  std::string timestamp_utc;  // ISO-8601 UTC
};

// Approval status mirror (domain-level; adapters populate from approvals DB).
struct ApprovalStatus {
  bool approved {false};
  std::optional<ApprovalReceipt> last_receipt;
  std::string guilty_field;   // populated on policy mismatch; empty when OK
};

// Nexus execution/settings resolved per policy (CLI > env > .env).
struct NexusSettings {
  std::string repo_root;         // VDM_REPO_ROOT
  std::string approval_db;       // VDM_APPROVAL_DB
  std::string approval_admin_db; // VDM_APPROVAL_ADMIN_DB
  bool gui_mode {false};         // whether to request GUI-mode sidecars from runners
};

// Run-manifest reference (schema and path only; treated read-only).
struct RunManifestRef {
  std::string manifest_schema;   // e.g., "vdm.run-manifest.v1"
  std::string manifest_path;     // path to manifest JSON (read-only)
};

// Catalog entry used by discovery/browsers (read-only inventory).
struct CatalogEntry {
  ExperimentId id;
  std::string script_path;   // canonical runner script path
  std::string spec_path;     // spec JSON path
  std::string schema_path;   // schema JSON path
  std::string mtime_utc;     // last-modified time as ISO-8601 for UI freshness
};

} // namespace domain
} // namespace vdm_nexus