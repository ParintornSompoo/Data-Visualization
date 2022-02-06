from re import S
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QListView
from selectionwindow import Ui_SecondWindow
from DatapreviewWindow import Ui_DatapreviewWindow



class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1088, 762)
        self.setupUi(MainWindow)

        self.fileName = None
        self.data = None
        self.dimensions = []
        self.measurements = []
        self.MODE = {}

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

        self.measurementlist = QtWidgets.QListWidget(self.frame)
        self.measurementlist.setGeometry(QtCore.QRect(0, 390, 311, 241))
        self.measurementlist.setObjectName("measurementlist")
        self.measurementlist.setDragEnabled(True)

        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 151, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.file_selected)

        self.union_button = QtWidgets.QPushButton(self.frame)
        self.union_button.setGeometry(QtCore.QRect(170, 10, 151, 31))
        self.union_button.setObjectName("union_button")
        # self.union_button.clicked.connect(lambda:print("hello world"))

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
        self.tabWidget.setGeometry(QtCore.QRect(360, 120, 711, 621))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(20, 10, 671, 581))
        self.tableWidget.setObjectName("tableWidget")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.frame_3 = QtWidgets.QFrame(self.tab_2)
        self.frame_3.setGeometry(QtCore.QRect(380, 130, 661, 511))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")


        self.chart_container = MplWidget(self.tab_2)
        self.chart_container.setGeometry(QtCore.QRect(10, 60, 641, 421))
        self.chart_container.setObjectName("chart_container")

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
        fileName, _ = QFileDialog.getOpenFileName()
        self.fileName = fileName
        if self.fileName != None:
            self.read_file()
        
    def union_data(self):
        pass

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
        for dimensions in self.dimensions:
            i = Item(dimensions)
            self.dimensionlist.addItem(i)
        for measurements in self.measurements:
            i = Item(measurements)
            self.measurementlist.addItem(i)
    
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

    def setupSlider(self):          # setting up slider
        self.limx = np.array(self.chart_container.canvas.ax.get_xlim())
        self.limy = np.array(self.chart_container.canvas.ax.get_ylim())
        self.horizontalScrollBar.actionTriggered.connect(self.update)
        self.verticalScrollBar.actionTriggered.connect(self.update)
        self.update()

    def update(self, evt=None):     # update slider
        if self.verticalchart:
            r = self.horizontalScrollBar.value() / ((1 + self.step) * 100)
            l1 = self.limx[0] + r * np.diff(self.limx)
            l2 = l1 + np.diff(self.limx) * self.step
            self.chart_container.canvas.ax.set_xlim(l1, l2)
        else:
            v = self.verticalScrollBar.value() / ((1 + self.step) * 100)
            l3 = self.limy[0] + v * np.diff(self.limy)
            l4 = l3 + np.diff(self.limy) * self.step
            self.chart_container.canvas.ax.set_ylim(l4, l3)
        self.chart_container.canvas.draw_idle()

    def on_combobox_changed(self):
        mode = self.ui.comboBox.currentText()       # current selected mode
        if self.columnselected:
            self.columnlist.item(self.index).mode = mode
            self.MODE[self.columnlist.item(self.index).text()] = mode
        else:
            self.rowlist.item(self.index).mode = mode
            self.MODE[self.rowlist.item(self.index).text()] = mode
   
    def create_statistic(self):
        self.chart_container.canvas.ax.cla()        # clear previous plot
        # get row columns
        columnitem = []
        for index in range(self.columnlist.count()):
            columnitem.append(self.columnlist.item(index))
        rowitems = []
        for index in range(self.rowlist.count()):
            rowitems.append(self.rowlist.item(index))

        if columnitem[0].text() in self.dimensions:
            self.verticalchart = True
            width = 0.5/len(rowitems)  # the width of the bars
            for i, row_item in enumerate(rowitems):
                mode = None
                if row_item.text() in self.MODE.keys():
                    mode = self.MODE[row_item.text()]
                    if mode == "sum":
                        data = self.data.groupby(columnitem[0].text()).sum()[
                            row_item.text()]
                    elif mode == "mean":
                        data = self.data.groupby(columnitem[0].text()).mean()[
                            row_item.text()]
                    elif mode == "median":
                        data = self.data.groupby(columnitem[0].text()).median()[
                            row_item.text()]
                else:
                    mode = "sum"
                    data = self.data.groupby(columnitem[0].text()).sum()[
                        row_item.text()]
                labels = list(data.index)
                values = list(data.values)
                x = np.arange(len(labels))  # the label locations
                rects1 = self.chart_container.canvas.ax.bar(
                    x + width*i, values, width, label=f"{row_item.text()} ({mode})")
                self.chart_container.canvas.ax.set_ylabel(row_item.text())
                self.chart_container.canvas.ax.set_xticks(x + width*i, labels)
                self.chart_container.canvas.ax.bar_label(rects1, padding=3)
                self.verticalScrollBar.hide()
                self.horizontalScrollBar.show()

        elif rowitems[0].text() in self.dimensions:
            self.verticalchart = False
            width = 0.5/len(columnitem)  # the width of the bars
            for i, column_item in enumerate(columnitem):
                mode = None
                if column_item.text() in self.MODE.keys():
                    mode = self.MODE[column_item.text()]
                    if mode == "sum":
                        data = self.data.groupby(rowitems[0].text()).sum()[
                            column_item.text()]
                    elif mode == "mean":
                        data = self.data.groupby(rowitems[0].text()).mean()[
                            column_item.text()]
                    elif mode == "median":
                        data = self.data.groupby(rowitems[0].text()).median()[
                            column_item.text()]
                else:
                    mode = "sum"
                    data = self.data.groupby(rowitems[0].text()).sum()[
                        column_item.text()]
                labels = list(data.index)
                values = list(data.values)
                x = np.arange(len(labels))  # the label locations
                rects2 = self.chart_container.canvas.ax.barh(
                    x + width*i, values, width, label=f"{column_item.text()} ({mode})")
                self.chart_container.canvas.ax.set_xlabel(column_item.text())
                self.chart_container.canvas.ax.set_yticks(x + width*i, labels)
                self.chart_container.canvas.ax.bar_label(rects2, padding=3)
                self.horizontalScrollBar.hide()
                self.verticalScrollBar.show()

        else:
            print("No row & column selected")
            return

        self.chart_container.canvas.ax.legend()

        self.chart_container.canvas.draw()
        self.step = 3/len(labels)
        self.setupSlider()

class Item(QtWidgets.QListWidgetItem):
    def __init__(self, *args, **kwargs):
        self.mode = "sum"
        QtWidgets.QListWidgetItem.__init__(self, *args, **kwargs)


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        super().__init__(self.fig)


class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()                  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
