# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'orientationGui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1397, 717)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.overviewWidget = QtWidgets.QWidget(self.centralwidget)
        self.overviewWidget.setGeometry(QtCore.QRect(30, 20, 301, 301))
        self.overviewWidget.setObjectName("overviewWidget")
        self.zoomWidget = QtWidgets.QWidget(self.centralwidget)
        self.zoomWidget.setGeometry(QtCore.QRect(360, 20, 301, 301))
        self.zoomWidget.setObjectName("zoomWidget")
        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setGeometry(QtCore.QRect(30, 460, 113, 32))
        self.resetButton.setObjectName("resetButton")
        self.markerTable = QtWidgets.QTableWidget(self.centralwidget)
        self.markerTable.setGeometry(QtCore.QRect(30, 350, 301, 101))
        self.markerTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.markerTable.setObjectName("markerTable")
        self.markerTable.setColumnCount(0)
        self.markerTable.setRowCount(0)
        self.markerWidget = QtWidgets.QWidget(self.centralwidget)
        self.markerWidget.setGeometry(QtCore.QRect(690, 20, 301, 301))
        self.markerWidget.setObjectName("markerWidget")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(220, 460, 113, 32))
        self.saveButton.setObjectName("saveButton")
        self.skipButton = QtWidgets.QPushButton(self.centralwidget)
        self.skipButton.setGeometry(QtCore.QRect(220, 490, 113, 32))
        self.skipButton.setObjectName("skipButton")
        self.rotatedWidget = QtWidgets.QWidget(self.centralwidget)
        self.rotatedWidget.setGeometry(QtCore.QRect(1020, 20, 301, 301))
        self.rotatedWidget.setObjectName("rotatedWidget")
        self.imageTable = QtWidgets.QTableWidget(self.centralwidget)
        self.imageTable.setGeometry(QtCore.QRect(360, 350, 301, 301))
        self.imageTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.imageTable.setObjectName("imageTable")
        self.imageTable.setColumnCount(0)
        self.imageTable.setRowCount(0)
        self.processedWidget = QtWidgets.QWidget(self.centralwidget)
        self.processedWidget.setGeometry(QtCore.QRect(1020, 350, 301, 301))
        self.processedWidget.setObjectName("processedWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1397, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cigar tomography orientation fixer"))
        self.resetButton.setText(_translate("MainWindow", "Reset marker"))
        self.saveButton.setText(_translate("MainWindow", "Save && next"))
        self.skipButton.setText(_translate("MainWindow", "Skip"))

