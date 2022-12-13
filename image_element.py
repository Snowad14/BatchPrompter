from PyQt5 import QtCore, QtGui, QtWidgets
import itertools, glob, os, uuid, imagesize, copy

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
        self.isSelected = False
        self.usedDict = {}
        self.setEnabled(True)
        self.setMinimumSize(QtCore.QSize(200, 200))
        width, height = imagesize.get(self.path)
        if width - height <= 50:  # choose if image render as rectangle or squarre
            self.setMaximumSize(QtCore.QSize(200, 200))
        else:
            self.setMaximumSize(QtCore.QSize(300, 200))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.Image = QtWidgets.QLabel(self)
        self.Image.setText("")
        self.Image.setPixmap(QtGui.QPixmap(image))
        self.Image.setScaledContents(True)
        self.layout.addWidget(self.Image)
        self.caption = QtWidgets.QLabel(self)
        self.caption.setWordWrap(True)
        self.caption.setText("")
        #self.caption.setText(self.readCaption()) # Import
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
            return os.path.splitext(self.path)[0]

    def saveImageToCaption(self):
        #dest_path = self.parentFolder + f"/{self.caption.text()}_{self.id}.png".
        if self.mainFrame.TxtCaptionCheckbox.isChecked():
            onlyName = os.path.splitext(self.path)[0]
            with open(onlyName + ".txt", "w") as f:
                f.write(self.caption.text())
        else:
            dest_path = self.parentFolder + f"/{self.caption.text()}_{self.id}{str(uuid.uuid4())[0:3]}.png"
            os.rename(self.path, dest_path)
            self.path = dest_path

    # Remplement paintEvent on custom QWidget
    def paintEvent(self, pe):
        o = QtWidgets.QStyleOption()
        o.initFrom(self)
        p = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PrimitiveElement.PE_Widget, o, p, self)

    def select(self):
        self.setStyleSheet("QWidget { background-color: rgb(255, 69, 69) }")
        self.isSelected = True

    def deselect(self):
        self.isSelected = False
        self.setStyleSheet("")

    def _dict2Caption(self):
        subjectList = []
        for i in self.usedDict.items():
            a = [element.entry.text() for element in [i[0]] + i[1]]
            subjectList.append(", ".join(a))
        name = "; ".join(subjectList)
        return name

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

