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
            menu.setStyleSheet("background-color: rgb(112, 112, 112)")
            editPromptAction = QtWidgets.QAction("Edit prompt", self)
            if type(self.widget) == prompt_element.PromptElement:
                applyPromptAction = QtWidgets.QAction(f"""Apply "{self.widget.parentFrame.prompt.entry.text()}" to all images""", self)
            else:
                applyPromptAction = QtWidgets.QAction(f"""Apply "{self.widget.entry.text()}" description on all "{self.widget.parentFrame.prompt.entry.text()}" prompted images""", self)
            menu.addAction(editPromptAction)
            menu.addAction(applyPromptAction)

            if prompt_element.PromptElement.currentSelected:
                applySelectedPromptsAction = QtWidgets.QAction(f"Apply selected prompts to all images", self)
                menu.addAction(applySelectedPromptsAction)

            action = menu.exec_(event.globalPos())

            if action == editPromptAction:
                self.widget.entry.setReadOnly(False)
                self.widget.isEditing = True

            elif action == applyPromptAction:
                for imageWidget in image_element.ImageElement.allImages:
                    if self.widget.parentFrame.prompt in imageWidget.usedDict.keys():
                        if type(self.widget) == prompt_element.PromptElement:
                            if self.widget.parentFrame.prompt not in imageWidget.usedDict.keys() and not imageWidget.isHidden():
                                imageWidget.usedDict[self.widget.parentFrame.prompt] = []
                        else:
                            if not self.widget in imageWidget.usedDict[self.widget.parentFrame.prompt]:
                                imageWidget.usedDict[self.widget.parentFrame.prompt].append(self.widget)

                        imageWidget.updateCaption()

            elif prompt_element.PromptElement.currentSelected and action == applySelectedPromptsAction:
                for imageWidget in image_element.ImageElement.allImages:
                    if imageWidget.isHidden(): continue
                    desc = [i for i in prompt_element.PromptElement.currentSelected.getNonEmptyDescriptions() if i in description_element.DescriptionElement.selectedDescriptions]
                    if prompt_element.PromptElement.currentSelected not in imageWidget.usedDict.keys():
                        imageWidget.usedDict[prompt_element.PromptElement.currentSelected] = desc
                    else:
                        imageWidget.usedDict[prompt_element.PromptElement.currentSelected] = [i for i in list(set(imageWidget.usedDict[prompt_element.PromptElement.currentSelected] + desc)) if i]

                    imageWidget.updateCaption()


