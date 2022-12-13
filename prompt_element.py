from PyQt5 import QtCore, QtGui, QtWidgets
import itertools, glob, os

from main import Ui_MainWindow
import utils, image_element, description_element

class PromptContainer(QtWidgets.QFrame):

    def __init__(self, parent : QtWidgets.QWidget, prompt : QtWidgets.QWidget):
        self.parent = parent
        self.prompt = prompt
        super(PromptContainer, self).__init__(self.parent)
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setContentsMargins(0, 0, 0, 1)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        e.accept()

class PromptElement(QtWidgets.QWidget):

    idGenerator = itertools.count(1)
    currentSelected : QtWidgets.QWidget = None

    def __init__(self, mainFrame: Ui_MainWindow):
        self.mainFrame = mainFrame
        self.parent = mainFrame.NameScrollAreaContent
        self.parentLayout = mainFrame.NameScrollAreaLayout
        self.parentFrame = PromptContainer(self.parent, self)
        self.parentFrameLayout = QtWidgets.QVBoxLayout(self.parentFrame)
        self.id = next(PromptElement.idGenerator)
        self.descriptions = []

        super(PromptElement, self).__init__(self.parentFrame)

        self.setMaximumSize(QtCore.QSize(200000, 50))

        self.layout = QtWidgets.QHBoxLayout(self)
        self.entry = utils.clickableQLineEdit(self)
        self.entry.setMinimumSize(QtCore.QSize(200, 35))

        self.addButton = QtWidgets.QPushButton(self)
        self.addButton.setEnabled(True)
        self.addButton.setAutoFillBackground(False)
        self.addButton.setStyleSheet("")
        self.addButton.setText("")
        self.addButton.setDisabled(True)

        self.deleteButton = QtWidgets.QPushButton(self)
        self.deleteButton.setEnabled(True)
        self.deleteButton.setAutoFillBackground(False)
        self.deleteButton.setStyleSheet("")
        self.deleteButton.setText("")

        addIcon = QtGui.QIcon()
        addIcon.addPixmap(QtGui.QPixmap("assets/add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(addIcon)

        deleteIcon = QtGui.QIcon()
        deleteIcon.addPixmap(QtGui.QPixmap("assets/trash.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(deleteIcon)

        self.layout.addWidget(self.entry)
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.deleteButton)

        self.parentFrameLayout.addWidget(self)
        self.parentLayout.addWidget(self.parentFrame)
        self.addButton.clicked.connect(self.create_description)
        self.deleteButton.clicked.connect(self.delete_element)
        self.entry.clicked.connect(self.selectEntry)
        self.entry.returnPressed.connect(self.duplicate_element)
        self.entry.selectionChanged.connect(lambda: self.entry.setSelection(0, 0)) # disable selection

    def create_description(self):
        new = description_element.DescriptionElement(self, self.mainFrame)
        new.entry.setFocus()

    def duplicate_element(self):
        if self.entry.text():
            self.entry.setReadOnly(True)
            new = PromptElement(self.mainFrame)
            new.entry.setFocus()
            self.addButton.setEnabled(True)

    def delete_element(self):
        if utils.sendConfirmMessage("Are you sure to delete this prompt ?"):
            self.parentFrame.close()
            for img in image_element.ImageElement.allImages:
                if self in img.usedDict.keys():
                    del img.usedDict[self]
                    img.updateCaption()
                    if self == PromptElement.currentSelected: img.deselect()

            if self == PromptElement.currentSelected:
                PromptElement.currentSelected = None

    def select(self):
        self.entry.setStyleSheet("QWidget { background-color: rgb(68, 140, 203) }")
        PromptElement.currentSelected = self

    def deselect(self):
        self.entry.setStyleSheet("")

    def _deselectAllElement(self):
        if PromptElement.currentSelected: # Make sure one PromptElement is selected
            PromptElement.currentSelected.deselect()

            for desc in PromptElement.currentSelected.descriptions:
                desc.deselect()

        # deselect all images
        for img in image_element.ImageElement.getSelectedImages():  # unselet all image when changing prompt
            img.deselect()

    def selectEntry(self):
        if self.entry.isReadOnly(): # only after user created the prombt
            self._deselectAllElement()

            # select images containing the new prompt
            for img in image_element.ImageElement.allImages:
                # if self in img.usedPrompt:
                #     img.select()
                if self in img.usedDict.keys():
                    img.select()

            self.select()
