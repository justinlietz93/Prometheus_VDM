#pragma once

#include <QString>
#include <QStringList>
#include <QDateTime>

/**
 * @brief Canonical experiment descriptor mirrored from derivation/code/physics/* metadata.
 *
 * This struct remains framework-free; it is consumed by application use-cases and
 * infrastructure adapters (filesystem, approvals DB) to orchestrate runner launches.
 */
namespace vdm::domain {

struct Experiment {
  QString tag;                 ///< Unique experiment tag (e.g., rd_front_speed)
  QString domain;              ///< Physics domain folder under derivation/code/physics
  QString runnerScript;        ///< Python runner path relative to repository root
  QString specPath;            ///< Path to active spec JSON (canon; read-only)
  QString schemaPath;          ///< Path to JSON Schema validating the spec
  QString proposalPath;        ///< Path to PROPOSAL_* Markdown (viewer-only)
  QString approvalsRequired;   ///< Approval tag or ID required before launch
  QStringList artifactsExpected; ///< e.g., {"PNG","CSV","JSON"} as mandated by RESULTS standards
  QDateTime lastDiscoveredUtc; ///< Timestamp of last catalog refresh (UTC)

  bool isValid() const noexcept {
    return !tag.isEmpty() && !domain.isEmpty() && !runnerScript.isEmpty();
  }
};

}  // namespace vdm::domain