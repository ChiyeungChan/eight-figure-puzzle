import myUi
from PyQt5 import QtWidgets, QtCore
import matplotlib.pyplot as plt
import sys
import aStarAlgorithm
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import networkx as nx

class MyCanvas(QWidget):
    def __init__(self, canvas_no, parent=None):
        super(MyCanvas, self).__init__(parent)
        self.canvas_no = canvas_no  # 这是pyplot的显示区编号
        self.figure1 = plt.figure(canvas_no)  # 指定到哪个pyplot显示区，并返回显示区，初始化时使用返回值绑定到画布
        self.canvas1 = FigureCanvas(self.figure1) # 添加画布并绑定显示区
        self.layout = QHBoxLayout(self) # 建立这个Widget中的框架
        self.layout.addWidget(self.canvas1)     # 画布添加到框架

        #   networkx的画图属性
        self.options = {
            'node_color': 'black',
            'node_size': 1,
            'width':0.5,
        #    'node_shape' : 's',
            'alpha' : 0.5,
            'font_size':7,
            'with_labels':True,
        }

    # 刷新（重绘）画布
    def update_figure(self, G, root, graphon = 1):
        self.figure1 = plt.figure(self.canvas_no)  # 回到自己的显示区
        plt.clf()   # 清空显示区
        if(graphon == 0):
            self.canvas1.draw()
            return

        # 一系列步骤创造networkx图的点的排列方式
        shellLay = [[root]]
        tmp = [root]
        close = tmp
        while len(tmp) != 0:
            thisLay = [[j for j in nx.all_neighbors(G, i)] for i in tmp]
            shellLay.append([])
            for i in thisLay:
                shellLay[-1] += i
            for i in close:
                while i in shellLay[-1]:
                    shellLay[-1].remove(i)
            tmp = shellLay[-1]
            if len(shellLay[-1]) <= 1:
                shellLay[-2] += shellLay[-1]
                shellLay.remove(shellLay[-1])
            close += tmp

        #   画图，指定点排列，指定画图属性
        nx.draw_shell(G, nlist=shellLay, **self.options)
        self.canvas1.draw()

class Window(myUi.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        
        self.initTextEdit = []
        self.initTextEdit.append(self.initTextEdit_1)
        self.initTextEdit.append(self.initTextEdit_2)
        self.initTextEdit.append(self.initTextEdit_3)
        self.initTextEdit.append(self.initTextEdit_4)
        self.initTextEdit.append(self.initTextEdit_5)
        self.initTextEdit.append(self.initTextEdit_6)
        self.initTextEdit.append(self.initTextEdit_7)
        self.initTextEdit.append(self.initTextEdit_8)
        self.initTextEdit.append(self.initTextEdit_9)

        self.targetTextEdit = []
        self.targetTextEdit.append(self.targetTextEdit_1)
        self.targetTextEdit.append(self.targetTextEdit_2)
        self.targetTextEdit.append(self.targetTextEdit_3)
        self.targetTextEdit.append(self.targetTextEdit_4)
        self.targetTextEdit.append(self.targetTextEdit_5)
        self.targetTextEdit.append(self.targetTextEdit_6)
        self.targetTextEdit.append(self.targetTextEdit_7)
        self.targetTextEdit.append(self.targetTextEdit_8)
        self.targetTextEdit.append(self.targetTextEdit_9)

        
        #启发函数，h1为0，h2为1，默认选择h1
        self.algorithm = 0
        self.radioButtonH1.setChecked(True)

        #另一个线程进行计算
        #self.astarThread = aStarThread()
        self.astar = aStarAlgorithm.aStar()
        for i, j in enumerate(self.initTextEdit):
            j.setText(str(self.astar.start.state[i//3][i%3]))

        for i, j in enumerate(self.targetTextEdit):
            j.setText(str(self.astar.target.state[i//3][i%3]))
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        #添加画布
        self.canvas = MyCanvas(1, self)
        self.imgLayout = QHBoxLayout()
        self.imgLayout.addWidget(self.canvas)
        self.imgWidget.setLayout(self.imgLayout)
        
        self.G = nx.Graph()
        self.buildUpConnect()
        self.show()

    def buildUpConnect(self):
        self.radioButtonH1.toggled.connect(self.changeAlgorithm)
        self.radioButtonH2.toggled.connect(self.changeAlgorithm)
        self.startButton.clicked.connect(self.startMission)

    def changeAlgorithm(self):
        sender = self.sender()
        if sender == self.radioButtonH1:
            self.algorithm = 0
        else:
            self.algorithm = 1

    def update(self):
        if not self.astar.isFinish:
            newNode = self.astar.run()
            self.resultTextEdit.append(newNode.toStr2() + '\t\t%8d\n' % (len(self.astar.open)))
            self.G.add_node(newNode.toStr())
            if newNode.pre is not None:
                self.G.add_edge(newNode.toStr(), newNode.pre.toStr())
            self.canvas.update_figure(self.G, self.astar.start.toStr())
        else:
            self.timer.stop()
            self.resultTextEdit.append(self.astar.path())
            self.startButton.setEnabled(True)


    def startMission(self):

        for i, c in enumerate(self.targetTextEdit):
            x = i // 3
            y = i % 3
            self.astar.target.state[x][y] = int(c.toPlainText())
            if int(c.toPlainText()) == 0:
                self.astar.target.blank = i

        for i, c in enumerate(self.initTextEdit):
            x = i // 3
            y = i % 3
            self.astar.start.state[x][y] = int(c.toPlainText())
            if int(c.toPlainText()) == 0:
                self.astar.start.blank = i

        self.astar.start.h = self.astar.calH(self.astar.start, self.astar.target, self.algorithm)
        self.astar.algorithm = self.algorithm
        self.astar.initOpen()
        self.G.clear()
        self.G.add_node(self.astar.start.toStr())
        self.canvas.update_figure(self.G, self.astar.start.toStr())
        self.resultTextEdit.clear()
        if self.astar.canSolve():
            self.startButton.setEnabled(False)
            self.timer.start(200)
        else:
            self.resultTextEdit.append('无解\n')
        
        


class aStarThread(QThread):
    def __init__(self, parent=None):
        super(aStarThread,self).__init__(parent)  
        self.astar = aStarAlgorithm.aStar()

    def run(self):
        self.astar.run()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())