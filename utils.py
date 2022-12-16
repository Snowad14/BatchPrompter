from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox

def sendErrorMessage(message : str):
    errorDialog = QtWidgets.QMessageBox()
    errorDialog.setText(message)
    errorDialog.setWindowTitle("Error")
    errorDialog.exec_()

def sendConfirmMessage(message : str):
    result = QMessageBox.question(
        None,
        'Confirmation',
        message,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    return result == QMessageBox.Yes

class clickableQLineEdit(QtWidgets.QLineEdit):
    clicked = QtCore.pyqtSignal()

    def __init__(self, widget):
        super().__init__(widget)

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()

