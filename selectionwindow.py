from PyQt5 import QtCore, QtGui, QtWidgets
import range_slider

class Ui_SecondWindow(object):
    def setupUi(self, SecondWindow):
        SecondWindow.setObjectName("SecondWindow")
        SecondWindow.resize(325, 339)
        self.secondwindow = SecondWindow
        self.centralwidget = QtWidgets.QWidget(SecondWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(80, 90, 171, 22))
        self.comboBox.setObjectName("comboBox")
        AGG = ["sum", "mean", "median", "min", "max", "count"]
        for agg in AGG:
            self.comboBox.addItem(agg)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(90, 280, 161, 28))
        self.pushButton.setObjectName("pushButton")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(130, 130, 70, 17))
        self.checkBox.setObjectName("checkBox")
        self.horizontalSlider = range_slider.RangeSlider(QtCore.Qt.Horizontal,self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(40, 190, 241, 22))
        self.horizontalSlider.setMinimumHeight(30)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(100)
        
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 160, 91, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(230, 160, 91, 13))
        self.label_3.setObjectName("label_3")

        SecondWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SecondWindow)
        QtCore.QMetaObject.connectSlotsByName(SecondWindow)

        self.mode = self.comboBox.currentText()
        
    def retranslateUi(self, SecondWindow):
        _translate = QtCore.QCoreApplication.translate
        SecondWindow.setWindowTitle(_translate("SecondWindow", "SelectionWindow"))
        self.label.setText(_translate("SecondWindow", "Text"))
        self.pushButton.setText(_translate("SecondWindow", "Comfirm"))
        self.checkBox.setText(_translate("SecondWindow", "Filter"))
        self.label_2.setText(_translate("SecondWindow", "min"))
        self.label_3.setText(_translate("SecondWindow", "max"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SecondWindow = QtWidgets.QMainWindow()
    ui = Ui_SecondWindow()
    ui.setupUi(SecondWindow)
    SecondWindow.show()
    sys.exit(app.exec_())
