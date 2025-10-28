#include <QGuiApplication>
#include <QDebug>
#include <QString>

#include "../presentation/DashboardController.h"

// Smoke-ingest the roadmap index JSON at startup (read-only) and print summary counters.
// This wires Task 1.3 ingestion without any GUI dependency; presentation panes can bind to
// DashboardController properties later via QML/Widgets.
int main(int argc, char* argv[]) {
  QGuiApplication app(argc, argv);

  DashboardController ctrl;
  const bool ok = ctrl.loadIndex(QString()); // default path resolution (VDM_REPO_ROOT or relative)
  qInfo().noquote() << "[NEXUS][INDEX]"
                    << (ok ? "loaded" : "missing")
                    << "repo_head=" << ctrl.repoHead()
                    << "pending_approvals=" << ctrl.pendingApprovals()
                    << "orphan_proposals=" << ctrl.orphanProposals()
                    << "artifacts_total=" << ctrl.artifactsTotal();

  // No GUI loop yet; exit immediately after ingest print (compile/run sanity).
  return 0;
}