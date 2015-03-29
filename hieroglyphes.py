from xml.etree import ElementTree
from random import randrange
from PyQt4.Qt import QApplication
from PyQt4 import QtCore, QtDeclarative
import os
import sys
import subprocess

class HieroglyphCard:
    def __init__(self, meaning, transcription, symbolPath, soundPath):
        self.meaning = meaning
        self.imagePath = symbolPath
        self.soundPath = soundPath
        self.transcription = transcription

class HieroglyphesTest(QtDeclarative.QDeclarativeView):
    changeTranslate = QtCore.pyqtSignal(str)
    changeNextDescription = QtCore.pyqtSignal(str)
    updateSymbolUrl = QtCore.pyqtSignal(str)
    changeTranscription = QtCore.pyqtSignal(str)

    def __init__(self, startedWith, config='dictionary.xml'):
        QtDeclarative.QDeclarativeView.__init__(self, None)

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
        self.__playSound = False

        self.setSource(QtCore.QUrl.fromLocalFile('hieroglyphesView.qml'))
        self.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

        viewRootObject = self.rootObject()

        viewRootObject.pushNext.connect(self.onNext)
        viewRootObject.pushSound.connect(self.onSound)

        self.changeTranslate.connect(viewRootObject.updateTranslate)
        self.changeNextDescription.connect(viewRootObject.updateNextButtonText)
        self.updateSymbolUrl.connect(viewRootObject.updateSymbolImage)
        self.changeTranscription.connect(viewRootObject.updateTranscription)

        self.onNext()

    def __currentButtonText(self):
        return "[{0}/{1}] Next >".format(self.__count, self.__numberOfHieroglyphes)

    def __randomInsert__(self, lst, item):
        lst.insert(randrange(len(lst)+1), item)    

    def __changeMeaning(self):
        self.changeTranslate.emit(self.__currentCard.meaning)

    def __changeImage(self):
        self.updateSymbolUrl.emit(self.__currentCard.imagePath)

    def __changeSound(self):
        self.changeTranscription.emit(self.__currentCard.transcription)
        self.__currentSoundPath = self.__currentCard.soundPath
        self.__playSound = True

    def onNext(self):
        if self.__state == 0:
            self.__count = self.__count + 1
            self.changeNextDescription.emit(self.__currentButtonText())
            self.changeTranslate.emit('')
            self.updateSymbolUrl.emit('')
            self.changeTranscription.emit('X')
            self.__playSound = False

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
        if self.__playSound:
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
