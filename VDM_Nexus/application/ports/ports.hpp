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
 
// ---- Memory KG-Lite ports (read-only; no Qt/DB/Python includes) ----
// Reference schema: [kg-lite.chunkenvelope.v1.schema.json](../../memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite.chunkenvelope.v1.schema.json)
 
// Minimal descriptor for a chunk entry in the index payload
struct ChunkDescriptor {
  std::string chunk_id;   // "${set_id}@${set_version}:${chunk_type}"
  std::string kind;       // "meta" | "axes_dimensions" | "subfactors" | "signals" | "edges" | "retrieval_policy" | "index"
  std::string sha256;     // 64-hex; payload canonical JSON hash
};
 
// In-memory mirror of the KG-Lite set index; adapters populate from index envelope
struct MemoryIndex {
  std::string set_id;
  std::string set_version;
  std::string schema_version;                // payload.schema_version
  std::vector<ChunkDescriptor> chunks;       // payload.chunks[*]
  std::map<std::string,int> counts;           // payload.counts (axes, dimensions, subfactors, signals, edges, ...)
  std::string source;                        // envelope.source (path to justin-graph.json)
};
 
// MemoryStore port exposes read-only access to KG-Lite envelopes stored under memory-bank/
// Adapters must not mutate or relocate files; all paths are resolved in place.
class IMemoryStore {
public:
  virtual ~IMemoryStore() = default;
 
  // List available memory sets (e.g., ["justin@1.0"])
  virtual std::vector<std::string> list_sets() const = 0;
 
  // Load the set index (validates internal invariants and hashes where available)
  virtual MemoryIndex get_index(const std::string& set_id,
                                const std::string& set_version) const = 0;
 
  // Read the canonical payload JSON for a given chunk_id (opaque to application)
  virtual std::string read_payload_canonical_json(const std::string& chunk_id) const = 0;
 
  // Return the root where chunks are discovered (repo-relative or absolute)
  virtual std::string chunks_root() const = 0;
};
 
// PathRetriever port encapsulates KG-Lite retrieval policy (PathRAG)
// It consumes index + edges/signals payloads and yields candidate paths with scores.
struct PathConfig {
  double path_prune_alpha {0.8}; // [0,1]
  double path_threshold   {0.2}; // [0,1]
  double min_novelty      {0.55}; // [0,1]
  int    k_paths          {8};    // top-K paths to return
  int    max_hops         {4};    // hop cap to bound search
};
 
struct PathResult {
  std::vector<std::string> nodes; // ordered node ids along the path
  std::vector<std::string> edges; // ordered edge ids or "u->v:relation" strings
  double score {0.0};              // composite score after pruning
};
 
class IPathRetriever {
public:
  virtual ~IPathRetriever() = default;
 
  // Find K paths between start and goal within a memory set, honoring retrieval policy.
  virtual std::vector<PathResult> find_paths(const std::string& set_id,
                                              const std::string& set_version,
                                              const std::string& start_node_id,
                                              const std::string& goal_node_id,
                                              const PathConfig& cfg) const = 0;
};
 
// Notes for implementers (../infrastructure/*):
// - Match environment precedence: CLI flags > env vars > .env (see NEXUS §7).
// - Approvals writes must shell through approve_tag.py (GUI stores no secrets).
// - Artifacts must be enumerated via canonical paths in place (no copies/renames).
// - Telemetry/stdout streaming must avoid truncation; GUI presents a read-only mirror.
// - Keep each implementation file ≤ 500 LOC and provide constructor-injected dependencies.
 
} // namespace app
} // namespace vdm_nexus