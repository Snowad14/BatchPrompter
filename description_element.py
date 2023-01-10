from PyQt5 import QtCore, QtGui, QtWidgets
import itertools, glob, os, uuid, imagesize

# Local Import
import image_element, prompt_element, QPromptLine

class DescriptionElement(QtWidgets.QWidget):

    selectedDescriptions = []

    def __init__(self, promptParent, mainFrame):
        self.promptParent = promptParent
        self.mainFrame = mainFrame
        self.parentLayout = self.promptParent.parentFrameLayout
        self.parentFrame = self.promptParent.parentFrame
        self.isEditing = False
        super(DescriptionElement, self).__init__()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 5, 0, 0)

        self.horizontalSpacer = QtWidgets.QSpacerItem(40, 20)
        self.layout.addItem(self.horizontalSpacer)

        self.entry = QPromptLine.QPromptLine(self)
        self.entry.setMinimumSize(QtCore.QSize(200, 35))

        self.deleteButton = QtWidgets.QPushButton(self)
        self.deleteButton.setEnabled(True)
        self.deleteButton.setAutoFillBackground(False)
        self.deleteButton.setStyleSheet("")
        self.deleteButton.setText("")

        deleteIcon = QtGui.QIcon()
        deleteIcon.addPixmap(QtGui.QPixmap("assets/trash.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(deleteIcon)

        self.layout.addWidget(self.entry)
        self.layout.addWidget(self.deleteButton)

        self.parentLayout.addWidget(self)
        self.promptParent.parentFrameLayout.addWidget(self)

        self.promptParent.addDescriptionElement(self)
        self.deleteButton.clicked.connect(self.delete_element)
        self.entry.returnPressed.connect(self.duplicate_element)
        self.entry.selectionChanged.connect(lambda: self.entry.setSelection(0, 0))  # disable selection
        self.entry.clicked.connect(self.selectEntry)

    def isUniqueElement(self):
        if [desc.entry.text() for desc in self.promptParent.descriptions].count(self.entry.text()) > 1:
            return False
        return True

    def updateAllChildImages(self): # TODO: Use a class whose description element and prompt element go to avoid these repetitions
        for imageWidget in image_element.ImageElement.allImages:
            if self.promptParent in imageWidget.usedDict.keys():  # Not mandatory but allows to go a little bit faster
                if self in imageWidget.usedDict[self.promptParent]:
                    imageWidget.updateCaption()

    def duplicate_element(self):
        if self.entry.text() and self.isUniqueElement():
            self.entry.setReadOnly(True)
            self.updateAllChildImages()
            if not self.isEditing:
                new = DescriptionElement(self.promptParent, self.mainFrame)
                new.entry.setFocus()
            self.isEditing = False

    def delete_element(self):
        self.close()
        self.promptParent.removeDescriptionElement(self)
        for img in image_element.ImageElement.allImages:
            if img.usedDict.get(self.promptParent) and self in img.usedDict[self.promptParent]:
                img.usedDict[self.promptParent].remove(self)
                img.deselect()
                img.updateCaption()
        self.deselect()

    def select(self):
        self.entry.setStyleSheet("QWidget { background-color: rgb(68, 140, 203) }")
        DescriptionElement.selectedDescriptions.append(self)

    def deselect(self):
        self.entry.setStyleSheet("")
        if self in DescriptionElement.selectedDescriptions:
            DescriptionElement.selectedDescriptions.remove(self)

    def selectEntry(self):
        if self.entry.isReadOnly(): # only after user created the prombt

            if self.promptParent == prompt_element.PromptElement.currentSelected:
                if self in DescriptionElement.selectedDescriptions:
                    self.deselect()
                else:
                    self.select()
            else:
                if prompt_element.PromptElement.currentSelected: prompt_element.PromptElement.currentSelected.deselectAllElement()
                prompt_element.PromptElement.currentSelected = self.promptParent
                prompt_element.PromptElement.currentSelected.selectAllChildImages()
                self.promptParent.select()
                self.select()

            for img in image_element.ImageElement.getSelectedImages():
                img.updateBackground()


