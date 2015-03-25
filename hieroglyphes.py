from xml.etree import ElementTree
from random import randrange
from PyQt4.Qt import QApplication, QWidget, QLabel, QPushButton, QMessageBox
from PyQt4.QtGui import QPixmap, QGridLayout
from PyQt4 import QtCore
import os
import sys
import subprocess

class HieroglyphCard:
    def __init__(self, meaning, transcription, symbolPath, soundPath):
        self.__meaning = meaning
        self.__imagePath = symbolPath
        self.__soundPath = soundPath
        self.__transcription = transcription


    def getHieroglyphImage(self):
        return QPixmap(self.__imagePath)

    def getMeaning(self):
        return self.__meaning
    
    def getTranscription(self):
        return self.__transcription

    def getSoundPath(self):
        return self.__soundPath

class HieroglyphesTest(QWidget):
    def __init__(self, startedWith, config='dictionary.xml'):
        super(HieroglyphesTest, self).__init__(None)

        location = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)) )
        tree = ElementTree.parse(location + '/' + config)
        root = tree.getroot()
        folderTag = root.find('folder')
        dirPathImg = folderTag.get('symbolsPath') + '/'
        dirPathSounds = folderTag.get('soundsPath') + '/'
        root = root.find('hieroglyphes')

        self.__state = 0
        self.__doFirst = self.__changeMeaning;
        self.__doSecond = self.__changeImage;
        self.__doThird = self.__changeSound;

        if startedWith == 'image':
            self.__doFirst, self.__doSecond = self.__doSecond, self.__doFirst

        if startedWith == 'sound':
            self.__doFirst, self.__doThird = self.__doThird, self.__doFirst
        self.__dictionary = list()

        for ideogram in root.iter('ideogram'):
            self.__randomInsert__( self.__dictionary, HieroglyphCard(ideogram.get('meaning'), \
                                                                     ideogram.get('transcription'), \
                                                                     dirPathImg + ideogram.get('symbolFile'), \
                                                                     dirPathSounds + ideogram.get('soundFile')) )          

        self.__count = 0;
        self.__numberOfHieroglyphes = len(self.__dictionary)
        self.__currentCard = self.__dictionary.pop()

        self.__imageLabel = QLabel()
        self.__imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        self.__meaningLabel = QLabel()

        self.__soundButton = QPushButton('X')
        self.__soundButton.clicked.connect(self.onSound)

        self.__nextButton = QPushButton(self.__currentButtonText())
        self.__nextButton.clicked.connect(self.onNext)

        layout = QGridLayout()
        topMostLayout = QGridLayout()

        topMostLayout.addWidget(self.__meaningLabel, 0, 1, alignment = QtCore.Qt.AlignLeft)
        topMostLayout.addWidget(self.__soundButton, 0, 2, alignment = QtCore.Qt.AlignRight)
        layout.addLayout(topMostLayout, 0, 1, alignment = QtCore.Qt.AlignTop)
        layout.addWidget(self.__imageLabel, 1, 1, alignment = QtCore.Qt.AlignVCenter)
        layout.addWidget(self.__nextButton, 2, 1, alignment = QtCore.Qt.AlignBottom)

        self.setLayout(layout)
        self.resize(500, 400)

    def __currentButtonText(self):
        return "[{0}/{1}] Next >".format(self.__count, self.__numberOfHieroglyphes)

    def __randomInsert__(self, lst, item):
        lst.insert(randrange(len(lst)+1), item)    

    def __changeMeaning(self):
        self.__meaningLabel.setText(self.__currentCard.getMeaning())

    def __changeImage(self):
        self.__imageLabel.setPixmap(self.__currentCard.getHieroglyphImage())

    def __changeSound(self):
        self.__soundButton.setText(self.__currentCard.getTranscription())
        self.__currentSoundPath = self.__currentCard.getSoundPath()

    def onNext(self):
        if self.__state == 0:
            self.__count = self.__count + 1
            self.__nextButton.setText(self.__currentButtonText())
            self.__meaningLabel.clear()
            self.__imageLabel.clear()
            self.__soundButton.setText('X')

            self.__doFirst()
        
        else:
            self.__doSecond()
            self.__doThird()
            if len(self.__dictionary) > 0:
                self.__currentCard = self.__dictionary.pop()
            else:
                return

        self.__state = (self.__state + 1)%2

    def onSound(self):
        if self.__soundButton.text() != 'X':
            subprocess.call(["aplay", self.__currentSoundPath])

if __name__ == '__main__': 
    app = QApplication(sys.argv)

    if len(sys.argv) > 1:
        startedWith = sys.argv[1]
    else:
        startedWith = 'meaning'
        
    screen = HieroglyphesTest(startedWith)
    screen.show()

    sys.exit(app.exec_())
