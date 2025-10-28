#pragma once
//
// VDM Nexus — Application Ports (Clean Architecture interfaces)
// Reference: NEXUS standard §12.4 (Clean Architecture seams)
//   See: ../../NEXUS_ARCHITECTURE.md
//
// Policy:
// - Read-only lens over canonical derivation tree; no Qt/DB/Python includes here.
// - Thresholds/approvals are sourced from canonical structured artifacts (schemas/specs/DB), never from Markdown.
// - Adapters live in ../infrastructure/* and must implement these interfaces.
// - Presentation must depend on application ports/use-cases, not on infrastructure.
//
// Checklist alignment:
// - TODO_CHECKLIST.md Task 2.1.1 — Define ports in application/ports (this file).
// - TODO_CHECKLIST.md Task 2.1.3 — Adapters must honor constructor injection (to be implemented in infrastructure).
//

#include <string>
#include <vector>
#include <map>
#include <optional>
#include <cstdint>

namespace vdm_nexus {
namespace app {

// ---- Common plain-data types (no framework headers) ----

struct ApprovalReceipt {
  std::string approver;       // human-readable identity (from approvals DB)
  std::string hmac;           // script-scoped HMAC ID
  std::string timestamp_utc;  // ISO-8601
};

struct ApprovalsStatus {
  bool approved {false};
  std::optional<ApprovalReceipt> last_receipt;
  std::string guilty_field;   // populated by policy checker on mismatch; empty if ok
};

struct ArtifactInfo {
  std::string path;           // repo-relative or absolute path (policy-resolved)
  std::string type;           // "png" | "csv" | "json" | "vti" | "vtp" | "vtu" | ...
  std::string sha256;         // content hash (empty if not computed)
  std::uint64_t size {0};     // bytes (0 if unknown)
};

struct MarkdownDoc {
  std::string path;           // canon Markdown path
  std::string content;        // raw text (rendering handled elsewhere)
  std::string commit;         // git commit hash for provenance banner
};

struct SchemaError {
  std::string instance_path;  // JSON pointer of failing node
  std::string message;        // validator message
};

struct SchemaValidation {
  bool valid {false};
  std::string schema_path;                    // path to JSON Schema used
  std::vector<SchemaError> errors;          // empty when valid
};

// ---- Ports (pure abstract interfaces) ----
// NEXUS_ARCHITECTURE.md §12.4 mandates these seams.
// No writes occur through these interfaces except launching canonical CLIs/runners
// via IRunnerService and calling the approvals CLI externally (not exposed here).

class IApprovalRepo {
public:
  virtual ~IApprovalRepo() = default;

  // Query approval status for a (domain, script, tag).
  // Example keying matches policy: "domain:script:tag".
  virtual ApprovalsStatus status(const std::string& domain,
                                 const std::string& script,
                                 const std::string& tag) const = 0;
};

class IRunnerService {
public:
  virtual ~IRunnerService() = default;

  struct LaunchRequest {
    std::string script_path;                    // Derivation/code/physics/.../run_*.py
    std::string spec_path;                      // Path to spec JSON
    std::map<std::string, std::string> env;   // Resolved env (VDM_REPO_ROOT, VDM_APPROVAL_DB/Admin, etc.)
    bool gui_mode {false};                      // When true, set VDM_NEXUS=1 for in-situ adapters
  };

  struct LaunchHandle {
    int pid {-1};               // OS process id if available
    std::string run_tag;        // Adapter-provided or derived tag to associate artifacts
  };

  // Launch a canonical Python runner with deterministic environment.
  // Must fail fast on approvals mismatch; stderr/stdout streaming is handled by adapter/monitor.
  virtual LaunchHandle launch(const LaunchRequest& req) = 0;
};

class IArtifactStore {
public:
  virtual ~IArtifactStore() = default;

  // Enumerate artifacts for a domain and (optional) run tag, operating strictly in place.
  virtual std::vector<ArtifactInfo> list_artifacts(const std::string& domain,
                                                     const std::optional<std::string>& run_tag) const = 0;

  // Compute SHA-256 for a path; adapters may cache results (never relocate files).
  virtual std::string sha256(const std::string& path) const = 0;
};

class IMarkdownReader {
public:
  virtual ~IMarkdownReader() = default;

  // Read canon Markdown (read-only) and surface visible commit hash for banners.
  virtual MarkdownDoc read(const std::string& path) const = 0;
};

class ISchemaCatalog {
public:
  virtual ~ISchemaCatalog() = default;

  // Validate a JSON file against a JSON Schema.
  virtual SchemaValidation validate_json(const std::string& json_path,
                                         const std::string& schema_path) const = 0;

  // Resolve KPI thresholds strictly from the experiment spec or its referenced schema.
  // Never derive thresholds from Markdown canon.
  virtual std::map<std::string, double> thresholds_from_spec(const std::string& spec_path) const = 0;

  // Optional: discover available (domain, script, tag) catalog entries with timestamps for UIs.
  virtual std::vector<std::string> list_specs_for_domain(const std::string& domain) const = 0;
};
 
// Memory graph interfaces removed from Nexus scope (PathRAG, KG‑Lite).
// Ownership relocated to memory-bank plans and standards:
//  - [KG_Lite_Retrieval_and_Evaluation.md](../../memory-bank/plans/KG_Lite_Retrieval_and_Evaluation.md:1)
//  - [MEMORY_GRAPH_STANDARDS.md](../../memory-bank/MEMORY_GRAPH_STANDARDS.md:188)
// This space intentionally left blank to preserve include stability.
 
// Notes for implementers (../infrastructure/*):
// - Match environment precedence: CLI flags > env vars > .env (see NEXUS §7).
// - Approvals writes must shell through approve_tag.py (GUI stores no secrets).
// - Artifacts must be enumerated via canonical paths in place (no copies/renames).
// - Telemetry/stdout streaming must avoid truncation; GUI presents a read-only mirror.
// - Keep each implementation file ≤ 500 LOC and provide constructor-injected dependencies.
 
} // namespace app
} // namespace vdm_nexus