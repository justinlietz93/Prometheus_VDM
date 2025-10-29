#include <QCoreApplication>
#include <QDebug>
#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QString>
#include <QTimer>

#include "../presentation/DashboardController.h"

namespace {

QString qmlEntryPoint() {
  return QStringLiteral("qrc:/presentation/qml/Main.qml");
}

}  // namespace

int main(int argc, char* argv[]) {
  QGuiApplication app(argc, argv);
  QGuiApplication::setApplicationDisplayName(QStringLiteral("VDM Nexus"));
  QGuiApplication::setApplicationName(QStringLiteral("VDM Nexus"));

  DashboardController controller;
  const bool loaded = controller.loadIndex(QString());
  qInfo().noquote() << "[NEXUS][INDEX]"
                    << (loaded ? "loaded" : "missing")
                    << "repo_head=" << controller.repoHead()
                    << "pending_approvals=" << controller.pendingApprovals()
                    << "orphan_proposals=" << controller.orphanProposals()
                    << "results_total=" << controller.resultsTotal()
                    << "proposals_total=" << controller.totalProposals()
                    << "code_domains_tracked=" << controller.codeDomainsTracked()
                    << "documentation_buckets=" << controller.documentationBuckets()
                    << "artifacts_total=" << controller.artifactsTotal();

  QQmlApplicationEngine engine;
  engine.rootContext()->setContextProperty(QStringLiteral("dashboardController"), &controller);

  const QUrl url = QUrl::fromUserInput(qmlEntryPoint());
  QObject::connect(
      &engine, &QQmlApplicationEngine::objectCreated, &app,
      [url](QObject* obj, const QUrl& objUrl) {
        if (!obj && url == objUrl) {
          QCoreApplication::exit(-1);
        }
      },
      Qt::QueuedConnection);

  engine.load(url);
  if (engine.rootObjects().isEmpty()) {
    qCritical().noquote() << "[NEXUS][QML] failed to load" << url;
    return -1;
  }

  const QString platform = qEnvironmentVariable("QT_QPA_PLATFORM");
  if (platform.compare(QStringLiteral("offscreen"), Qt::CaseInsensitive) == 0) {
    QTimer::singleShot(0, &app, [&app]() {
      qInfo().noquote()
          << "[NEXUS][QML] offscreen platform detected; exiting after successful"
             " load";
      app.quit();
    });
  }

  return app.exec();
}
