import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    visible: true
    width: 960
    height: 600
    title: "VDM Nexus — Dashboard Preview"
    color: "#111318"

    function openRepoPath(path) {
        if (!dashboardController || !path) {
            return;
        }
        const url = dashboardController.repositoryUrl(path);
        if (url && url.isValid() && url.toString().length > 0) {
            Qt.openUrlExternally(url);
        }
    }

    background: Rectangle {
        color: root.color
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 32
        spacing: 24

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 4

            Text {
                text: qsTr("VDM Nexus Dashboard Snapshot")
                color: "#E4E6EB"
                font.pixelSize: 28
                font.bold: true
                Layout.alignment: Qt.AlignLeft
            }

            Text {
                text: qsTr("Repository head: %1").arg(dashboardController && dashboardController.repoHead.length > 0
                                                      ? dashboardController.repoHead
                                                      : qsTr("—"))
                color: "#B0B3B8"
                font.pixelSize: 16
                Layout.alignment: Qt.AlignLeft
                wrapMode: Text.WrapAnywhere
                font.family: "Source Code Pro"
            }

            Text {
                text: qsTr("Updated: %1 UTC").arg(dashboardController && dashboardController.updatedTimestamp.length > 0
                                                 ? dashboardController.updatedTimestamp
                                                 : qsTr("—"))
                color: "#7C8699"
                font.pixelSize: 14
                Layout.alignment: Qt.AlignLeft
            }
        }

        DashboardMetrics {
            Layout.fillWidth: true
            Layout.fillHeight: true
            controller: dashboardController
        }

        Rectangle {
            Layout.fillWidth: true
            color: "#1F1F24"
            height: 1
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 12
            visible: dashboardController && dashboardController.spotlightCards.length > 0

            Text {
                text: qsTr("Spotlight — proposals awaiting RESULTS bundles")
                color: "#E4E6EB"
                font.pixelSize: 20
                font.bold: true
            }

            Repeater {
                model: dashboardController ? dashboardController.spotlightCards : []
                delegate: Rectangle {
                    color: "#1C1E24"
                    radius: 10
                    Layout.fillWidth: true
                    implicitHeight: 96

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 16
                        spacing: 6

                        Text {
                            text: modelData.title
                            color: "#F3F4F6"
                            font.pixelSize: 18
                            font.bold: true
                            wrapMode: Text.WordWrap
                        }

                        Text {
                            text: qsTr("Domain bucket: %1").arg(modelData.bucket)
                            color: "#9DA3B4"
                            font.pixelSize: 14
                            wrapMode: Text.WordWrap
                        }

                        Text {
                            text: modelData.hasResults ? qsTr("Results present") : qsTr("Results pending — reference VALIDATION_METRICS gates")
                            color: modelData.hasResults ? "#7BD88F" : "#F0AD4E"
                            font.pixelSize: 14
                        }
                    }

                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: openRepoPath(modelData.proposalPath)
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            color: "#1F1F24"
            height: 1
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 8

            Text {
                text: qsTr("Canonical references")
                color: "#E4E6EB"
                font.pixelSize: 18
                font.bold: true
            }

            Flow {
                Layout.fillWidth: true
                spacing: 8

                Repeater {
                    model: dashboardController ? dashboardController.referenceLinks : []
                    delegate: Rectangle {
                        radius: 14
                        color: "#262A33"
                        implicitHeight: 32
                        implicitWidth: Math.max(120, referenceLabel.implicitWidth + 24)

                        Text {
                            id: referenceLabel
                            anchors.centerIn: parent
                            text: modelData.label
                            color: "#9DC5FF"
                            font.pixelSize: 14
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: openRepoPath(modelData.path)
                        }
                    }
                }
            }
        }
    }
}
