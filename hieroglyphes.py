from xml.etree import ElementTree
from random import randrange
from PyQt4.Qt import QApplication, QWidget, QLabel, QPushButton, QMessageBox
from PyQt4.QtGui import QPixmap, QGridLayout
from PyQt4 import QtCore
import os
import sys

class HieroglyphCard:
    def __init__(self, meaning, path):
        self.__meaning = meaning
        self.__imagePath = path

    def getHieroglyphImage(self):
        return QPixmap(self.__imagePath)

    def getMeaning(self):
        return self.__meaning
    
class HieroglyphesTest(QWidget):
    def __init__(self, showPictFirst, config='dictionary.xml'):
        super(HieroglyphesTest, self).__init__(None)

        location = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)) )
        tree = ElementTree.parse(location + '/' + config)
        root = tree.getroot()
        dirPathImg = root.find('folder').get('path') + '/'
        root = root.find('hieroglyphes')

        self.__state = 0
        self.__doFirst = self.__changeMeaning;
        self.__doSecond = self.__changeImage;

        if showPictFirst == True:
            self.__doFirst = self.__changeImage
            self.__doSecond = self.__changeMeaning

        self.__showPict = showPictFirst
        self.__dictionary = list()

        for ideogram in root.iter('ideogram'):
            self.__randomInsert__( self.__dictionary, HieroglyphCard(ideogram.get('meaning'), dirPathImg + ideogram.get('fileName')) )          

        self.__count = 0;
        self.__numberOfHieroglyphes = len(self.__dictionary)
        self.__currentCard = self.__dictionary.pop()

        self.__imageLabel = QLabel()
        self.__imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        self.__meaningLabel = QLabel()

        self.__nextButton = QPushButton(self.__currentButtonText())
        self.__nextButton.clicked.connect(self.onNext)

        layout = QGridLayout()
        layout.addWidget(self.__meaningLabel, 0, 1, alignment = QtCore.Qt.AlignTop)
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

    def onNext(self):
        if self.__state == 0:
            self.__count = self.__count + 1
            self.__nextButton.setText(self.__currentButtonText())
            self.__meaningLabel.clear()
            self.__imageLabel.clear()

            self.__doFirst()
        
        else:
            self.__doSecond()
            if len(self.__dictionary) > 0:
                self.__currentCard = self.__dictionary.pop()
            else:
                return

        self.__state = (self.__state + 1)%2

if __name__ == '__main__': 
    app = QApplication(sys.argv)

    pictFirst = False

    if len(sys.argv) > 1:
        pictFirst = (sys.argv[1] == 'meaning')
        
    screen = HieroglyphesTest(pictFirst)
    screen.show()

    sys.exit(app.exec_())
