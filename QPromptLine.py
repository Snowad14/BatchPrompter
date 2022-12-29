from PyQt5 import QtWidgets, QtGui, QtCore

import description_element
import image_element, prompt_element

class QPromptLine(QtWidgets.QLineEdit):
    clicked = QtCore.pyqtSignal()

    def __init__(self, widget : QtWidgets.QMenu):
        self.widget = widget
        super().__init__(widget)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()

    def contextMenuEvent(self, event):
        if self.widget.entry.text():
            menu = QtWidgets.QMenu(self)

            editPromptAction = QtWidgets.QAction("Edit prompt", self)
            applyMainPromptAction = QtWidgets.QAction(f"""Apply "{self.widget.parentFrame.prompt.entry.text()}" to all images""", self)
            menu.addAction(editPromptAction)
            menu.addAction(applyMainPromptAction)

            if prompt_element.PromptElement.currentSelected:
                applySelectedPromptsAction = QtWidgets.QAction(f"Apply selected prompts to all images", self)
                menu.addAction(applySelectedPromptsAction)

            action = menu.exec_(event.globalPos())

            if action == editPromptAction:
                self.widget.entry.setReadOnly(False)
                self.widget.isEditing = True

            elif action == applyMainPromptAction:
                for imageWidget in image_element.ImageElement.allImages:
                    # Retrieves the main prompt even if the function is run in a DescriptionElement or a PromptElement
                    if self.widget.parentFrame.prompt not in imageWidget.usedDict.keys():
                        imageWidget.usedDict[self.widget.parentFrame.prompt] = []
                        imageWidget.updateCaption()

            elif prompt_element.PromptElement.currentSelected and action == applySelectedPromptsAction:
                for imageWidget in image_element.ImageElement.allImages:
                    # Retrieves the main prompt even if the function is run in a DescriptionElement or a PromptElement
                    desc = [i for i in prompt_element.PromptElement.currentSelected.getNonEmptyDescriptions() if i in description_element.DescriptionElement.selectedDescriptions]
                    if prompt_element.PromptElement.currentSelected not in imageWidget.usedDict.keys():
                        imageWidget.usedDict[prompt_element.PromptElement.currentSelected] = desc
                    else:
                        imageWidget.usedDict[prompt_element.PromptElement.currentSelected] = [i for i in list(set(imageWidget.usedDict[prompt_element.PromptElement.currentSelected] + desc)) if i]

                    imageWidget.updateCaption()

