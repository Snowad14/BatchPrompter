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
    allPrompts = []
    currentSelected : QtWidgets.QWidget = None

    def __init__(self, mainFrame: Ui_MainWindow):
        self.mainFrame = mainFrame
        self.parent = mainFrame.NameScrollAreaContent
        self.parentLayout = mainFrame.NameScrollAreaLayout
        self.parentFrame = PromptContainer(self.parent, self)
        self.parentFrameLayout = QtWidgets.QVBoxLayout(self.parentFrame)
        self.id = next(PromptElement.idGenerator)
        PromptElement.allPrompts.append(self)
        self.descriptions = []
        self.isCollapsed = False

        super(PromptElement, self).__init__(self.parentFrame)

        self.setMaximumSize(QtCore.QSize(200000, 50))

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(1)

        self.collapseButton = QtWidgets.QPushButton(self)
        self.collapseButton.setEnabled(True)
        self.collapseButton.setAutoFillBackground(False)
        self.collapseButton.setStyleSheet("")
        self.collapseButton.setText("")
        self.collapseButton.hide()

        collapseIcon = QtGui.QIcon()
        pixmap = QtGui.QPixmap("assets/triangle.svg")
        collapseIcon.addPixmap(pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.collapseButton.setIcon(collapseIcon)
        self.collapseButton.setStyleSheet("background: transparent;")

        self.entry = utils.clickableQLineEdit(self)
        self.entry.setMinimumSize(QtCore.QSize(150, 35))

        self.addButton = QtWidgets.QPushButton(self)
        self.addButton.setEnabled(True)
        self.addButton.setAutoFillBackground(False)
        self.addButton.setStyleSheet("")
        self.addButton.setText("")
        self.addButton.setDisabled(True)

        addIcon = QtGui.QIcon()
        addIcon.addPixmap(QtGui.QPixmap("assets/add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(addIcon)

        self.deleteButton = QtWidgets.QPushButton(self)
        self.deleteButton.setEnabled(True)
        self.deleteButton.setAutoFillBackground(False)
        self.deleteButton.setStyleSheet("")
        self.deleteButton.setText("")

        deleteIcon = QtGui.QIcon()
        deleteIcon.addPixmap(QtGui.QPixmap("assets/trash.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(deleteIcon)

        self.layout.addWidget(self.collapseButton)
        self.layout.addWidget(self.entry)
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.deleteButton)


        self.parentFrameLayout.addWidget(self)
        self.parentLayout.addWidget(self.parentFrame)
        self.addButton.clicked.connect(self.create_description)
        self.deleteButton.clicked.connect(self.delete_element)
        self.collapseButton.clicked.connect(self.collapsePrompt)
        self.entry.clicked.connect(self.selectEntry)
        self.entry.returnPressed.connect(self.duplicate_element)
        self.entry.selectionChanged.connect(lambda: self.entry.setSelection(0, 0)) # disable selection

    def collapsePrompt(self):
        collapseIcon = QtGui.QIcon()
        pixmap = QtGui.QPixmap("assets/triangle.svg")
        if self.isCollapsed:
            self.isCollapsed = False
            for desc in self.descriptions:
                desc.show()
        else:
            pixmap = pixmap.transformed(QtGui.QTransform().rotate(270))
            self.isCollapsed = True
            for desc in self.descriptions:
                desc.hide()

        collapseIcon.addPixmap(pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.collapseButton.setIcon(collapseIcon)

    def getNonEmptyDescriptions(self):
        return [i for i in self.descriptions if i.entry.text() != ""]

    def addDescriptionElement(self, element):
        self.descriptions.append(element)
        if len(self.descriptions) > 0: self.collapseButton.show()

    def removeDescriptionElement(self, element):
        self.descriptions.remove(element)
        if len(self.descriptions) <= 0: self.collapseButton.hide()

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
        concernedImg = [img for img in image_element.ImageElement.allImages if self in img.usedDict.keys()]
        if utils.sendConfirmMessage(f"Are you sure you want to delete this prompt from {len(concernedImg)} images?"):
            self.parentFrame.close()
            for img in concernedImg:
                del img.usedDict[self]
                img.updateCaption()
                if self == PromptElement.currentSelected: img.deselect()
                description_element.DescriptionElement.selectedDescriptions.clear()

            PromptElement.allPrompts.remove(self)
            if self == PromptElement.currentSelected:
                PromptElement.currentSelected = None


    def select(self):
        self.entry.setStyleSheet("QWidget { background-color: rgb(68, 140, 203) }")
        PromptElement.currentSelected = self

    def deselect(self):
        self.entry.setStyleSheet("")

    def deselectAllElement(self):
        if PromptElement.currentSelected: # Make sure one PromptElement is selected
            PromptElement.currentSelected.deselect()

            for desc in PromptElement.currentSelected.descriptions:
                desc.deselect()

        # deselect all images
        for img in image_element.ImageElement.getSelectedImages():  # unselet all image when changing prompt
            img.deselect()

    def selectAllChildImages(self):
        for img in image_element.ImageElement.allImages:
            if self in img.usedDict.keys():
                img.select()

    def selectEntry(self):
        if self.entry.isReadOnly(): # only after user created the prombt
            self.deselectAllElement()

            # select images containing the new prompt
            self.selectAllChildImages()

            self.select()
