import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QListView
from selectionwindow import Ui_SecondWindow


class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1065, 737)
        self.setupUi(MainWindow)

        self.fileName = None
        self.data = None
        self.dimensions = []
        self.measurements = []

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
        self.pushButton.setGeometry(QtCore.QRect(20, 10, 221, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.file_selected)

        self.Dimensionlabel = QtWidgets.QLabel(self.frame)
        self.Dimensionlabel.setGeometry(QtCore.QRect(10, 50, 141, 31))

        font = QtGui.QFont()
        font.setPointSize(16)
        self.Dimensionlabel.setFont(font)
        self.Dimensionlabel.setObjectName("Dimensionlabel")
        self.neasurementlabel = QtWidgets.QLabel(self.frame)
        self.neasurementlabel.setGeometry(QtCore.QRect(10, 350, 181, 31))
        self.neasurementlabel.setFont(font)
        self.neasurementlabel.setObjectName("neasurementlabel")

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
        self.rowlist.doubleClicked.connect(lambda: self.getrowlistindex())

        self.columnlist = QtWidgets.QListWidget(self.frame_2)
        self.columnlist.setGeometry(QtCore.QRect(100, 20, 591, 31))
        self.columnlist.setObjectName("columnlist")
        self.columnlist.setFlow(QListView.LeftToRight)
        self.columnlist.setAcceptDrops(True)
        self.columnlist.setDragEnabled(True)
        self.columnlist.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.columnlist.doubleClicked.connect(lambda: self.getcolumnlistindex())

        self.Rowlabel = QtWidgets.QLabel(self.frame_2)
        self.Rowlabel.setGeometry(QtCore.QRect(20, 70, 71, 21))
        self.Rowlabel.setFont(font)
        self.Rowlabel.setObjectName("Rowlabel")

        self.Columnlabel = QtWidgets.QLabel(self.frame_2)
        self.Columnlabel.setGeometry(QtCore.QRect(0, 20, 91, 31))
        self.Columnlabel.setFont(font)
        self.Columnlabel.setObjectName("Columnlabel")

        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(380, 130, 661, 511))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        self.chart_container = MplWidget(self.frame_3)
        self.chart_container.setGeometry(QtCore.QRect(10, 60, 641, 421))
        self.chart_container.setObjectName("chart_container")

        self.verticalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.verticalScrollBar.setGeometry(QtCore.QRect(360, 199, 20, 441))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.verticalScrollBar.hide()

        self.horizontalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(380, 660, 671, 20))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.horizontalScrollBar.hide()

        self.statisticbtn = QtWidgets.QPushButton(self.frame_3)
        self.statisticbtn.setGeometry(QtCore.QRect(20, 10, 141, 41))
        self.statisticbtn.setObjectName("statisticbtn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.statisticbtn.clicked.connect(self.create_statistic)

        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self.window)
        self.ui.comboBox.currentTextChanged.connect(self.on_combobox_changed)
    
    def on_combobox_changed(self):
        self.mode = self.ui.comboBox.currentText()
        print(self.mode)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Select File"))
        self.Dimensionlabel.setText(_translate("MainWindow", "Dimension"))
        self.neasurementlabel.setText(_translate("MainWindow", "Measurement"))
        self.Rowlabel.setText(_translate("MainWindow", "Row"))
        self.Columnlabel.setText(_translate("MainWindow", "Column"))
        self.statisticbtn.setText(_translate("MainWindow", "Statistic"))

    def file_selected(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName()
        self.fileName = fileName
        if self.fileName != None:
            self.read_file()

    def read_file(self):
        extension = self.fileName.split(".")[1]
        if extension == "csv":
            self.data = pd.read_csv(self.fileName, encoding="ISO-8859-1")
            self.setDimensionsMeasurements()
        elif extension == "xlsx":
            self.data = pd.read_excel(self.fileName, engine='openpyxl')
            self.setDimensionsMeasurements()
        self.set_listwidget()

    def setDimensionsMeasurements(self):
        for i, _type in enumerate(self.data.dtypes):
            if _type == "O":
                self.dimensions.append(self.data.columns[i])
            else:
                self.measurements.append(self.data.columns[i])

    def set_listwidget(self):
        for dimensions in self.dimensions:
            self.dimensionlist.addItem(dimensions)
        for measurements in self.measurements:
            self.measurementlist.addItem(measurements)
    
    def getcolumnlistindex(self):
        print(self.columnlist.currentIndex().row())
        print(self.columnlist.currentItem().text())
        if self.columnlist.currentItem().text() in self.measurements:
            self.columnselected = True
            self.secondwindow()

    def getrowlistindex(self):
        print(self.rowlist.currentIndex().row())
        print(self.rowlist.currentItem().text())
        if self.rowlist.currentItem().text() in self.measurements:
            self.columnselected = False
            self.secondwindow()

    def secondwindow(self):
        _translate = QtCore.QCoreApplication.translate
        if self.columnselected:
            self.ui.label.setText(_translate("SecondWindow", 
            self.columnlist.currentItem().text()))
        else:
            self.ui.label.setText(_translate("SecondWindow", 
            self.rowlist.currentItem().text()))
        self.window.show()

    def setupSlider(self):
        self.limx = np.array(self.chart_container.canvas.ax.get_xlim())
        self.limy = np.array(self.chart_container.canvas.ax.get_ylim())
        self.horizontalScrollBar.actionTriggered.connect(self.update)
        self.verticalScrollBar.actionTriggered.connect(self.update)
        self.update()

    def update(self, evt=None):
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

    def create_statistic(self):
        # print(self.ui.mode)
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
                data = self.data.groupby(columnitem[0].text()).sum()[
                    row_item.text()]
                labels = list(data.index)
                values = list(data.values)
                x = np.arange(len(labels))  # the label locations
                rects1 = self.chart_container.canvas.ax.bar(
                    x + width*i, values, width, label=row_item.text())
                self.chart_container.canvas.ax.set_ylabel(row_item.text())
                self.chart_container.canvas.ax.set_xticks(x + width*i, labels)
                self.chart_container.canvas.ax.bar_label(rects1, padding=3)
                self.verticalScrollBar.hide()
                self.horizontalScrollBar.show()

        elif rowitems[0].text() in self.dimensions:
            self.verticalchart = False
            width = 0.5/len(columnitem)  # the width of the bars
            for i, column_item in enumerate(columnitem):
                data = self.data.groupby(rowitems[0].text()).sum()[
                    column_item.text()]
                labels = list(data.index)
                values = list(data.values)
                x = np.arange(len(labels))  # the label locations
                rects2 = self.chart_container.canvas.ax.barh(
                    x + width*i, values, width, label=column_item.text())
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
