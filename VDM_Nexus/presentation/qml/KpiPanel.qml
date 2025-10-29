import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root
    property var controller

    implicitHeight: content.implicitHeight
    implicitWidth: content.implicitWidth

    ColumnLayout {
        id: content
        anchors.fill: parent
        spacing: 12

        Text {
            text: qsTr("KPI Summary")
            color: "#E4E6EB"
            font.pixelSize: 20
            font.bold: true
            visible: controller && controller.kpiCards.length > 0
        }

        GridLayout {
            columns: root.width > 840 ? 3 : (root.width > 540 ? 2 : 1)
            columnSpacing: 16
            rowSpacing: 16
            Layout.fillWidth: true
            visible: controller && controller.kpiCards.length > 0

            Repeater {
                model: controller ? controller.kpiCards : []
                delegate: Rectangle {
                    radius: 12
                    color: modelData.pass ? "#14271C" : "#2A1B1B"
                    border.width: 1
                    border.color: modelData.pass ? "#2D7D46" : "#A64E4E"
                    implicitHeight: 140
                    Layout.fillWidth: true

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 16
                        spacing: 8

                        Text { text: modelData.label; color: "#B0B3B8"; font.pixelSize: 16 }
                        Text {
                            text: modelData.pass ? qsTr("PASS") : qsTr("FAIL")
                            color: modelData.pass ? "#7BD88F" : "#FF8080"
                            font.pixelSize: 26
                            font.bold: true
                        }
                        Text {
                            text: qsTr("%1 %2 %3").arg(Number(modelData.value).toLocaleString(Qt.locale()))
                                                  .arg(modelData.comparator)
                                                  .arg(Number(modelData.threshold).toLocaleString(Qt.locale()))
                            color: "#E4E6EB"
                            font.pixelSize: 14
                        }
                        Text {
                            text: qsTr("Definition: %1").arg(modelData.definitionPath)
                            color: "#9DC5FF"
                            font.pixelSize: 13
                        }
                    }
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: root.Window.window && root.Window.window.openRepoPath(modelData.definitionPath)
                    }
                }
            }
        }

        // Canon provenance panel
        ColumnLayout {
            spacing: 6
            visible: controller && controller.canonProvenance.length > 0

            Text { text: qsTr("Canon provenance"); color: "#E4E6EB"; font.pixelSize: 18; font.bold: true }

            Repeater {
                model: controller ? controller.canonProvenance : []
                delegate: RowLayout {
                    spacing: 12
                    Layout.fillWidth: true
                    Rectangle { width: 8; height: 8; radius: 4; color: "#6C7280" }
                    Text { text: modelData.label; color: "#B0B3B8"; font.pixelSize: 14 }
                    Text { text: qsTr("last commit: %1").arg(modelData.lastCommit); color: "#8E94A4"; font.pixelSize: 13; font.family: "Source Code Pro" }
                }
            }
        }
    }
}
