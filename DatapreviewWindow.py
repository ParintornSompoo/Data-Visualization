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
        self.dimensionlist.setDragEnabled(True)
        self.dimensionlist.setAcceptDrops(True)
        self.dimensionlist.setDefaultDropAction(QtCore.Qt.MoveAction)

        self.measurementlist = QtWidgets.QListWidget(self.centralwidget)
        self.measurementlist.setGeometry(QtCore.QRect(10, 360, 311, 241))
        self.measurementlist.setObjectName("measurementlist")
        self.measurementlist.setDragEnabled(True)
        self.measurementlist.setAcceptDrops(True)
        self.measurementlist.setDefaultDropAction(QtCore.Qt.MoveAction)

        self.neasurementlabel = QtWidgets.QLabel(self.centralwidget)
        self.neasurementlabel.setGeometry(QtCore.QRect(20, 320, 181, 31))

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

    def show_data(self, data):
        # set row,column count
        if len(data.index) > 100:
            self.tableWidget.setRowCount(100)
        else:
            self.tableWidget.setRowCount(len(data.index))
        self.tableWidget.setColumnCount(len(data.columns))
        # set header
        for i, column in enumerate(data.columns):
            item = QtWidgets.QTableWidgetItem(column)
            self.tableWidget.setHorizontalHeaderItem(i, item)
        for i in range(len((data.index))):
            item = QtWidgets.QTableWidgetItem(str(i+1))
            self.tableWidget.setVerticalHeaderItem(i, item)
        # set data
        for i in range(len(data.index)):
            if i > 100:
                break
            for j in range(len(data.columns)):
                item = QtWidgets.QTableWidgetItem(str(data.iloc[i][j]))
                self.tableWidget.setItem(i, j, item)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DatapreviewWindow = QtWidgets.QMainWindow()
    ui = Ui_DatapreviewWindow()
    ui.setupUi(DatapreviewWindow)
    DatapreviewWindow.show()
    sys.exit(app.exec_())
