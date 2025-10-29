import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: root
    property var controller

    implicitHeight: contentItem.implicitHeight
    implicitWidth: contentItem.implicitWidth

    function metricValue(v) {
        return v !== undefined ? v : 0
    }

    function metricsModel() {
        if (!controller) {
            return []
        }
        return [
            {
                title: qsTr("Pending approvals"),
                value: metricValue(controller.pendingApprovals),
                description: qsTr("Approval tags without approve_tag.py receipts")
            },
            {
                title: qsTr("Proposals missing RESULTS"),
                value: metricValue(controller.proposalsMissingResults),
                description: qsTr("Structured count sourced from nexus-roadmap-index summary")
            },
            {
                title: qsTr("Harvested artifacts"),
                value: metricValue(controller.artifactsTotal),
                description: qsTr("Total logs + figures discovered via io_paths guardrails")
            },
            {
                title: qsTr("Results catalogued"),
                value: metricValue(controller.resultsTotal),
                description: qsTr("RESULTS bundles tracked in roadmap manifest")
            },
            {
                title: qsTr("Proposals indexed"),
                value: metricValue(controller.totalProposals),
                description: qsTr("Roadmap proposals discovered across canon domains")
            },
            {
                title: qsTr("Code domains tracked"),
                value: metricValue(controller.codeDomainsTracked),
                description: qsTr("Physics domains mapped in nexus-roadmap-index summary")
            },
            {
                title: qsTr("Documentation buckets"),
                value: metricValue(controller.documentationBuckets),
                description: qsTr("Canonical doc buckets enumerated for quick navigation")
            }
        ]
    }

    ColumnLayout {
        id: contentItem
        anchors.fill: parent
        spacing: 16

        GridLayout {
            id: metricsGrid
            columns: root.width > 840 ? 3 : (root.width > 540 ? 2 : 1)
            columnSpacing: 16
            rowSpacing: 16
            Layout.fillWidth: true

            Repeater {
                model: metricsModel()
                delegate: MetricCard {
                    title: modelData.title
                    value: modelData.value
                    description: modelData.description
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: "#1F1F24"
        }

        Text {
            text: qsTr("Data source: VDM_Nexus/reports/nexus-roadmap-index.v1.json (read-only)")
            color: "#8E94A4"
            font.pixelSize: 14
            wrapMode: Text.WordWrap
        }
    }

    component MetricCard: Rectangle {
        property string title: ""
        property int value: 0
        property string description: ""

        color: "#1C1E24"
        radius: 12
        Layout.fillWidth: true
        implicitHeight: 140

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: 8

            Text {
                text: title
                color: "#9DA3B4"
                font.pixelSize: 16
                font.capitalization: Font.AllUppercase
            }

            Text {
                text: Number(value).toLocaleString(Qt.locale())
                color: "#F3F4F6"
                font.pixelSize: 42
                font.bold: true
            }

            Text {
                text: description
                color: "#B0B3B8"
                font.pixelSize: 14
                wrapMode: Text.WordWrap
            }
        }
    }
}
