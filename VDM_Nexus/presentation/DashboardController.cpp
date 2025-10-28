#include "DashboardController.h"

#include <QCoreApplication>
#include <QFile>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QStandardPaths>

namespace {

// Return true if an approval meta object has a non-empty "approved_at" field.
static bool isApproved(const QJsonObject& meta) {
  auto it = meta.find("approved_at");
  if (it == meta.end()) return false;
  const auto v = it.value();
  if (v.isString()) return !v.toString().trimmed().isEmpty();
  return false;
}

} // namespace

DashboardController::DashboardController(QObject* parent)
  : QObject(parent) {
}

void DashboardController::reset() {
  m_pendingApprovals = 0;
  m_orphanProposals = 0;
  m_artifactsTotal = 0;
  m_repoHead.clear();
}

QString DashboardController::defaultIndexPath() const {
  // Resolution precedence for repo root (CLI flags would be handled by app args; here we read env):
  // 1) VDM_REPO_ROOT (absolute)
  // 2) Fallback relative to application dir: <repo>/VDM_Nexus/reports/nexus-roadmap-index.v1.json
  const QString envRoot = qEnvironmentVariable("VDM_REPO_ROOT");
  const QString relIndex = "VDM_Nexus/reports/nexus-roadmap-index.v1.json";
  if (!envRoot.trimmed().isEmpty()) {
    return QDir(envRoot).filePath(relIndex);
  }
  // Attempt relative to process working directory first
  QString pathCwd = QDir::current().filePath(relIndex);
  if (QFile::exists(pathCwd)) return pathCwd;
  // Attempt relative to application binary dir
  const QString appDir = QCoreApplication::applicationDirPath();
  QString pathApp = QDir(appDir).filePath(relIndex);
  return pathApp;
}

bool DashboardController::loadIndex(const QString& path) {
  QString p = path;
  if (p.trimmed().isEmpty()) {
    p = defaultIndexPath();
  }
  QFile f(p);
  if (!f.exists()) {
    reset();
    emit changed();
    return false;
  }
  if (!f.open(QIODevice::ReadOnly)) {
    reset();
    emit changed();
    return false;
  }
  const QByteArray data = f.readAll();
  f.close();
  const bool ok = computeFromJson(data);
  emit changed();
  return ok;
}

bool DashboardController::computeFromJson(const QByteArray& data) {
  reset();
  QJsonParseError perr{};
  const QJsonDocument doc = QJsonDocument::fromJson(data, &perr);
  if (perr.error != QJsonParseError::NoError || !doc.isObject()) {
    return false;
  }
  const QJsonObject root = doc.object();

  // repo_head
  if (root.contains("repo_head") && root.value("repo_head").isString()) {
    m_repoHead = root.value("repo_head").toString();
  }

  // code_domains: compute pending approvals and artifact totals
  int pending = 0;
  int logs = 0;
  int figs = 0;

  const QJsonValue cdVal = root.value("code_domains");
  if (cdVal.isArray()) {
    const QJsonArray codeDomains = cdVal.toArray();
    for (const QJsonValue& v : codeDomains) {
      if (!v.isObject()) continue;
      const QJsonObject cd = v.toObject();

      // approvals.allowed_tags vs approvals.approvals[tag].approved_at
      const QJsonObject approvals = cd.value("approvals").toObject();
      const QJsonArray allowed = approvals.value("allowed_tags").toArray();
      const QJsonObject approvedMap = approvals.value("approvals").toObject();

      for (const QJsonValue& tagVal : allowed) {
        const QString tag = tagVal.toString();
        const QJsonObject meta = approvedMap.value(tag).toObject();
        const bool ok = isApproved(meta);
        if (!ok) pending += 1;
      }

      // outputs logs_total, figures_total
      const QJsonObject outputs = cd.value("outputs").toObject();
      if (outputs.contains("logs_total")) {
        logs += outputs.value("logs_total").toInt(0);
      }
      if (outputs.contains("figures_total")) {
        figs += outputs.value("figures_total").toInt(0);
      }
    }
  }

  // proposal_status: count has_results == false
  int orphan = 0;
  const QJsonValue psVal = root.value("proposal_status");
  if (psVal.isArray()) {
    const QJsonArray ps = psVal.toArray();
    for (const QJsonValue& v : ps) {
      if (!v.isObject()) continue;
      const QJsonObject row = v.toObject();
      const QJsonValue hasRes = row.value("has_results");
      const bool b = hasRes.isBool() ? hasRes.toBool() : false;
      if (!b) orphan += 1;
    }
  }

  m_pendingApprovals = pending;
  m_orphanProposals = orphan;
  m_artifactsTotal = logs + figs;
  return true;
}