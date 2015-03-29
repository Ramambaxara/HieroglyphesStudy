import QtQuick 1.1
import QtDesktop 0.1

Rectangle {
    signal pushNext
    signal pushSound

    function updateTranslate(text) {
        translateText.text = text
    }

    function updateNextButtonText(text) {
        nextButton.text = text
    }

    function updateSymbolImage(imageUrl) {
        tstImg.source = imageUrl
    }

    function updateTranscription(text) {
        soundButton.text = text
    }

    id: page
    width: 500; height: 540
    color: "lightgreen"

    property variant firstLineY: 10
    property variant tab: 10 

    Keys.onPressed: {
        if (event.key == Qt.Key_S) {
            soundButton.clicked()
        }

        if (event.key == Qt.Key_N) {
            nextButton.clicked()
        }
    }
    Keys.onSpacePressed: nextButton.clicked()
    focus: true

    Text {
        id: translateText
        y: page.firstLineY
        x: page.tab
        font.pointSize: 20
    }

    Button {
        id: soundButton
        width: 70
        height: 30
        y: page.firstLineY
        x: page.width - page.tab - width
        onClicked: pushSound()
    }

    Image {
        id: tstImg
        width: 300; height: 400
        y: 60
        anchors.horizontalCenter: page.horizontalCenter
        fillMode: Image.PreserveAspectFit
    }

    Button {
        id: nextButton
        anchors.bottom: page.bottom
        width: page.width
        height: 30
        onClicked: pushNext()
    }
}