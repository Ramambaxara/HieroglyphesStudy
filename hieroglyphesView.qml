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

    Text {
        id: translateText
        y: page.firstLineY
        x: page.tab
        font.pointSize: 20
        text: "Country"
    }

    Button {
        id: soundButton
        width: 70
        height: 30
        y: page.firstLineY
        x: page.width - page.tab - width
        onClicked: pushSound()
        text: "shuǐ"
    }

    Image {
        id: tstImg
        width: 400; height: 500
        y: 20
        anchors.horizontalCenter: page.horizontalCenter
        fillMode: Image.PreserveAspectFit

        source: "/home/ramamba/Projects/fun_with_python/study_chinese/picts/country.gif"
    }

    Button {
        id: nextButton
        anchors.bottom: page.bottom
        width: page.width
        height: 30
        onClicked: pushNext()
    }
}