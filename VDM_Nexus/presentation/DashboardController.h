#pragma once

#include <QObject>
#include <QString>
#include <QUrl>
#include <QVariantList>

class DashboardController : public QObject {
  Q_OBJECT
  Q_PROPERTY(int pendingApprovals READ pendingApprovals NOTIFY changed)
  Q_PROPERTY(int orphanProposals READ orphanProposals NOTIFY changed)
  Q_PROPERTY(int artifactsTotal READ artifactsTotal NOTIFY changed)
  Q_PROPERTY(QString repoHead READ repoHead NOTIFY changed)
  Q_PROPERTY(int totalProposals READ totalProposals NOTIFY changed)
  Q_PROPERTY(int proposalsMissingResults READ proposalsMissingResults NOTIFY changed)
  Q_PROPERTY(int resultsTotal READ resultsTotal NOTIFY changed)
  Q_PROPERTY(int codeDomainsTracked READ codeDomainsTracked NOTIFY changed)
  Q_PROPERTY(int documentationBuckets READ documentationBuckets NOTIFY changed)
  Q_PROPERTY(QString updatedTimestamp READ updatedTimestamp NOTIFY changed)
  Q_PROPERTY(QVariantList spotlightCards READ spotlightCards NOTIFY changed)
  Q_PROPERTY(QVariantList referenceLinks READ referenceLinks NOTIFY changed)
public:
  explicit DashboardController(QObject* parent=nullptr);

  Q_INVOKABLE bool loadIndex(const QString& path);
  Q_INVOKABLE QString defaultIndexPath() const;
  Q_INVOKABLE QUrl repositoryUrl(const QString& relativePath) const;

  int pendingApprovals() const { return m_pendingApprovals; }
  int orphanProposals() const { return m_orphanProposals; }
  int artifactsTotal() const { return m_artifactsTotal; }
  QString repoHead() const { return m_repoHead; }
  int totalProposals() const { return m_totalProposals; }
  int proposalsMissingResults() const { return m_proposalsMissingResults; }
  int resultsTotal() const { return m_resultsTotal; }
  int codeDomainsTracked() const { return m_codeDomainsTracked; }
  int documentationBuckets() const { return m_documentationBuckets; }
  QString updatedTimestamp() const { return m_updatedUtc; }
  QVariantList spotlightCards() const { return m_spotlightCards; }
  QVariantList referenceLinks() const { return m_referenceLinks; }

signals:
  void changed();

private:
  void reset();
  bool computeFromJson(const QByteArray& data);

  int m_pendingApprovals{0};
  int m_orphanProposals{0};
  int m_artifactsTotal{0};
  QString m_repoHead;
  int m_totalProposals{0};
  int m_proposalsMissingResults{0};
  int m_resultsTotal{0};
  int m_codeDomainsTracked{0};
  int m_documentationBuckets{0};
  QString m_updatedUtc;
  QVariantList m_spotlightCards;
  QVariantList m_referenceLinks;
};
