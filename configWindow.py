from PyQt5 import QtCore, QtGui, QtWidgets
from natsort import os_sorted
import os, sys, glob, configparser

import description_element
import utils
from flowlayout import FlowLayout
import prompt_element, image_element

class ConfigDialog(QtWidgets.QDialog):

    def __init__(self, mainFrame):
        self.config = mainFrame.config
        self.mainFrame = mainFrame

        super().__init__()

        self.setWindowTitle("Config Menu")
        self.resize(400, 200)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.SubfolderCheckbox = QtWidgets.QCheckBox(self)
        if self.config.has_option('DEFAULT', 'Include_Subfolder'): self.SubfolderCheckbox.setChecked(self.config.getboolean('DEFAULT', 'Include_Subfolder'))
        self.SubfolderCheckbox.stateChanged.connect(self.updateConfig)
        self.layout.addWidget(self.SubfolderCheckbox)

        self.TxtCaptionCheckbox = QtWidgets.QCheckBox(self)
        if self.config.has_option('DEFAULT', 'Txt_Caption'):
            self.TxtCaptionCheckbox.setChecked(self.config.getboolean('DEFAULT', 'Txt_Caption'))
        else:
            self.TxtCaptionCheckbox.setChecked(True)
        self.TxtCaptionCheckbox.stateChanged.connect(self.updateConfig)
        self.layout.addWidget(self.TxtCaptionCheckbox)

        self.RandomizeParentOrderCheckbox = QtWidgets.QCheckBox(self)
        if self.config.has_option('DEFAULT', 'Randomize_Parent_Order'): self.RandomizeParentOrderCheckbox.setChecked(self.config.getboolean('DEFAULT', 'Randomize_Parent_Order'))
        self.RandomizeParentOrderCheckbox.stateChanged.connect(self.updateConfig)
        self.layout.addWidget(self.RandomizeParentOrderCheckbox)

        self.RandomizeChildOrderCheckbox = QtWidgets.QCheckBox(self)
        if self.config.has_option('DEFAULT', 'Randomize_Child_Order'): self.RandomizeChildOrderCheckbox.setChecked(self.config.getboolean('DEFAULT', 'Randomize_Child_Order'))
        self.RandomizeChildOrderCheckbox.stateChanged.connect(self.updateConfig)
        self.layout.addWidget(self.RandomizeChildOrderCheckbox)

        self.addOnlyModeCheckbox = QtWidgets.QCheckBox(self)
        if self.config.has_option('DEFAULT', 'Add_Only_Mode'): self.addOnlyModeCheckbox.setChecked(self.config.getboolean('DEFAULT', 'Add_Only_Mode'))
        self.addOnlyModeCheckbox.stateChanged.connect(self.updateConfig)
        self.layout.addWidget(self.addOnlyModeCheckbox)

        self.SeparateByInfoLabel = QtWidgets.QLabel(self)
        self.SeparateByInfoLabel.setContentsMargins(0,0,0,0)
        self.SeparateByInfoLabel.setMaximumSize(100, 35)

        self.layout.addWidget(self.SeparateByInfoLabel)

        self.PrombtSeparatorFrame = QtWidgets.QFrame(self)
        self.PrombtSeparatorFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.PrombtSeparatorFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.layout.addWidget(self.PrombtSeparatorFrame)

        self.PrombtSeparatorFrameLayout = QtWidgets.QHBoxLayout(self.PrombtSeparatorFrame)

        self.subjectSeparatorLabel = QtWidgets.QLabel(self.PrombtSeparatorFrame)
        self.PrombtSeparatorFrameLayout.addWidget(self.subjectSeparatorLabel)

        self.subjectSeparatorContent = QtWidgets.QLineEdit(self.PrombtSeparatorFrame)
        if self.config.has_option('DEFAULT', 'Subject_Separator'):
            self.subjectSeparatorContent.setText(self.config.get('DEFAULT', 'Subject_Separator').strip('"'))
        else:
            self.subjectSeparatorContent.setText("; ")
        self.subjectSeparatorContent.textChanged.connect(self.updateConfig)
        self.PrombtSeparatorFrameLayout.addWidget(self.subjectSeparatorContent)

        self.descriptionSeparatorLabel = QtWidgets.QLabel(self.PrombtSeparatorFrame)
        self.PrombtSeparatorFrameLayout.addWidget(self.descriptionSeparatorLabel)

        self.descriptionSeparatorContent = QtWidgets.QLineEdit(self.PrombtSeparatorFrame)
        if self.config.has_option('DEFAULT', 'Description_Separator'):
            self.descriptionSeparatorContent.setText(self.config.get('DEFAULT', 'Description_Separator').strip('"'))
        else:
            self.descriptionSeparatorContent.setText(", ")
        self.descriptionSeparatorContent.textChanged.connect(self.updateConfig)
        self.PrombtSeparatorFrameLayout.addWidget(self.descriptionSeparatorContent)

        self.imageSizeFrame = QtWidgets.QFrame(self)
        self.imageSizeFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.imageSizeFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.layout.addWidget(self.imageSizeFrame)

        self.imageSizeFrameLayout = QtWidgets.QHBoxLayout(self.imageSizeFrame)
        self.ImageSizeLabel = QtWidgets.QLabel(self.imageSizeFrame)
        self.ImageSizeLabel.setText("Image Dimensions : ")
        self.imageSizeFrameLayout.addWidget(self.ImageSizeLabel)
        self.layout.addWidget(self.imageSizeFrame)

        self.ImageSizeContent = QtWidgets.QDoubleSpinBox(self.imageSizeFrame);
        self.ImageSizeContent.setRange(0.5, 5)
        self.ImageSizeContent.setDecimals(1);
        self.ImageSizeContent.setSingleStep(0.1);
        self.imageSizeFrameLayout.addWidget(self.ImageSizeContent)
        #self.ImageSizeContent.valueChanged.connect(self.changeImageDimension)

        if self.config.has_option('DEFAULT', 'Image_Size'):
            self.ImageSizeContent.setValue(self.config.getfloat('DEFAULT', 'Image_Size'))
        else:
            self.ImageSizeContent.setValue(1)
        self.ImageSizeContent.valueChanged.connect(self.updateConfig)
        self.ImageSizeContent.valueChanged.connect(self.changeImageDimension)

        self.SubfolderCheckbox.setText("Include Subfolders")
        self.TxtCaptionCheckbox.setText("Txt Caption")
        self.RandomizeParentOrderCheckbox.setText("Randomize parent prompt order")
        self.RandomizeChildOrderCheckbox.setText("Randomize child prompt order")
        self.addOnlyModeCheckbox.setText("Add-Only Mode")
        self.SeparateByInfoLabel.setText("Separate with :")
        self.subjectSeparatorLabel.setText("Subject :")
        self.descriptionSeparatorLabel.setText("Description :")

    def changeImageDimension(self):
        for imageWidget in image_element.ImageElement.allImages:
            imageWidget.setNewSize(self.ImageSizeContent.value())

    def updateConfig(self):
        #self.config["DEFAULT"]["Last_Folder_Path"] = self.lineEdit.text()
        self.config["DEFAULT"]["Include_Subfolder"] = str(self.SubfolderCheckbox.isChecked())
        self.config["DEFAULT"]["Txt_Caption"] = str(self.TxtCaptionCheckbox.isChecked())
        self.config["DEFAULT"]["Randomize_Parent_Order"] = str(self.RandomizeParentOrderCheckbox.isChecked())
        self.config["DEFAULT"]["Randomize_Child_Order"] = str(self.RandomizeChildOrderCheckbox.isChecked())
        self.config["DEFAULT"]["Add_Only_Mode"] = str(self.addOnlyModeCheckbox.isChecked())
        self.config["DEFAULT"]["Subject_Separator"] = f'"{self.subjectSeparatorContent.text()}"'
        self.config["DEFAULT"]["Description_Separator"] = f'"{self.descriptionSeparatorContent.text()}"'
        self.config["DEFAULT"]["Image_Size"] = str(self.ImageSizeContent.value())

        with open(self.mainFrame.configPath, 'w') as configfile:  # save
            self.config.write(configfile)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    MainWindow = ConfigDialog()
    MainWindow.show()
    sys.exit(app.exec_())

