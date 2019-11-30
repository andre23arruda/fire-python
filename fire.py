from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('QT5Agg')
from matplotlib.figure import Figure
import time

import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(995, 767)

        self.comecar_button = QtWidgets.QPushButton(Dialog)
        self.comecar_button.setGeometry(QtCore.QRect(240, 670, 151, 61))
        self.comecar_button.setObjectName("comecar_button")

        self.fire_slider = QtWidgets.QSlider(Dialog)
        self.fire_slider.setGeometry(QtCore.QRect(42, 60, 20, 531))
        self.fire_slider.setMinimum(40)
        self.fire_slider.setMaximum(100)
        self.fire_slider.setPageStep(10)
        self.fire_slider.setOrientation(QtCore.Qt.Vertical)
        self.fire_slider.setInvertedControls(False)
        self.fire_slider.setObjectName("fire_slider")

        self.wind_slider = QtWidgets.QSlider(Dialog)
        self.wind_slider.setGeometry(QtCore.QRect(100, 620, 851, 20))
        self.wind_slider.setMinimum(2)
        self.wind_slider.setMaximum(10)
        self.wind_slider.setPageStep(2)
        self.wind_slider.setProperty("value", 0)
        self.wind_slider.setOrientation(QtCore.Qt.Horizontal)
        self.wind_slider.setObjectName("wind_slider")

        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(100, 10, 851, 581))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("layout")

        self.parar_button = QtWidgets.QPushButton(Dialog)
        self.parar_button.setGeometry(QtCore.QRect(610, 670, 151, 61))
        self.parar_button.setObjectName("parar_button")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(820, 650, 120, 80))
        self.groupBox.setObjectName("groupBox")
        self.esquerda_button = QtWidgets.QRadioButton(self.groupBox)
        self.esquerda_button.setGeometry(QtCore.QRect(10, 20, 95, 20))
        self.esquerda_button.setChecked(True)
        self.esquerda_button.setObjectName("esquerda_button")
        self.direita_button = QtWidgets.QRadioButton(self.groupBox)
        self.direita_button.setGeometry(QtCore.QRect(10, 50, 95, 20))
        self.direita_button.setObjectName("direita_button")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(470, 600, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 20, 61, 31))
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setObjectName("label_2")

        self.decay_factor = 1.5
        self.wind_factor = 2
        self.fire = np.zeros([70, 100],dtype = 'uint8')

        self.figure = plt.figure()
        self.figure.patch.set_facecolor('k')
        self.img_canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.img_canvas)
        self.img_ax = self.img_canvas.figure.subplots()
        plt.subplots_adjust(left = 0.01, bottom = 0.01, right = 0.99, top = 0.99)

        self.img_ax.imshow(self.fire, cmap = 'hot', vmin = 0, vmax = 36, aspect = 'auto')
        self.img_ax.axis('off')
        self.img_ax.set_facecolor("black")

        self.timer = self.img_canvas.new_timer(100, [(self.createFire, (), {})])

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Fire Doom"))
        self.comecar_button.setText(_translate("Dialog", "Start"))
        self.parar_button.setText(_translate("Dialog", "Stop"))
        self.esquerda_button.setText(_translate("Dialog", "Left"))
        self.direita_button.setText(_translate("Dialog", "Right"))
        self.groupBox.setTitle(_translate("Dialog", "Wind side"))
        self.label.setText(_translate("Dialog", "Wind force"))
        self.label_2.setText(_translate("Dialog", "Fire Force"))

        self.fire_slider.valueChanged.connect(self.getFire)
        self.wind_slider.valueChanged.connect(self.getWind)

        self.comecar_button.clicked.connect(self.startFire)
        self.parar_button.clicked.connect(self.stopFire)


    def startFire(self):
        self.timer.start()

    def stopFire(self):
        self.timer.stop()

    def getFire(self):
        self.decay_factor = 11.5 - (self.fire_slider.value()/10)
        # print(self.decay_factor)

    def getWind(self):
        self.wind_factor = self.wind_slider.value()
        # print(self.wind_factor)

    def createFire(self):
        HEIGHT = 70
        WIDTH = 100
        self.fire[HEIGHT-1, :] = 36    

        for row in range(HEIGHT - 1):
            for col in range(WIDTH):

                decay_factor = self.decay_factor
                decay = np.int_(np.floor(np.random.rand() * decay_factor))

                if self.direita_button.isChecked():
                    col = WIDTH - 1 - col
                    col_index = (col + decay)%WIDTH
                    col2 = np.abs(col + 1 - np.random.randint(1, self.wind_factor))
                else:
                    col_index = col - decay
                    col2 = (col - 1 + np.random.randint(1, self.wind_factor))%WIDTH

                self.fire[HEIGHT - 2 - row, col_index] = np.clip(self.fire[HEIGHT - 1 - row, col2] - decay , 0, 36)

        self.img_ax.clear()        
        self.img_ax.imshow(self.fire, cmap = 'hot', vmin = 0, vmax = 36, aspect = 'auto')
        self.img_ax.axis('off')
        self.img_ax.figure.canvas.draw()
        # print('Deu bom')
        
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

