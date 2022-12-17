from PyQt5 import QtCore, QtGui, QtWidgets
from natsort import os_sorted
import os, sys, glob

import description_element
import utils
from flowlayout import FlowLayout
import prompt_element, image_element

#os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
VERSION = "0.9.1"

class CustomContainer(QtWidgets.QScrollArea):

    def __init__(self, parent, mainFrame):
        self.mainFrame = mainFrame
        self.parent = parent
        super(CustomContainer, self).__init__(self.parent)
        self.setWidgetResizable(True)
        self.setAcceptDrops(True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        e.accept()


class Ui_MainWindow(QtWidgets.QWidget):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)

        self.LeftContainer = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.LeftContainer.sizePolicy().hasHeightForWidth())
        self.LeftContainer.setSizePolicy(sizePolicy)
        self.LeftContainer.setFrameShape(QtWidgets.QFrame.Box)
        self.LeftContainer.setFrameShadow(QtWidgets.QFrame.Plain)
        self.LeftContainer.setMaximumSize(338, 50000)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.LeftContainer)

        self.ContextMenu = QtWidgets.QFrame(self.LeftContainer)
        self.ContextMenu.setFrameShape(QtWidgets.QFrame.Box)
        self.ContextMenu.setFrameShadow(QtWidgets.QFrame.Plain)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.ContextMenu)

        self.FolderBrowserFrame = QtWidgets.QFrame(self.ContextMenu)
        self.FolderBrowserFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.FolderBrowserFrame.setFrameShadow(QtWidgets.QFrame.Plain)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.FolderBrowserFrame)
        self.label = QtWidgets.QLabel(self.FolderBrowserFrame)
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.FolderBrowserFrame)
        self.lineEdit.setEnabled(False)
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.FolderBrowserFrame)
        self.pushButton.clicked.connect(self.browseImages)

        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addWidget(self.FolderBrowserFrame)

        self.SubfolderCheckbox = QtWidgets.QCheckBox(self.ContextMenu)
        self.verticalLayout_2.addWidget(self.SubfolderCheckbox)

        self.TxtCaptionCheckbox = QtWidgets.QCheckBox(self.ContextMenu)
        self.TxtCaptionCheckbox.setChecked(True)
        self.verticalLayout_2.addWidget(self.TxtCaptionCheckbox)

        self.RandomizePromptOrderCheckbox = QtWidgets.QCheckBox(self.ContextMenu)
        self.RandomizePromptOrderCheckbox.setChecked(True)
        self.verticalLayout_2.addWidget(self.RandomizePromptOrderCheckbox)

        self.SeparateByInfoLabel = QtWidgets.QLabel(self.ContextMenu)
        self.verticalLayout_2.addWidget(self.SeparateByInfoLabel)

        self.PrombtSeparatorFrame = QtWidgets.QFrame(self.ContextMenu)
        self.PrombtSeparatorFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.PrombtSeparatorFrame.setFrameShadow(QtWidgets.QFrame.Plain)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.PrombtSeparatorFrame)

        self.subjectSeparatorLabel = QtWidgets.QLabel(self.PrombtSeparatorFrame)
        self.horizontalLayout_2.addWidget(self.subjectSeparatorLabel)

        self.subjectSeparatorContent = QtWidgets.QLineEdit(self.PrombtSeparatorFrame)
        self.subjectSeparatorContent.setText("; ")
        self.horizontalLayout_2.addWidget(self.subjectSeparatorContent)


        self.descriptionSeparatorLabel = QtWidgets.QLabel(self.PrombtSeparatorFrame)
        self.horizontalLayout_2.addWidget(self.descriptionSeparatorLabel)
        self.descriptionSeparatorContent = QtWidgets.QLineEdit(self.PrombtSeparatorFrame)
        self.descriptionSeparatorContent.setText(", ")
        self.horizontalLayout_2.addWidget(self.descriptionSeparatorContent)

        # self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout_2.addWidget(self.PrombtSeparatorFrame)
        self.verticalLayout_4.addWidget(self.ContextMenu)
        spacerItem = QtWidgets.QSpacerItem(40, 70, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem)

        self.promptSearchBar = QtWidgets.QLineEdit(self.LeftContainer)
        self.verticalLayout_4.addWidget(self.promptSearchBar)
        self.promptSearchBar.textChanged.connect(self.filterPromptBySearch)
        controlF = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+F"), self.centralwidget)
        controlF.activated.connect(lambda : self.promptSearchBar.setFocus())

        self.NameContainer = CustomContainer(self.LeftContainer, self)
        self.vbar = self.NameContainer.verticalScrollBar()

        self.NameScrollAreaContent = QtWidgets.QWidget()
        self.NameScrollAreaContent.setGeometry(QtCore.QRect(0, 0, 292, 447))

        self.NameScrollAreaLayout = QtWidgets.QVBoxLayout(self.NameScrollAreaContent)
        self.NameScrollAreaLayout.setContentsMargins(0, 9, 9, 0)
        self.NameContainer.setWidget(self.NameScrollAreaContent)

        self.verticalLayout_4.addWidget(self.NameContainer)


        a = prompt_element.PromptElement(mainFrame=self)

        self.NameScrollAreaLayout.setAlignment(QtCore.Qt.AlignTop)
        self.horizontalLayout_4.addWidget(self.LeftContainer)


        self.RightContainerFrame = QtWidgets.QFrame(self.centralwidget)
        self.RightContainerFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.RightContainerFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.horizontalLayout_4.addWidget(self.RightContainerFrame)

        self.RightContainerLayout = QtWidgets.QVBoxLayout(self.RightContainerFrame)
        self.RightContainerLayout.setSpacing(0)
        self.RightContainerLayout.setContentsMargins(0, 0, 0, 0);

        self.RightContainerBottomFrame = QtWidgets.QFrame(self.RightContainerFrame)
        self.RightContainerBottomFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.RightContainerBottomFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.RightContainerLayout.addWidget(self.RightContainerBottomFrame)

        self.RightContainerBottomLayout = QtWidgets.QHBoxLayout(self.RightContainerBottomFrame)
        self.RightContainerBottomLayout.setContentsMargins(0, 0, 0, 0);

        self.RightContainerBottomSpacer = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.RightContainerBottomLayout.addItem(self.RightContainerBottomSpacer)

        self.RightContainerBottomSearchBar = QtWidgets.QLineEdit(self.RightContainerBottomFrame)
        self.RightContainerBottomSearchBar.textChanged.connect(self.filderImageBySearch)
        controlI = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+I"), self.centralwidget)
        controlI.activated.connect(lambda : self.RightContainerBottomSearchBar.setFocus())

        self.RightContainerBottomLayout.addItem(self.RightContainerBottomSpacer)
        self.RightContainerBottomLayout.addWidget(self.RightContainerBottomSearchBar)

        self.ImageContainer = QtWidgets.QScrollArea(self.RightContainerFrame)
        self.ImageContainer.setEnabled(True)
        self.ImageContainer.setAcceptDrops(False)
        self.ImageContainer.setWidgetResizable(True)
        self.ImageContainer.setStyleSheet("QWidget { background-color: rgb(112, 112, 112) }")
        self.RightContainerLayout.addWidget(self.ImageContainer)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setEnabled(True)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 773, 691))

        self.flowLayout = FlowLayout(self.scrollAreaWidgetContents)

        self.ImageContainer.setWidget(self.scrollAreaWidgetContents)

        MainWindow.setCentralWidget(self.centralwidget)

        # go to bottom
        self.NameContainer.verticalScrollBar().rangeChanged.connect(
            self.scrollToBottom,
        )

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def filderImageBySearch(self):
        text = self.RightContainerBottomSearchBar.text()
        for imageWidget in image_element.ImageElement.allImages:
            if text.lower() in imageWidget.caption.text().lower():
                imageWidget.show()
            else:
                imageWidget.hide()

    def scrollToBottom(self):
        # bad fixes for auto bottom when new prompt
        if self.NameContainer.verticalScrollBar().value() > self.NameContainer.verticalScrollBar().maximum() - 100:
            self.NameContainer.verticalScrollBar().setValue(
                self.NameContainer.verticalScrollBar().maximum()
            )

    def filterPromptBySearch(self):
        text = self.promptSearchBar.text()
        for prompt in prompt_element.PromptElement.allPrompts:
            if text.lower() in prompt.entry.text().lower():
                prompt.parentFrame.show()
            else:
                prompt.parentFrame.hide()

    def browseImages(self):
        filepath = QtWidgets.QFileDialog.getExistingDirectory(QtWidgets.QDialog(), 'Select Folder containing Images', "C:\\Users\\Raphael\\Desktop\\Caption")
        if filepath:
            self.lineEdit.setText(filepath)
            self.importImage(filepath)

    def importImage(self, folder_path):
        # Reset all static lists & all Widgets showed
        for image in image_element.ImageElement.allImages:
            image.setParent(None)
            image.deleteLater()
        image_element.ImageElement.allImages.clear()

        for root, dirs, files in os.walk(folder_path):
            for name in os_sorted(files):
                if name.endswith(('.jpg', '.png')):
                    image_element.ImageElement(os.path.join(root, name), name, mainFrame=self)
                    QtWidgets.QApplication.processEvents()
            if not self.SubfolderCheckbox.isChecked(): break

        # Import all captions [NEED REFACTOR]
        caption = [importedImages.caption.text() for importedImages in image_element.ImageElement.allImages]

        dico = {}
        newdico = {}
        for cap in caption:
            instanceList = cap.split(self.subjectSeparatorContent.text().strip())
            for instance in instanceList:
                elements = instance.split(self.descriptionSeparatorContent.text().strip())
                subjectName = elements[0].strip()
                if subjectName:
                    if not dico.get(subjectName): dico[subjectName] = []
                    descriptions = [desc.strip() for desc in elements[1:] if desc.strip() not in dico[subjectName]]
                    dico[subjectName] = dico[subjectName] + descriptions

        for subject in dico.keys():
            subjectPrompt = prompt_element.PromptElement(mainFrame=self)
            subjectPrompt.entry.setText(subject)
            subjectPrompt.entry.setReadOnly(True)
            subjectPrompt.addButton.setEnabled(True)
            newdico[subjectPrompt] = []

            for desc in dico[subject]:
                descPrompt = description_element.DescriptionElement(subjectPrompt, mainFrame=self)
                descPrompt.entry.setText(desc)
                descPrompt.entry.setReadOnly(True)
                newdico[subjectPrompt].append(descPrompt)

        for img in image_element.ImageElement.allImages:
            instanceList = img.caption.text().split(self.subjectSeparatorContent.text().strip())
            for instance in instanceList:
                elements = instance.split(self.descriptionSeparatorContent.text().strip())
                subjectName = elements[0].strip()
                if subjectName:
                    subjectElement = [subject for subject in newdico.keys() if subject.entry.text() == subjectName][0]
                    if not img.usedDict.get(subjectElement): img.usedDict[subjectElement] = []
                    descriptions = [desc.strip() for desc in elements[1:]]
                    for STRINGdesc in descriptions:
                        for x in newdico[subjectElement]:
                            if STRINGdesc == x.entry.text():
                                img.usedDict[subjectElement].append(x)
            img.updateCaption()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(f"BatchPrompter V{VERSION}")
        self.label.setText("Folder:")
        self.pushButton.setText("Browse")
        self.SubfolderCheckbox.setText("Include Subfolders")
        self.TxtCaptionCheckbox.setText("Txt Caption")
        self.RandomizePromptOrderCheckbox.setText("Randomize prompt order")
        self.SeparateByInfoLabel.setText("Separate with :")
        self.subjectSeparatorLabel.setText("Subject :")
        self.descriptionSeparatorLabel.setText("Description :")

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
