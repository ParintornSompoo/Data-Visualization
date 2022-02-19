import os
import sys
import json
import hashlib
from types import NoneType
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets , QtWebEngineWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QListView , QMenu , QWidget
from selectionwindow import Ui_SecondWindow
from DatapreviewWindow import Ui_DatapreviewWindow
from FilterdimensionWindow import Ui_FilterdimensionWindow
from io import StringIO
import altair as alt



class Ui_MainWindow(QtWidgets.QMainWindow,object):
    def __init__(self, MainWindow,parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1905, 1047)

        # picture path
        self.line_icon_path = os.getcwd() + "/picture/line.png" 
        self.bar_icon_path = os.getcwd() + "/picture/bar.png"
        self.pie_icon_path = os.getcwd() + "/picture/pie.png"


        self.file_path = ""
        self.data = None
        self.dimensions = []
        self.datetime_dimensions = []
        self.measurements = []
        self.MODE = {}
        self.filter = {}
        self.measurement_filter = {}
        self.agg = {}
        self.chart_type = 0  # 0 : bar, 1 : pie , 2 : line
        self.group_dimension = []

        self.setupUi(MainWindow)
    def setupUi(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 351, 871))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.dimensionlist = QtWidgets.QListWidget(self.frame)
        self.dimensionlist.setGeometry(QtCore.QRect(0, 110, 311, 281))
        self.dimensionlist.setObjectName("dimensionlist")
        self.dimensionlist.setDragEnabled(True)
        self.dimensionlist.setAcceptDrops(True)
        self.dimensionlist.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.dimensionlist.installEventFilter(self)
        self.dimensionlist.setSelectionMode(2)
        #self.dimensionlist.itemSelectionChanged.connect(self.group_dimension)

        self.measurementlist = QtWidgets.QListWidget(self.frame)
        self.measurementlist.setGeometry(QtCore.QRect(0, 510, 311, 291))
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
        self.measurementlabel.setGeometry(QtCore.QRect(10, 430, 181, 31))
        self.measurementlabel.setFont(font)
        self.measurementlabel.setObjectName("measurementlabel")

        self.viewdata_button = QtWidgets.QPushButton(self.frame)
        self.viewdata_button.setGeometry(QtCore.QRect(10, 820, 231, 28))
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
        self.rowlist.itemEntered.connect(self.set_grid_table)
        self.rowlist.installEventFilter(self)

        self.columnlist = QtWidgets.QListWidget(self.frame_2)
        self.columnlist.setGeometry(QtCore.QRect(100, 20, 591, 31))
        self.columnlist.setObjectName("columnlist")
        self.columnlist.setFlow(QListView.LeftToRight)
        self.columnlist.setAcceptDrops(True)
        self.columnlist.setDragEnabled(True)
        self.columnlist.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.columnlist.doubleClicked.connect(self.getcolumnlistindex)
        self.columnlist.itemChanged.connect(self.set_grid_table)
        self.columnlist.itemEntered.connect(self.set_grid_table)
        self.columnlist.installEventFilter(self)

        self.clear_col_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_col_button.setGeometry(QtCore.QRect(1050, 30, 151, 31))
        self.clear_col_button.clicked.connect(self.columnlist.clear)
        self.clear_col_button.setObjectName("clear_col_button")
        self.clear_row_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_row_button.setGeometry(QtCore.QRect(1050, 80, 151, 31))
        self.clear_row_button.setObjectName("clear_row_button")
        self.clear_row_button.clicked.connect(self.rowlist.clear)

        self.Rowlabel = QtWidgets.QLabel(self.frame_2)
        self.Rowlabel.setGeometry(QtCore.QRect(20, 70, 71, 21))
        self.Rowlabel.setFont(font)
        self.Rowlabel.setObjectName("Rowlabel")

        self.Columnlabel = QtWidgets.QLabel(self.frame_2)
        self.Columnlabel.setGeometry(QtCore.QRect(0, 20, 91, 31))
        self.Columnlabel.setFont(font)
        self.Columnlabel.setObjectName("Columnlabel")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(360, 120, 1491, 741))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(20, 10, 1461, 681))
        self.tableWidget.setObjectName("tableWidget")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.frame_3 = QtWidgets.QFrame(self.tab_2)
        self.frame_3.setGeometry(QtCore.QRect(40, 10, 661, 511))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        self.chart_list = QtWidgets.QListWidget(self.tab_2)
        self.chart_list.setGeometry(QtCore.QRect(1280, 110, 181, 501))
        self.chart_list.setObjectName("chart_list")
        self.chart_list.itemClicked.connect(self.select_chart_type)

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
        self.chart_container.setGeometry(QtCore.QRect(10, 60, 1231, 631))
        self.chart_container.setObjectName("chart_container")

        self.chart = WebEngineView()
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.chart)
        self.chart_container.setLayout(self.vbl)

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
        self.ui.pushButton.clicked.connect(self.set_measurement_filter)
        self.ui.horizontalSlider.sliderMoved.connect(self.update_minmax_label)
        self.ui.horizontalSlider.valueChanged.connect(self.update_minmax_label)


        self.window2 = QtWidgets.QMainWindow()
        self.ui2 = Ui_DatapreviewWindow()
        self.ui2.setupUi(self.window2)
        self.ui2.pushButton_2.clicked.connect(self.reset_dimension_measure)

        self.window3 = QtWidgets.QMainWindow()
        self.ui3 = Ui_FilterdimensionWindow()
        self.ui3.setupUi(self.window3)
        self.ui3.confirm_button.clicked.connect(self.set_filter)

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
        self.statisticbtn.setText(_translate("MainWindow", "Plot"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Grid Table"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Graph"))
        self.clear_col_button.setText(_translate("MainWindow", "Clear Column"))
        self.clear_row_button.setText(_translate("MainWindow", "Clear Row"))
    

    def file_selected(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName()     # selected file
        if file_path != "":
            self.file_path = file_path
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
        if self.file_path != "":
            extension = self.file_path.split(".")[-1]
        else:
            return
        if extension == "csv":
            self.data = pd.read_csv(self.file_path, encoding="ISO-8859-1")
        elif extension == "xlsx":
            self.data = pd.read_excel(self.file_path, engine='openpyxl')
        if os.path.exists("metadata.json"):
            self.load_metadata()
            self.set_datetime_dimensions()
        else:
            self.setDimensionsMeasurements()    # auto set dimension/measurement
        self.set_listwidget()

    def setDimensionsMeasurements(self):
        self.dimensions = []
        self.measurements = []
        self.datetime_dimensions = []
        for col in self.data.columns:
            if self.is_datetime(col):
                self.dimensions.append(col)
                self.datetime_dimensions.append(col)
            elif self.data[col].dtypes == "O":
                self.dimensions.append(col)
            elif col.lower().find("id") >= 0:
                self.dimensions.append(col)
            elif col.lower().find("code") >= 0:
                self.dimensions.append(col)
            else:
                self.measurements.append(col)
        self.set_datetime_dimensions()
        self.save_metadata()

    def set_datetime_dimensions(self):
        for DATETIME in self.datetime_dimensions:
            datetime_date = pd.to_datetime(self.data[DATETIME], format="%d/%m/%Y")
            self.data[f"{DATETIME}(year)"] = datetime_date.dt.year
            self.data[f"{DATETIME}(month)"] = datetime_date.dt.month
            self.data[f"{DATETIME}(day)"] = datetime_date.dt.day

    def datetime_dimensions_show(self):
        for index in range(self.rowlist.count()):
            item = self.rowlist.item(index).text()
            if item in self.datetime_dimensions:
                self.rowlist.item(index).setText(f"{item}(year)")
        for index in range(self.columnlist.count()):
            item = self.columnlist.item(index).text()
            if item in self.datetime_dimensions:
                self.columnlist.item(index).setText(f"{item}(year)")
    
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ContextMenu and source is self.columnlist:
            self.index = source.currentIndex().row()
            if source.itemAt(event.pos()) != None:
                self.columnselected = True
                self.menu = QMenu()
                self.action = QtWidgets.QAction("Drill down")
                self.action2 = QtWidgets.QAction("Filter")
                self.menu.addAction(self.action)
                self.menu.addAction(self.action2)
                self.action.triggered.connect(self.drill_down)
                self.action2.triggered.connect(self.getcolumnlistindex)

                if self.menu.exec_(event.globalPos()):
                    item = source.itemAt(event.pos())
        if event.type() == QtCore.QEvent.ContextMenu and source is self.rowlist:
            self.index = source.currentIndex().row()
            if source.itemAt(event.pos()) != None:
                self.columnselected = False
                self.menu = QMenu()
                self.action = QtWidgets.QAction("Drill down")
                self.action2 = QtWidgets.QAction("Filter")
                self.menu.addAction(self.action)
                self.menu.addAction(self.action2)
                self.action.triggered.connect(self.drill_down)
                self.action2.triggered.connect(self.getrowlistindex)

                if self.menu.exec_(event.globalPos()):
                    item = source.itemAt(event.pos())
        
        if event.type() == QtCore.QEvent.ContextMenu and source is self.dimensionlist:
            if len(self.dimensionlist.selectedItems()) >= 2:
                self.menu = QMenu()
                self.action = QtWidgets.QAction("Add")
                self.action2 = QtWidgets.QAction("Delete")
                self.menu.addAction(self.action)
                self.menu.addAction(self.action2)
                self.action.triggered.connect(self.add_group_dimension)
                # self.action2.triggered.connect(self.getrowlistindex)

                if self.menu.exec_(event.globalPos()):
                    item = source.itemAt(event.pos())
        return super().eventFilter(source, event)
    
    
    def drill_down(self):
        if self.columnselected:
            item = self.columnlist.item(self.index).text()
        else:
            item = self.rowlist.item(self.index).text()
        if item.find("year") >= 0:
            item = item.replace("year", "month")
        elif item.find("month") >= 0:
            item = item.replace("month", "day")

        rowlist = self.get_rowlist()
        columnlist = self.get_columnlist()
        if item in rowlist+columnlist:
            return

        if self.columnselected:
            self.columnlist.insertItem(self.index+1,item)
        else:
            self.rowlist.insertItem(self.index+1,item)

    def drill_up(self):
        if self.columnselected:
            item = self.columnlist.item(self.index).text()
        else:
            item = self.rowlist.item(self.index).text()
        if item.find("year") >= 0:
            pass
        elif item.find("month") >= 0:
            pass
    
    def add_group_dimension(self):
        ITEM = ""
        for item in self.dimensionlist.selectedItems():
            ITEM += item.text() + ","
            #print(item.text())
        ITEM = ITEM[:-1]
        item = QtWidgets.QListWidgetItem(ITEM)
        self.dimensionlist.addItem(item)
        self.group_dimension.append(ITEM)
        print(self.group_dimension)
        
    def set_listwidget(self):
        self.dimensionlist.clear()
        self.measurementlist.clear()
        for dimensions in self.dimensions:
            self.dimensionlist.addItem(dimensions)
        for measurements in self.measurements:
            self.measurementlist.addItem(measurements)
    
    def load_metadata(self):
        metadata_json = open("metadata.json")
        metadata = json.load(metadata_json)
        file_name = self.file_path.split("/")[-1]
        if file_name in metadata.keys():
            md5 = hashlib.md5(open(self.file_path, "rb").read()).hexdigest()
            if md5 != metadata[file_name]["md5"]:
                self.setDimensionsMeasurements()
                return
            self.measurements = metadata[file_name]["measurements"]
            self.dimensions = metadata[file_name]["dimensions"]
            self.datetime_dimensions = metadata[file_name]["datetime"]
        else:
            self.setDimensionsMeasurements()

    def save_metadata(self):
        if os.path.exists("metadata.json"):
            metadata_json = open("metadata.json")
            metadata = json.load(metadata_json)
        else:
            metadata = {}
        file_name = self.file_path.split("/")[-1]
        md5 = hashlib.md5(open(self.file_path, "rb").read()).hexdigest()
        metadata[file_name] = {}
        metadata[file_name]["measurements"] = self.measurements
        metadata[file_name]["dimensions"] = self.dimensions
        metadata[file_name]["datetime"] = self.datetime_dimensions
        metadata[file_name]["md5"] = md5

        with open("metadata.json", 'w') as outfile:
            JSON = json.dumps(metadata, indent=4)
            outfile.write(JSON)

    def getcolumnlistindex(self):
        item = self.columnlist.currentItem().text()
        if item in self.measurements:
            self.index = self.columnlist.currentIndex().row()
            if type(self.columnlist.currentItem()) != Item:
                i = Item(item)
                self.columnlist.takeItem(self.index)
                self.columnlist.insertItem(self.index,i)
            self.columnselected = True
            self.secondwindow(self.index)
        elif item in self.dimensions:
            self.columnselected = True
            self.index = self.columnlist.currentIndex().row()
            self.filter_dimension_Window(self.index)
        for datetime in self.datetime_dimensions:
            if item.find(datetime) >= 0:
                self.columnselected = True
                self.index = self.columnlist.currentIndex().row()
                self.filter_dimension_Window(self.index)
                break

    def getrowlistindex(self):
        item = self.rowlist.currentItem().text()
        if item in self.measurements:
            self.index = self.rowlist.currentIndex().row()
            if type(self.rowlist.currentItem()) != Item:
                i = Item(item)
                self.rowlist.takeItem(self.index)
                self.rowlist.insertItem(self.index,i)
            self.columnselected = False
            self.secondwindow(self.index)
        elif item in self.dimensions:
            self.columnselected = False
            self.index = self.rowlist.currentIndex().row()
            self.filter_dimension_Window(self.index)
        for datetime in self.datetime_dimensions:
            if item.find(datetime) >= 0:
                self.columnselected = False
                self.index = self.rowlist.currentIndex().row()
                self.filter_dimension_Window(self.index)
                break
    
    def filter_dimension_Window(self,index):
        self.ui3.listWidget.clear()
        if self.columnselected:
            dimensions = self.columnlist.item(index).text()
        else:
            dimensions = self.rowlist.item(index).text()
        keys = self.data.groupby(dimensions).groups.keys()
        # check if it has been filtered before
        if dimensions in self.filter.keys():
            for key in keys:
                item = QtWidgets.QListWidgetItem(str(key))
                if str(key) in self.filter[dimensions]:
                    item.setCheckState(QtCore.Qt.Checked)
                else:
                    item.setCheckState(QtCore.Qt.Unchecked)
                self.ui3.listWidget.addItem(item)
        else:   # check all the checkbox if picking filter first time
            for key in keys:
                item = QtWidgets.QListWidgetItem(str(key))
                item.setCheckState(QtCore.Qt.Checked)
                self.ui3.listWidget.addItem(item)
        self.window3.show()
    
    def set_filter(self):
        filter = []
        for i in range(self.ui3.listWidget.count()):
            item = self.ui3.listWidget.item(i)
            if item.checkState() == 2:      # if checkbox is checked
                filter.append(item.text())
        if self.columnselected:
            index = self.columnlist.item(self.index).text()
        else:
            index = self.rowlist.item(self.index).text()
        self.filter[index] = filter
        self.window3.hide()


    def secondwindow(self, index):
        _translate = QtCore.QCoreApplication.translate
        if self.columnselected:
            measurement = self.columnlist.item(index).text()
        else:
            measurement = self.rowlist.item(index).text()
        self.ui.label.setText(_translate("SecondWindow",measurement))
        self.Min = self.data[measurement].min()
        self.Max = self.data[measurement].max()

        if measurement in self.measurement_filter.keys():
            min = self.measurement_filter[measurement]["min"]
            max = self.measurement_filter[measurement]["max"]
            min_pos = self.reverse_transform_range(min)
            max_pos = self.reverse_transform_range(max)
            self.ui.horizontalSlider.setLow(int(min_pos))
            self.ui.horizontalSlider.setHigh(int(max_pos))
            self.ui.checkBox.setCheckState(QtCore.Qt.Checked)
            self.ui.label_2.setText(_translate("SecondWindow", f"Min : {min}"))
            self.ui.label_3.setText(_translate("SecondWindow", f"Max : {max}"))
        else:
            self.ui.checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.ui.horizontalSlider.setLow(0)
            self.ui.horizontalSlider.setHigh(100)
            self.ui.label_2.setText(_translate("SecondWindow", f"Min : {self.Min}"))
            self.ui.label_3.setText(_translate("SecondWindow", f"Max : {self.Max}"))

        if measurement in self.MODE.keys():
            self.ui.comboBox.setCurrentText(self.MODE[measurement])
        else:
            self.ui.comboBox.setCurrentText(self.rowlist.item(index).mode)
        self.window.show()
    
    def update_minmax_label(self):
        min_value = self.ui.horizontalSlider.low()
        max_value = self.ui.horizontalSlider.high()
        # transform range
        Min_Value = self.transform_range(min_value)
        Max_Value = self.transform_range(max_value)

        _translate = QtCore.QCoreApplication.translate
        self.ui.label_2.setText(_translate("SecondWindow", f"Min : {Min_Value}"))
        self.ui.label_3.setText(_translate("SecondWindow", f"Max : {Max_Value}"))

    def set_measurement_filter(self):
        min_value = self.ui.horizontalSlider.low()
        max_value = self.ui.horizontalSlider.high()
        # transform range
        Min_Value = self.transform_range(min_value)
        Max_Value = self.transform_range(max_value)
        if self.columnselected:
            measurement = self.columnlist.item(self.index).text()
        else:
            measurement = self.rowlist.item(self.index).text()
        if self.ui.checkBox.checkState() == 2:
            self.measurement_filter[measurement] = {"min" : Min_Value, "max" : Max_Value}
            self.set_grid_table()   # reset grid table data
        else:
            self.measurement_filter.pop(measurement, None)
        self.ui.secondwindow.close()

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
        self.rowlist.clear()
        self.columnlist.clear()
        for dimension in self.dimensions:
            self.dimensionlist.addItem(dimension)
        for measurement in self.measurements:
            self.measurementlist.addItem(measurement)
        self.save_metadata()
        self.window2.hide()

    def get_dimensions(self):   # get dimensions from rowlist and columnlist
        dimensions = []
        for index in range(self.rowlist.count()):
            item = self.rowlist.item(index).text()
            if item in self.dimensions:
                dimensions.append(item)
                continue
            for datetime in self.datetime_dimensions:
                if item.find(datetime) >= 0:
                    dimensions.append(item)
                    break
        for index in range(self.columnlist.count()):
            item = self.columnlist.item(index).text()
            if item in self.dimensions:
                dimensions.append(item)
                continue
            for datetime in self.datetime_dimensions:
                if item.find(datetime) >= 0:
                    dimensions.append(item)
                    break
        dimensions = list(dict.fromkeys(dimensions))    # remove duplicates
        return dimensions

    def get_measurements(self):   # get measuments from rowlist and columnlist
        measurements = []
        for index in range(self.rowlist.count()):
            item = self.rowlist.item(index).text()
            if item in self.measurements:
                measurements.append(item)
        for index in range(self.columnlist.count()):
            item = self.columnlist.item(index).text()
            if item in self.measurements:
                measurements.append(item)
        measurements = list(dict.fromkeys(measurements))    # remove duplicates
        return measurements

    def get_rowlist(self): # get row from rowlist
        rowitems = []
        for index in range(self.rowlist.count()):
            item = self.rowlist.item(index).text()
            rowitems.append(item)
        return rowitems

    def get_columnlist(self): # get column from columnlist
        columnitem = []
        for index in range(self.columnlist.count()):
            item = self.columnlist.item(index).text()
            columnitem.append(item)
        return columnitem
    
    def get_agg(self, measurements): # get aggregrate (dict)
        agg = {}
        for measurement in measurements:
            if measurement not in self.MODE.keys():
                agg[measurement] = "sum"
                self.MODE[measurement] = "sum"
            else:
                agg[measurement] = self.MODE[measurement]
        return agg

    def set_grid_table(self):
        self.datetime_dimensions_show()
        dimensions = self.get_dimensions()
        measurements = self.get_measurements()

        # get aggregrate
        self.agg = self.get_agg(measurements)

        # clear previous table
        self.tableWidget.clear()

        filtered_data = self.get_filter_data()
        # insert data
        if len(dimensions) > 0 and len(measurements) > 0:
            data = filtered_data.groupby(dimensions, as_index=False).agg(self.agg)
            # set row,column count
            self.tableWidget.setRowCount(len(data.index.tolist()))
            self.tableWidget.setColumnCount(len(data.columns.tolist()))
            # set header
            for i, column in enumerate(data.columns.tolist()):
                if column in self.agg.keys():
                    item = QtWidgets.QTableWidgetItem(f"{self.agg[column]} of {column}")
                else:
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
        self.set_grid_table()
   
    def select_chart_type(self):
        self.chart_type = self.chart_list.currentIndex().row()

    def get_filter_data(self):
        query = '' 
        original_columns = self.data.columns
        self.data.columns = [column.replace(" ", "_") for column in self.data.columns]
        self.data.columns = [column.replace("-", "_") for column in self.data.columns]
        self.data.columns = [column.replace("(", "_") for column in self.data.columns]
        self.data.columns = [column.replace(")", "") for column in self.data.columns]
        # dimensions filter
        for key in self.filter:
            original_key = key
            key = key.replace(" ","_")
            key = key.replace("-","_")
            key = key.replace("(","_")
            key = key.replace(")","")
            query += f"{key} == ["
            for selected in self.filter[original_key]:
                if self.is_datetime(original_key):
                    query += f'{selected},'
                else:
                    query += f'"{selected}",'
            query += "] and "
        # measurements filter
        for key in self.measurement_filter:
            original_key = key
            key = key.replace(" ","_")
            key = key.replace("-","_")
            min = self.measurement_filter[key]["min"]
            max = self.measurement_filter[key]["max"]
            query += f"{key} >= {min} and {key} <= {max} and "
        if len(query) != 0:
            filtered_data = self.data.query(query[:-5])
            filtered_data.columns = original_columns
        else:
            filtered_data = self.data
        self.data.columns = original_columns
        return filtered_data

    def create_statistic(self):
        # get row columns
        dimensions = self.get_dimensions()
        measurements = self.get_measurements()
        columnitem = self.get_columnlist()
        if len(dimensions) == 0:
            return
        # get filtered data
        filtered_data = self.get_filter_data()
        # ploting
        if len(dimensions) == 1:
            alt_column = [alt.X, alt.Column, alt.Color]
            alt_row = [alt.Y, alt.Row, alt.Color]
        else:
            if dimensions[0] in columnitem:
                alt_column = [alt.Column, alt.X, alt.Color]
                alt_row = [alt.Y, alt.Row, alt.Color]
            else:
                alt_column = [alt.X, alt.Column, alt.Color]
                alt_row = [alt.Row, alt.Y, alt.Color]
        alt_plot = []
        tooltip = []
        PLOT = []
        for dimension in dimensions:
            if dimension in columnitem:
                alt_plot.append(alt_column[0](f"{dimension}:O"))
                alt_column.pop(0)
            else:
                alt_plot.append(alt_row[0](f"{dimension}:O"))
                alt_row.pop(0)
            tooltip.append(dimension)
        for measurement in measurements:
            data = filtered_data.groupby(dimensions,as_index=False).agg(self.agg)
            min_bar = 0
            max_bar = 0
            if min_bar > data[measurement].min() : min_bar = data[measurement].min()
            if max_bar < data[measurement].max() : max_bar = data[measurement].max()
            plt = alt_plot.copy()
            if measurement in columnitem:
                plt.append(alt_column[0](measurement,scale=alt.Scale(domain=(min_bar, max_bar), clamp=True)))
            else:
                plt.append(alt_row[0](measurement,scale=alt.Scale(domain=(min_bar, max_bar), clamp=True)))
            plt.append(alt.Tooltip(tooltip+[measurement]))
            if self.chart_type == 0:        # bar charts
                chart = (alt.Chart(data).mark_bar().encode(
                    *plt,
                    )
                    .resolve_scale(x="independent",y="independent")
                    .interactive()
                    .properties(title=f"{self.MODE[measurement]} of {measurement}")
                    .transform_filter(alt.FieldGTPredicate(field=str(measurement),gt=-1e10))
                )
                PLOT.append(chart)
            elif self.chart_type == 1:      # pie charts
                CHART = []
                for dimension in dimensions:
                    sub_chart = []
                    data = filtered_data.groupby(dimension,as_index=False).agg(self.agg)
                    BASE = alt.Chart(data).mark_arc().encode(
                        color=alt.Color(dimension)
                    )
                    for measurement in measurements:
                        base = BASE.encode(
                            theta=alt.Theta(measurement),
                            tooltip=alt.Tooltip([dimension,measurement])
                        )
                        sub_chart.append(base)
                    CHART.append(sub_chart)
            elif self.chart_type == 2:      # line charts
                chart = (alt.Chart(data).mark_line().encode(
                    *plt
                    )
                    .resolve_scale(x="independent",y="independent")
                    .interactive()
                    .properties(title=f"{self.MODE[measurement]} of {measurement}")
                ) 
                PLOT.append(chart)
        if len(measurements) > 0:
            if measurements[0] in columnitem:
                if self.chart_type == 1:
                    hchart = []
                    for sub_chart in CHART:
                        hchart.append(alt.hconcat(*sub_chart))
                    chart = alt.vconcat(*hchart)
                else:
                    chart = alt.hconcat(*PLOT)
            else:
                if self.chart_type == 1:
                    vchart = []
                    for sub_chart in CHART:
                        vchart.append(alt.vconcat(*sub_chart))
                    chart = alt.hconcat(*vchart)
                else:
                    chart = alt.vconcat(*PLOT)
            self.chart.updateChart(chart)   # plot chart

    def transform_range(self, value):
        NewRange = self.Max - self.Min
        return ((value * NewRange) / 100) + self.Min

    def reverse_transform_range(self, value):
        OldRange = self.Max - self.Min
        return (((value - self.Min) * 100) / OldRange)
    
    def is_datetime(self, word):
        if word.lower().find("date") >= 0:
            return True
        if word.lower().find("datetime") >= 0:
            return True
        else:
            return False
    

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
