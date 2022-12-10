from PyQt5 import QtCore, QtGui, QtWidgets
import itertools, glob, os, uuid, imagesize

# Local Import
import image_element, prompt_element, utils

class DescriptionElement(QtWidgets.QWidget):

    selectedDescriptions = []

    def __init__(self, promptParent, mainFrame):
        self.promptParent = promptParent
        self.mainFrame = mainFrame
        self.parentLayout = self.promptParent.parentFrameLayout
        super(DescriptionElement, self).__init__()

        self.layout = QtWidgets.QHBoxLayout(self)

        self.horizontalSpacer = QtWidgets.QSpacerItem(40, 20)
        self.layout.addItem(self.horizontalSpacer)

        self.entry = utils.clickableQLineEdit(self)
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

        self.promptParent.descriptions.append(self)
        self.deleteButton.clicked.connect(self.delete_element)
        self.entry.returnPressed.connect(self.duplicate_element)
        self.entry.selectionChanged.connect(lambda: self.entry.setSelection(0, 0))  # disable selection
        self.entry.clicked.connect(self.selectEntry)

    def duplicate_element(self):
        if self.entry.text():
            self.entry.setReadOnly(True)
            new = DescriptionElement(self.promptParent, self.mainFrame)
            new.entry.setFocus()

    def delete_element(self):
        self.close()
        self.promptParent.descriptions.remove(self)
        for img in image_element.ImageElement.allImages:
            if self in img.usedPrompt:
                img.deselect()
                img.usedPrompt.remove(self)
                img.updateCaption()

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
