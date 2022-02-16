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
        self.confirm_button = QtWidgets.QPushButton(self.centralwidget)
        self.confirm_button.setGeometry(QtCore.QRect(280, 480, 251, 28))
        self.confirm_button.setObjectName("pushButton")
        self.select_all_button = QtWidgets.QPushButton(self.centralwidget)
        self.select_all_button.setGeometry(QtCore.QRect(30, 20, 141, 41))
        self.select_all_button.setObjectName("pushButton_2")
        self.select_all_button.clicked.connect(self.selected_all_filter)
        self.uncheck_all_button = QtWidgets.QPushButton(self.centralwidget)
        self.uncheck_all_button.setGeometry(QtCore.QRect(30, 70, 141, 41))
        self.uncheck_all_button.setObjectName("uncheck_all_button")
        self.uncheck_all_button.clicked.connect(self.clear_filter)
        self.drill_down_button = QtWidgets.QPushButton(self.centralwidget)
        self.drill_down_button.setGeometry(QtCore.QRect(620, 10, 141, 41))
        self.drill_down_button.setObjectName("pushButton_4")
        #self.drill_down_button.hide()
        self.drill_up_button = QtWidgets.QPushButton(self.centralwidget)
        self.drill_up_button.setGeometry(QtCore.QRect(620, 60, 141, 41))
        self.drill_up_button.setObjectName("pushButton_5")
        #self.drill_up_button.hide()
        FilterdimensionWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(FilterdimensionWindow)
        QtCore.QMetaObject.connectSlotsByName(FilterdimensionWindow)

    def retranslateUi(self, FilterdimensionWindow):
        _translate = QtCore.QCoreApplication.translate
        FilterdimensionWindow.setWindowTitle(_translate("FilterdimensionWindow", "FilterdimensionWIndow"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.confirm_button.setText(_translate("FilterdimensionWindow", "Confirm"))
        self.select_all_button.setText(_translate("FilterdimensionWindow", "Select All"))
        self.uncheck_all_button.setText(_translate("FilterdimensionWindow", "Uncheck All"))
        self.drill_down_button.setText(_translate("FilterdimensionWindow", "Drill Down"))
        self.drill_up_button.setText(_translate("FilterdimensionWindow", "Drill Up"))
    
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
