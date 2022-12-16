from PyQt5 import QtCore, QtGui, QtWidgets
import itertools, glob, os, uuid, imagesize, copy, random

# Local Imports
import utils, prompt_element, description_element

class ImageElement(QtWidgets.QWidget):
    idGenerator = itertools.count(1)
    allImages = []

    def __init__(self, image, name, mainFrame):
        super(ImageElement, self).__init__(mainFrame.scrollAreaWidgetContents)
        self.path = image
        self.parentFolder = os.path.dirname(self.path)
        self.name = name
        self.mainFrame = mainFrame
        self.allImages.append(self)
        self.id = next(ImageElement.idGenerator)
        self.nameid = f"Image-{id}"
        self.setObjectName(self.nameid)
        self.isSelected = False
        self.usedDict = {}
        self.setEnabled(True)
        width, height = imagesize.get(self.path)
        if width - height <= 50:  # choose if image render as rectangle or squarre
            self.dimensions = QtCore.QSize(200, 200)
        else:
            self.dimensions = QtCore.QSize(300, 200)
        self.setMinimumSize(self.dimensions)
        self.setMaximumSize(self.dimensions)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.Image = QtWidgets.QLabel(self)
        self.Image.setText("")
        self.Image.setPixmap(QtGui.QPixmap(image).scaled(self.dimensions.width() * 2, self.dimensions.height() * 2))
        self.Image.setScaledContents(True)
        self.layout.addWidget(self.Image)
        self.caption = QtWidgets.QLabel(self)
        self.caption.setWordWrap(True)
        self.caption.setText("")
        self.caption.setText(self.readCaption()) # Import
        self.layout.addWidget(self.caption)

        mainFrame.flowLayout.addWidget(self)

    @staticmethod
    def getSelectedImages():
        return [img for img in ImageElement.allImages if img.isSelected]

    def updateCaption(self):
        name = self._dict2Caption()
        self.caption.setText(name)
        self.saveImageToCaption()

    def readCaption(self):
        if self.mainFrame.TxtCaptionCheckbox.isChecked():
            onlyName = os.path.splitext(self.path)[0]
            if os.path.exists(onlyName + ".txt"):
                with open(onlyName + ".txt", "r") as f:
                    return f.read()
        else:
            return os.path.splitext(self.path)[0].split("_")[0]

    def _dict2Caption(self):
        subjectList = []
        for i in self.usedDict.items():
            a = [element.entry.text() for element in [i[0]] + i[1]] # Get all subject & desc in one list
            subjectList.append(self.mainFrame.descriptionSeparatorContent.text().join(a))
        name = self.mainFrame.subjectSeparatorContent.text().join(subjectList)
        return name

    def _getRandomPromptOrder(self):
        subjectList = []
        for key, value in self.usedDict.items():
            key, value = (key.entry.text(), [i.entry.text() for i in value])
            if not value:
                subjectList.append(key)
                continue
            random.shuffle(value)
            value.insert(0, key)
            subjectList.append(self.mainFrame.descriptionSeparatorContent.text().join(value))
        random.shuffle(subjectList)
        return self.mainFrame.subjectSeparatorContent.text().join(subjectList)

    def saveImageToCaption(self):
        captionString = self._getRandomPromptOrder() if self.mainFrame.RandomizePromptOrderCheckbox.isChecked() else self.caption.text()
        if self.mainFrame.TxtCaptionCheckbox.isChecked():
            onlyName = os.path.splitext(self.path)[0]
            with open(onlyName + ".txt", "w") as f:
                print(self._getRandomPromptOrder())
                f.write(captionString)
        else:
            dest_path = self.parentFolder + f"/{captionString}_{self.id}{str(uuid.uuid4())[0:3]}.png"
            os.rename(self.path, dest_path)
            self.path = dest_path

    # Remplement paintEvent on custom QWidget
    def paintEvent(self, pe):
        o = QtWidgets.QStyleOption()
        o.initFrom(self)
        p = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PrimitiveElement.PE_Widget, o, p, self)
        # p.end()
        # del p

    def select(self):
        self.setStyleSheet("QWidget { background-color: rgb(255, 69, 69) }")
        self.isSelected = True

    def deselect(self):
        self.isSelected = False
        self.setStyleSheet("")

    def _removeAllElements(self):
        self.usedDict[prompt_element.PromptElement.currentSelected] = description_element.DescriptionElement.selectedDescriptions
        del self.usedDict[prompt_element.PromptElement.currentSelected]

    def _addSelectedElements(self):
        self.usedDict[prompt_element.PromptElement.currentSelected] = [*description_element.DescriptionElement.selectedDescriptions]

    def _hasAllSelectedPrompt(self):
        for desc in description_element.DescriptionElement.selectedDescriptions:
            if desc not in self.usedDict.values():
                return False
        return True


    def mousePressEvent(self, QMouseEvent):

        if prompt_element.PromptElement.currentSelected: # make sur user has selected a prombt
            # Check if prompt has change and update or deselect image depending on whether the image already had all the prompts
            if self.isSelected and self.usedDict.get(prompt_element.PromptElement.currentSelected) != description_element.DescriptionElement.selectedDescriptions:
                self._removeAllElements()
                self._addSelectedElements()
            elif self.isSelected:
                self.deselect()
                self._removeAllElements()
            else:
                self.select()
                self._addSelectedElements()

            self.updateCaption()
            print(self.usedDict)
        else:
            utils.sendErrorMessage("You must selected a Prompt")

