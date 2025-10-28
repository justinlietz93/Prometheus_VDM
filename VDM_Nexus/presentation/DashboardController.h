#pragma once

#include <QObject>
#include <QString>

class DashboardController : public QObject {
  Q_OBJECT
  Q_PROPERTY(int pendingApprovals READ pendingApprovals NOTIFY changed)
  Q_PROPERTY(int orphanProposals READ orphanProposals NOTIFY changed)
  Q_PROPERTY(int artifactsTotal READ artifactsTotal NOTIFY changed)
  Q_PROPERTY(QString repoHead READ repoHead NOTIFY changed)
public:
  explicit DashboardController(QObject* parent=nullptr);

  Q_INVOKABLE bool loadIndex(const QString& path);
  Q_INVOKABLE QString defaultIndexPath() const;

  int pendingApprovals() const { return m_pendingApprovals; }
  int orphanProposals() const { return m_orphanProposals; }
  int artifactsTotal() const { return m_artifactsTotal; }
  QString repoHead() const { return m_repoHead; }

signals:
  void changed();

private:
  void reset();
  bool computeFromJson(const QByteArray& data);

  int m_pendingApprovals{0};
  int m_orphanProposals{0};
  int m_artifactsTotal{0};
  QString m_repoHead;
};