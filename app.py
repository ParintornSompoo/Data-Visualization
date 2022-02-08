import os
import sys
import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets , QtWebEngineWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QListView
from selectionwindow import Ui_SecondWindow
from DatapreviewWindow import Ui_DatapreviewWindow
from io import StringIO
import altair as alt
from vega_datasets import data




class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1342, 762)

        # picture path
        self.line_icon_path = os.getcwd() + "/picture/line.png" 
        self.bar_icon_path = os.getcwd() + "/picture/bar.png"
        self.pie_icon_path = os.getcwd() + "/picture/pie.png"


        self.fileName = None
        self.data = None
        self.dimensions = []
        self.measurements = []
        self.MODE = {}

        self.setupUi(MainWindow)
    def setupUi(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 351, 671))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.dimensionlist = QtWidgets.QListWidget(self.frame)
        self.dimensionlist.setGeometry(QtCore.QRect(0, 90, 311, 241))
        self.dimensionlist.setObjectName("dimensionlist")
        self.dimensionlist.setDragEnabled(True)
        self.dimensionlist.setAcceptDrops(True)
        self.dimensionlist.setDefaultDropAction(QtCore.Qt.MoveAction)

        self.measurementlist = QtWidgets.QListWidget(self.frame)
        self.measurementlist.setGeometry(QtCore.QRect(0, 390, 311, 241))
        self.measurementlist.setObjectName("measurementlist")
        self.measurementlist.setDragEnabled(True)
        self.measurementlist.setAcceptDrops(True)
        self.measurementlist.setDefaultDropAction(QtCore.Qt.MoveAction)

        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 151, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.file_selected)

        self.union_button = QtWidgets.QPushButton(self.frame)
        self.union_button.setGeometry(QtCore.QRect(170, 10, 151, 31))
        self.union_button.setObjectName("union_button")
        self.union_button.clicked.connect(self.union_data)

        self.Dimensionlabel = QtWidgets.QLabel(self.frame)
        self.Dimensionlabel.setGeometry(QtCore.QRect(10, 50, 141, 31))

        font = QtGui.QFont()
        font.setPointSize(16)
        self.Dimensionlabel.setFont(font)
        self.Dimensionlabel.setObjectName("Dimensionlabel")
        self.measurementlabel = QtWidgets.QLabel(self.frame)
        self.measurementlabel.setGeometry(QtCore.QRect(10, 350, 181, 31))
        self.measurementlabel.setFont(font)
        self.measurementlabel.setObjectName("measurementlabel")

        self.viewdata_button = QtWidgets.QPushButton(self.frame)
        self.viewdata_button.setGeometry(QtCore.QRect(10, 640, 231, 28))
        self.viewdata_button.setObjectName("pushButton_2")
        self.viewdata_button.clicked.connect(self.datapreviewwindow)

        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(350, 10, 701, 111))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.rowlist = QtWidgets.QListWidget(self.frame_2)
        self.rowlist.setGeometry(QtCore.QRect(100, 70, 591, 31))
        self.rowlist.setObjectName("rowlist")
        self.rowlist.setFlow(QListView.LeftToRight)
        self.rowlist.setDragEnabled(True)
        self.rowlist.setAcceptDrops(True)
        self.rowlist.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.rowlist.doubleClicked.connect(self.getrowlistindex)
        self.rowlist.itemChanged.connect(self.set_grid_table)

        self.columnlist = QtWidgets.QListWidget(self.frame_2)
        self.columnlist.setGeometry(QtCore.QRect(100, 20, 591, 31))
        self.columnlist.setObjectName("columnlist")
        self.columnlist.setFlow(QListView.LeftToRight)
        self.columnlist.setAcceptDrops(True)
        self.columnlist.setDragEnabled(True)
        self.columnlist.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.columnlist.doubleClicked.connect(self.getcolumnlistindex)
        self.columnlist.itemChanged.connect(self.set_grid_table)

        self.Rowlabel = QtWidgets.QLabel(self.frame_2)
        self.Rowlabel.setGeometry(QtCore.QRect(20, 70, 71, 21))
        self.Rowlabel.setFont(font)
        self.Rowlabel.setObjectName("Rowlabel")

        self.Columnlabel = QtWidgets.QLabel(self.frame_2)
        self.Columnlabel.setGeometry(QtCore.QRect(0, 20, 91, 31))
        self.Columnlabel.setFont(font)
        self.Columnlabel.setObjectName("Columnlabel")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(360, 120, 961, 621))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(20, 10, 911, 581))
        self.tableWidget.setObjectName("tableWidget")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.frame_3 = QtWidgets.QFrame(self.tab_2)
        self.frame_3.setGeometry(QtCore.QRect(380, 130, 661, 511))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        self.chart_list = QtWidgets.QListWidget(self.tab_2)
        self.chart_list.setGeometry(QtCore.QRect(740, 30, 181, 501))
        self.chart_list.setObjectName("chart_list")

        # set icon image

        self.bar_icon = QtGui.QIcon(self.bar_icon_path)
        self.pie_icon = QtGui.QIcon(self.pie_icon_path)
        self.line_icon = QtGui.QIcon(self.line_icon_path)
        self.bar_list = QtWidgets.QListWidgetItem("")
        self.bar_list.setIcon(self.bar_icon)
        self.pie_list = QtWidgets.QListWidgetItem("")
        self.pie_list.setIcon(self.pie_icon)
        self.line_list = QtWidgets.QListWidgetItem("")
        self.line_list.setIcon(self.line_icon)
        size = QtCore.QSize(150,180)
        self.chart_list.setIconSize(size)
        self.chart_list.addItem(self.bar_list)
        self.chart_list.addItem(self.pie_list)
        self.chart_list.addItem(self.line_list)

        self.chart_container = QtWidgets.QWidget(self.tab_2)
        self.chart_container.setGeometry(QtCore.QRect(10, 60, 671, 431))
        self.chart_container.setObjectName("chart_container")

        self.chart = WebEngineView()
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.chart)
        self.chart_container.setLayout(self.vbl)

        cars = data.cars()

        chart = (
            alt.Chart(cars)
            .mark_bar()
            .encode(x=alt.X("Miles_per_Gallon", bin=True), y="count()",)
            .properties(title="A bar chart")
            .configure_title(anchor="start")
        )
        self.chart.updateChart(chart)

        self.verticalScrollBar = QtWidgets.QScrollBar(self.tab_2)
        self.verticalScrollBar.setGeometry(QtCore.QRect(10, 70, 20, 441))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.verticalScrollBar.hide()

        self.horizontalScrollBar = QtWidgets.QScrollBar(self.tab_2)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(30, 530, 671, 20))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.horizontalScrollBar.hide()

        self.statisticbtn = QtWidgets.QPushButton(self.tab_2)
        self.statisticbtn.setGeometry(QtCore.QRect(20, 10, 141, 41))
        self.statisticbtn.setObjectName("statisticbtn")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.statisticbtn.clicked.connect(self.create_statistic)

        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self.window)
        self.ui.comboBox.currentTextChanged.connect(self.on_combobox_changed)


        self.window2 = QtWidgets.QMainWindow()
        self.ui2 = Ui_DatapreviewWindow()
        self.ui2.setupUi(self.window2)
        self.ui2.pushButton_2.clicked.connect(self.reset_dimension_measure)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Select File"))
        self.Dimensionlabel.setText(_translate("MainWindow", "Dimension"))
        self.measurementlabel.setText(_translate("MainWindow", "Measurement"))
        self.viewdata_button.setText(_translate("MainWindow", "View Data"))
        self.Rowlabel.setText(_translate("MainWindow", "Row"))
        self.union_button.setText(_translate("MainWindow", "View Data"))
        self.union_button.setText(_translate("MainWindow", "Union data"))
        self.Columnlabel.setText(_translate("MainWindow", "Column"))
        self.statisticbtn.setText(_translate("MainWindow", "Statistic"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Grid Table"))
        self.statisticbtn.setText(_translate("MainWindow", "Statistic"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Plot"))

    def file_selected(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName()     # selected file
        self.fileName = fileName
        if self.fileName != None:
            self.read_file()
        
    def union_data(self):       # from  union button
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName()    # selected file
        if (file_name != None) and (file_name != ""):   
            extension = file_name.split(".")[-1]        # file extension type
            if extension == "csv":
                data = pd.read_csv(file_name, encoding="ISO-8859-1")
            elif extension == "xlsx":
                data = pd.read_excel(file_name, engine='openpyxl')
            else:
                data = None
            self.data = pd.concat([self.data, data])    # union data 

    def read_file(self):
        if self.fileName != "":
            extension = self.fileName.split(".")[-1]
        else:
            return
        if extension == "csv":
            self.data = pd.read_csv(self.fileName, encoding="ISO-8859-1")
            self.setDimensionsMeasurements()
        elif extension == "xlsx":
            self.data = pd.read_excel(self.fileName, engine='openpyxl')
            self.setDimensionsMeasurements()
        self.set_listwidget()

    def setDimensionsMeasurements(self):
        self.dimensions = []
        self.measurements = []
        for i, col in enumerate(self.data.columns):
            if self.data[col].dtypes == "O":
                self.dimensions.append(self.data.columns[i])
            elif col.lower().find("id") > 0:
                self.dimensions.append(self.data.columns[i])
            elif col.lower().find("code") > 0:
                self.dimensions.append(self.data.columns[i])
            else:
                self.measurements.append(self.data.columns[i])

    def set_listwidget(self):
        self.dimensionlist.clear()
        self.measurementlist.clear()
        for dimensions in self.dimensions:
            self.dimensionlist.addItem(dimensions)
        for measurements in self.measurements:
            self.measurementlist.addItem(measurements)
    
    def getcolumnlistindex(self):
        if self.columnlist.currentItem().text() in self.measurements:
            self.index = self.columnlist.currentIndex().row()
            if type(self.columnlist.currentItem()) != Item:
                i = Item(self.columnlist.currentItem().text())
                self.columnlist.takeItem(self.index)
                self.columnlist.insertItem(self.index,i)
            self.columnselected = True
            self.secondwindow(self.index)

    def getrowlistindex(self):
        if self.rowlist.currentItem().text() in self.measurements:
            self.index = self.rowlist.currentIndex().row()
            if type(self.rowlist.currentItem()) != Item:
                i = Item(self.rowlist.currentItem().text())
                self.rowlist.takeItem(self.index)
                self.rowlist.insertItem(self.index,i)
            self.columnselected = False
            self.secondwindow(self.index)

    def secondwindow(self, index):
        _translate = QtCore.QCoreApplication.translate
        if self.columnselected:
            self.ui.label.setText(_translate("SecondWindow", 
            self.columnlist.item(index).text()))
            if self.columnlist.item(index).text() in self.MODE.keys():
                self.ui.comboBox.setCurrentText(self.MODE[self.columnlist.item(index).text()])
            else:
                self.ui.comboBox.setCurrentText(self.columnlist.item(index).mode)
        else:
            self.ui.label.setText(_translate("SecondWindow", 
            self.rowlist.item(index).text()))
            if self.rowlist.item(index).text() in self.MODE.keys():
                self.ui.comboBox.setCurrentText(self.MODE[self.rowlist.item(index).text()])
            else:
                self.ui.comboBox.setCurrentText(self.rowlist.item(index).mode)
        self.window.show()

    def datapreviewwindow(self):
        # clear dimensions, measurements Qlistwidget
        self.ui2.dimensionlist.clear()
        self.ui2.measurementlist.clear()
        # add item to Qlistwidget
        for dimension in self.dimensions:
            self.ui2.dimensionlist.addItem(dimension)
        for measurement in self.measurements:
            self.ui2.measurementlist.addItem(measurement)
        self.ui2.show_data(self.data)
        self.window2.show()     # show data preview window

    def reset_dimension_measure(self):
        # clear old dimensions, measurements
        self.dimensions = []
        self.measurements = []
        # set new dimensions, measurements from QListWidget
        for index in range(self.ui2.dimensionlist.count()):
            self.dimensions.append(self.ui2.dimensionlist.item(index).text())
        for index in range(self.ui2.measurementlist.count()):
            self.measurements.append(self.ui2.measurementlist.item(index).text())
        # set new dimensions, measurements in mainwindow
        self.dimensionlist.clear()
        self.measurementlist.clear()
        for dimension in self.dimensions:
            self.dimensionlist.addItem(dimension)
        for measurement in self.measurements:
            self.measurementlist.addItem(measurement)
        self.window2.hide()

    def set_grid_table(self):
        dimensions = []
        measurements = []
        for index in range(self.rowlist.count()):
            item = self.rowlist.item(index).text()
            if item in self.dimensions:
                dimensions.append(item)
            else:
                measurements.append(item)
        for index in range(self.columnlist.count()):
            item = self.columnlist.item(index).text()
            if item in self.dimensions:
                dimensions.append(item)
            else:
                measurements.append(item)
        agg = {}
        for measurement in measurements:
            agg = self.MODE
            if measurement not in self.MODE.keys():
                agg[measurement] = "sum"
        if len(dimensions) > 0 and len(measurements) > 0:
            data = self.data.groupby(dimensions, as_index=False).agg(agg)
            print(data)
            # set row,column count
            self.tableWidget.setRowCount(len(data.index.tolist()))
            self.tableWidget.setColumnCount(len(data.columns.tolist()))
            # set header
            for i, column in enumerate(data.columns.tolist()):
                item = QtWidgets.QTableWidgetItem(column)
                self.tableWidget.setHorizontalHeaderItem(i, item)
            for i, index in enumerate(data.index.tolist()):
                item = QtWidgets.QTableWidgetItem(index)
                self.tableWidget.setVerticalHeaderItem(i, item)
            # set data
            for i in range(len(data.index.tolist())):
                for j in range(len(data.columns.tolist())):
                    item = QtWidgets.QTableWidgetItem(str(data.iloc[i][j]))
                    self.tableWidget.setItem(i, j, item)

    def on_combobox_changed(self):
        mode = self.ui.comboBox.currentText()       # current selected mode
        if self.columnselected:
            self.columnlist.item(self.index).mode = mode
            self.MODE[self.columnlist.item(self.index).text()] = mode
        else:
            self.rowlist.item(self.index).mode = mode
            self.MODE[self.rowlist.item(self.index).text()] = mode
   
    def create_statistic(self):
        # get row columns
        columnitem = []
        for index in range(self.columnlist.count()):
            columnitem.append(self.columnlist.item(index))
        rowitems = []
        for index in range(self.rowlist.count()):
            rowitems.append(self.rowlist.item(index))


class Item(QtWidgets.QListWidgetItem):
    def __init__(self, *args, **kwargs):
        self.mode = "sum"
        QtWidgets.QListWidgetItem.__init__(self, *args, **kwargs)


class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page().profile().downloadRequested.connect(self.onDownloadRequested)
        self.windows = []

    @QtCore.pyqtSlot(QtWebEngineWidgets.QWebEngineDownloadItem)
    def onDownloadRequested(self, download):
        if (
            download.state()
            == QtWebEngineWidgets.QWebEngineDownloadItem.DownloadRequested
        ):
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, self.tr("Save as"), download.path()
            )
            if path:
                download.setPath(path)
                download.accept()

    def createWindow(self, type_):
        if type_ == QtWebEngineWidgets.QWebEnginePage.WebBrowserTab:
            window = QtWidgets.QMainWindow(self)
            view = QtWebEngineWidgets.QWebEngineView(window)
            window.resize(640, 480)
            window.setCentralWidget(view)
            window.show()
            return view

    def updateChart(self, chart, **kwargs):
        output = StringIO()
        chart.save(output, "html", **kwargs)
        self.setHtml(output.getvalue())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
