# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/andrew/Documents/workfolder/yandex_project/arc.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(806, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.add_folder_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_folder_button.setGeometry(QtCore.QRect(20, 40, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.add_folder_button.setFont(font)
        self.add_folder_button.setObjectName("add_folder_button")
        self.extarct_button = QtWidgets.QPushButton(self.centralwidget)
        self.extarct_button.setGeometry(QtCore.QRect(300, 40, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.extarct_button.setFont(font)
        self.extarct_button.setObjectName("extarct_button")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(20, 120, 541, 441))
        self.treeView.setObjectName("treeView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(585, 79, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(580, 120, 201, 441))
        self.listWidget.setObjectName("listWidget")
        self.update_inf_button = QtWidgets.QPushButton(self.centralwidget)
        self.update_inf_button.setGeometry(QtCore.QRect(750, 90, 21, 21))
        self.update_inf_button.setObjectName("update_inf_button")
        self.add_file_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_file_button.setGeometry(QtCore.QRect(160, 40, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.add_file_button.setFont(font)
        self.add_file_button.setObjectName("add_file_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 806, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Archiver"))
        self.add_folder_button.setText(_translate("MainWindow", "Add folder"))
        self.extarct_button.setText(_translate("MainWindow", "Extract all"))
        self.label.setText(_translate("MainWindow", "Recent archives"))
        self.update_inf_button.setText(_translate("MainWindow", "↻"))
        self.add_file_button.setText(_translate("MainWindow", "Add file"))

