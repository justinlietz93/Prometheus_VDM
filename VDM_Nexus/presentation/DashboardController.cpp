#include "DashboardController.h"

#include <QCoreApplication>
#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonValue>
#include <QRegularExpression>
#include <QSet>
#include <QStringList>
#include <QVariantMap>

namespace {

QString normalizedRelativePath(const QString& relativePath);

// Return true if an approval meta object has a non-empty "approved_at" field.
static bool isApproved(const QJsonObject& meta) {
  auto it = meta.find("approved_at");
  if (it == meta.end()) return false;
  const auto v = it.value();
  if (v.isString()) return !v.toString().trimmed().isEmpty();
  return false;
}

QVariantList makeSpotlightCards(const QJsonArray& cards) {
  QVariantList result;
  result.reserve(cards.size());
  for (const QJsonValue& value : cards) {
    if (!value.isObject()) {
      continue;
    }
    const QJsonObject object = value.toObject();
    QVariantMap card;
    card.insert(QStringLiteral("title"), object.value("title").toString());
    card.insert(QStringLiteral("bucket"), object.value("bucket").toString());
    const QString proposal = object.value("proposal_path").toString();
    card.insert(QStringLiteral("proposalPath"), normalizedRelativePath(proposal));
    card.insert(QStringLiteral("hasResults"), object.value("has_results").toBool(false));
    card.insert(QStringLiteral("results"), object.value("results"));
    result.push_back(card);
  }
  return result;
}

QVariantList makeReferenceLinks(const QJsonObject& references) {
  QVariantList result;
  result.reserve(references.size());
  QSet<QString> labels;

  const auto keys = references.keys();
  for (const QString& key : keys) {
    const QJsonValue value = references.value(key);
    if (!value.isString()) {
      continue;
    }
    const QString normalized = normalizedRelativePath(value.toString());
    if (normalized.isEmpty()) {
      continue;
    }
    if (labels.contains(key)) {
      continue;
    }
    QVariantMap item;
    item.insert(QStringLiteral("label"), key);
    item.insert(QStringLiteral("path"), normalized);
    result.push_back(item);
    labels.insert(key);
  }

  // Canon anchors we always expose in the dashboard shell.
  const struct {
    const char* label;
    const char* path;
  } canonAnchors[] = {
      {"VDM-AX-A0…A7", "Derivation/AXIOMS.md#vdm-ax-a0"},
      {"VDM-E-033", "Derivation/EQUATIONS.md#vdm-e-033"},
      {"VDM-E-090", "Derivation/EQUATIONS.md#vdm-e-090"},
      {"VALIDATION_METRICS", "Derivation/VALIDATION_METRICS.md#kpi-front-speed-rel-err"},
  };
  for (const auto& anchor : canonAnchors) {
    const QString label = QString::fromUtf8(anchor.label);
    if (labels.contains(label)) {
      continue;
    }
    QVariantMap item;
    item.insert(QStringLiteral("label"), label);
    item.insert(QStringLiteral("path"), QString::fromUtf8(anchor.path));
    result.push_back(item);
    labels.insert(label);
  }

  return result;
}

QString normalizedRelativePath(const QString& relativePath) {
  QString trimmed = relativePath.trimmed();
  if (trimmed.isEmpty()) {
    return QString();
  }

  QString fragment;
  const int fragmentIndex = trimmed.indexOf(QLatin1Char('#'));
  if (fragmentIndex >= 0) {
    fragment = trimmed.mid(fragmentIndex + 1).trimmed();
    trimmed = trimmed.left(fragmentIndex);
  }

  QString normalized = trimmed;
  normalized.replace(QChar::fromLatin1(static_cast<char>(0x5C)), QChar::fromLatin1('/'));
  if (normalized.startsWith(QStringLiteral("qrc:"))) {
    return QString();
  }
  if (normalized.startsWith(QStringLiteral("//"))) {
    return QString();
  }
  if (normalized.startsWith(QLatin1Char('/'))) {
    normalized.remove(0, 1);
  }
  // Prevent drive letters or scheme usage.
  if (normalized.contains(QLatin1Char(':'))) {
    return QString();
  }

  QStringList parts = normalized.split(QLatin1Char('/'), Qt::SkipEmptyParts);
  QStringList safeParts;
  for (const QString& part : parts) {
    if (part == QLatin1String(".")) {
      continue;
    }
    if (part == QLatin1String("..")) {
      if (safeParts.isEmpty()) {
        return QString();
      }
      safeParts.removeLast();
      continue;
    }
    safeParts.push_back(part);
  }

  QString safePath = safeParts.join(QLatin1Char('/'));
  if (safePath.isEmpty()) {
    return QString();
  }

  if (!fragment.isEmpty()) {
    static const QRegularExpression kFragmentPattern(QStringLiteral("^[A-Za-z0-9_.-]+$"));
    if (!kFragmentPattern.match(fragment).hasMatch()) {
      return safePath;
    }
    safePath.append(QLatin1Char('#'));
    safePath.append(fragment);
  }

  return safePath;
}

}  // namespace

DashboardController::DashboardController(QObject* parent)
  : QObject(parent) {
}

void DashboardController::reset() {
  m_pendingApprovals = 0;
  m_orphanProposals = 0;
  m_artifactsTotal = 0;
  m_repoHead.clear();
  m_totalProposals = 0;
  m_proposalsMissingResults = 0;
  m_resultsTotal = 0;
  m_codeDomainsTracked = 0;
  m_documentationBuckets = 0;
  m_updatedUtc.clear();
  m_spotlightCards.clear();
  m_referenceLinks.clear();
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

  if (root.contains("updated_utc") && root.value("updated_utc").isString()) {
    m_updatedUtc = root.value("updated_utc").toString();
  }

  // code_domains: compute pending approvals and artifact totals
  int pending = 0;
  int logs = 0;
  int figs = 0;
  int domainCount = 0;

  const QJsonValue cdVal = root.value("code_domains");
  if (cdVal.isArray()) {
    const QJsonArray codeDomains = cdVal.toArray();
    for (const QJsonValue& v : codeDomains) {
      if (!v.isObject()) continue;
      const QJsonObject cd = v.toObject();

      // approvals.allowed_tags vs approvals.approvals[tag].approved_at
      domainCount += 1;

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
  int results = 0;
  const QJsonValue psVal = root.value("proposal_status");
  if (psVal.isArray()) {
    const QJsonArray ps = psVal.toArray();
    for (const QJsonValue& v : ps) {
      if (!v.isObject()) continue;
      const QJsonObject row = v.toObject();
      const QJsonValue hasRes = row.value("has_results");
      const bool b = hasRes.isBool() ? hasRes.toBool() : false;
      if (!b) orphan += 1;
      if (b) results += 1;
    }
  }

  // summary block
  const QJsonValue summaryVal = root.value("summary");
  if (summaryVal.isObject()) {
    const QJsonObject summary = summaryVal.toObject();
    m_totalProposals = summary.value("proposals_total").toInt(m_totalProposals);
    m_proposalsMissingResults = summary.value("proposals_missing_results").toInt(m_proposalsMissingResults);
    m_resultsTotal = summary.value("results_total").toInt(m_resultsTotal);
    m_codeDomainsTracked = summary.value("code_domains").toInt(m_codeDomainsTracked);
    m_documentationBuckets = summary.value("doc_buckets").toInt(m_documentationBuckets);
  } else {
    m_totalProposals = orphan + results;
    m_proposalsMissingResults = orphan;
    m_resultsTotal = results;
    m_codeDomainsTracked = domainCount;
  }

  const QJsonValue docBucketsVal = root.value("doc_buckets");
  if (docBucketsVal.isArray()) {
    m_documentationBuckets = docBucketsVal.toArray().size();
  }

  // spotlight cards provide roadmap context for missing results.
  const QJsonValue spotlightVal = root.value("spotlight_cards");
  if (spotlightVal.isArray()) {
    m_spotlightCards = makeSpotlightCards(spotlightVal.toArray());
  }

  // references block -> canonical anchors.
  const QJsonValue referencesVal = root.value("references");
  if (referencesVal.isObject()) {
    m_referenceLinks = makeReferenceLinks(referencesVal.toObject());
  }

  m_pendingApprovals = pending;
  m_orphanProposals = orphan;
  m_artifactsTotal = logs + figs;
  return true;
}

QUrl DashboardController::repositoryUrl(const QString& relativePath) const {
  const QString rel = normalizedRelativePath(relativePath);
  if (rel.isEmpty()) {
    return QUrl();
  }

  QString fragment;
  QString relPath = rel;
  const int fragmentIndex = rel.indexOf(QLatin1Char('#'));
  if (fragmentIndex >= 0) {
    fragment = rel.mid(fragmentIndex + 1);
    relPath = rel.left(fragmentIndex);
  }

  auto candidateUrl = [&fragment, &relPath](const QString& base) -> QUrl {
    if (base.trimmed().isEmpty() || relPath.isEmpty()) {
      return QUrl();
    }
    const QDir baseDir(base);
    const QString candidate = baseDir.filePath(relPath);
    const QFileInfo info(candidate);
    if (!info.exists() || !info.isFile()) {
      return QUrl();
    }
    const QString canonicalBase = baseDir.canonicalPath();
    const QString canonicalFile = info.canonicalFilePath();
    if (canonicalBase.isEmpty() || canonicalFile.isEmpty()) {
      return QUrl();
    }
    if (!canonicalFile.startsWith(canonicalBase + QLatin1Char('/')) && canonicalFile != canonicalBase) {
      return QUrl();
    }
    QUrl url = QUrl::fromLocalFile(canonicalFile);
    if (!fragment.isEmpty()) {
      url.setFragment(fragment);
    }
    return url;
  };

  const QString envRoot = qEnvironmentVariable("VDM_REPO_ROOT");
  if (const QUrl envUrl = candidateUrl(envRoot); envUrl.isValid()) {
    return envUrl;
  }

  const QString cwd = QDir::currentPath();
  if (const QUrl cwdUrl = candidateUrl(cwd); cwdUrl.isValid()) {
    return cwdUrl;
  }

  const QString appDir = QCoreApplication::applicationDirPath();
  if (const QUrl appUrl = candidateUrl(appDir); appUrl.isValid()) {
    return appUrl;
  }

  return QUrl();
}
