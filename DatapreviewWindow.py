from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DatapreviewWindow(object):
    def setupUi(self, DatapreviewWindow):
        DatapreviewWindow.setObjectName("DatapreviewWindow")
        DatapreviewWindow.resize(1139, 764)
        self.centralwidget = QtWidgets.QWidget(DatapreviewWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(340, 10, 781, 721))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.Dimensionlabel = QtWidgets.QLabel(self.centralwidget)
        self.Dimensionlabel.setGeometry(QtCore.QRect(20, 20, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Dimensionlabel.setFont(font)
        self.Dimensionlabel.setObjectName("Dimensionlabel")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 620, 231, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.dimensionlist = QtWidgets.QListWidget(self.centralwidget)
        self.dimensionlist.setGeometry(QtCore.QRect(10, 60, 311, 241))
        self.dimensionlist.setObjectName("dimensionlist")
        self.measurementlist = QtWidgets.QListWidget(self.centralwidget)
        self.measurementlist.setGeometry(QtCore.QRect(10, 360, 311, 241))
        self.measurementlist.setObjectName("measurementlist")
        self.neasurementlabel = QtWidgets.QLabel(self.centralwidget)
        self.neasurementlabel.setGeometry(QtCore.QRect(20, 320, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.neasurementlabel.setFont(font)
        self.neasurementlabel.setObjectName("neasurementlabel")
        DatapreviewWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(DatapreviewWindow)
        QtCore.QMetaObject.connectSlotsByName(DatapreviewWindow)

    def retranslateUi(self, DatapreviewWindow):
        _translate = QtCore.QCoreApplication.translate
        DatapreviewWindow.setWindowTitle(_translate("DatapreviewWindow", "DatapreviewWindow"))
        self.Dimensionlabel.setText(_translate("DatapreviewWindow", "Dimension"))
        self.pushButton_2.setText(_translate("DatapreviewWindow", "Comfirm"))
        self.neasurementlabel.setText(_translate("DatapreviewWindow", "Measurement"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DatapreviewWindow = QtWidgets.QMainWindow()
    ui = Ui_DatapreviewWindow()
    ui.setupUi(DatapreviewWindow)
    DatapreviewWindow.show()
    sys.exit(app.exec_())
