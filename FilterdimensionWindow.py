from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FilterdimensionWindow(object):
    def setupUi(self, FilterdimensionWindow):
        FilterdimensionWindow.setObjectName("FilterdimensionWindow")
        FilterdimensionWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(FilterdimensionWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(200, 130, 421, 331))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 480, 251, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 20, 141, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.selected_all_filter)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 70, 141, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.clear_filter)
        FilterdimensionWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(FilterdimensionWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        FilterdimensionWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(FilterdimensionWindow)
        self.statusbar.setObjectName("statusbar")
        FilterdimensionWindow.setStatusBar(self.statusbar)

        self.retranslateUi(FilterdimensionWindow)
        QtCore.QMetaObject.connectSlotsByName(FilterdimensionWindow)

    def retranslateUi(self, FilterdimensionWindow):
        _translate = QtCore.QCoreApplication.translate
        FilterdimensionWindow.setWindowTitle(_translate("FilterdimensionWindow", "FilterdimensionWIndow"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("FilterdimensionWindow", "Confirm"))
        self.pushButton_2.setText(_translate("FilterdimensionWindow", "Select All"))
        self.pushButton_3.setText(_translate("FilterdimensionWindow", "Uncheck All"))
    
    def clear_filter(self):
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            item.setCheckState(QtCore.Qt.Unchecked)
    
    def selected_all_filter(self):
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            item.setCheckState(QtCore.Qt.Checked)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FilterdimensionWindow = QtWidgets.QMainWindow()
    ui = Ui_FilterdimensionWindow()
    ui.setupUi(FilterdimensionWindow)
    FilterdimensionWindow.show()
    sys.exit(app.exec_())
