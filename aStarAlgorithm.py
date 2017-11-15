import copy
import time
import networkx as nx
import matplotlib.pyplot as plt
import queue
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets,QtCore 
import sys 
class node:
   
    def __init__(self):
        self.state = []
        self.blank = 0
        self.g = 0
        self.h = 0
        self.pre = None
        self.next = []

    def toStr(self):
        result = ''
        for i in range(3):
            for j in range(3):
                result += str(self.state[i][j])
                result += ' '
            result += '\n'
        return result

    def toStr2(self):
        result = ''
        state = ''
        for i in range(3):
            for j in range(3):
                result += str(self.state[i][j])
                result += ' '
            if i != 2:
                result += '\n'
        result += '\t\t%5d\t\t%6d' % (self.h, self.g + self.h)
        return result

    def toOneLineStr(self):
        result = ''
        for i in range(3):
            for j in range(3):
                result += str(self.state[i][j])
        return result

    def __eq__(self, other):
        if self.state != other.state:
            return False
        return True

    def __lt__(self, other):
        return self.h + self.g < other.h + other.g

    def __le__(self, other):
        return self.h + self.g <= other.h + other.g

    def getNixuNum(self):
        sum = 0
        state = self.toOneLineStr()
        for i in range(9):
            for j in range(i+1, 9):
                if state[i] != '0' and state[j] != '0' and state[j] < state[i]:
                    sum += 1
        return sum


class aStar:
    
    def __init__(self):
        self.open = []  #open表
        self.close = [] #close表
        self.step = 0 #总步数
        self.algorithm = 1 #启发函数
        

        self.target = node() #目标状态
        self.target.state = [[8, 1, 2], [7, 6, 3], [5, 4, 0]]
        self.target.blank = 8

        self.start = node() #初始状态
        self.start.state = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
        self.start.blank = 4
        self.start.g = 0
        self.start.h = self.calH(self.start, self.target, self.algorithm)
        
        self.optNode = self.start #最优节点

        self.isFinish = 0

    #根据启发函数计算h的值
    def calH(self, start, target, algorithm):
        count = 0
        if algorithm:
            for i in range(3):
                for j in range(3):
                    v = start.state[i][j]
                    for k in range(3):
                        for l in range(3):
                            if v == target.state[k][l]:
                                count += abs(i -k) + abs(j - l)
        else:
            for i in range(3):
                for j in range(3):
                    if start.state[i][j] != 0 and start.state[i][j] != target.state[i][j]:
                        count += 1
        return count

    def minNode(self):
        l = sorted(self.open)
        return self.open.pop(self.open.index(l[0]))

    def canMove(self, a, b):
        return a >= 0 and a < 3 and b >= 0 and b < 3

    def canSolve(self):
        return self.start.getNixuNum() % 2 == self.target.getNixuNum() % 2
        

    def createChild(self, curNode):
        xtran = (-1, 0, 1, 0)
        ytran = (0, 1, 0, -1)
        x = curNode.blank // 3
        y = curNode.blank % 3
        result = []
        for i in range(4):
            nx = x + xtran[i]
            ny = y + ytran[i]

            if self.canMove(nx, ny):
                nextNode = node()
                nextNode.blank = nx * 3 + ny
                nextNode.state = copy.deepcopy(curNode.state)
                temp = nextNode.state[x][y]
                nextNode.state[x][y] = nextNode.state[nx][ny]
                nextNode.state[nx][ny] = temp
                nextNode.g = curNode.g + 1
                nextNode.h = self.calH(nextNode, self.target, self.algorithm)
                nextNode.pre = curNode
                if not curNode.pre or nextNode != curNode.pre:
                    result.append(nextNode)
        return result

    def path(self):
        l = []
        while (self.optNode):
            l.append(self.optNode)
            self.optNode = self.optNode.pre
        self.step = len(l)

        result = '最优路径：\n\n'

        while (l):
            i = l.pop()
            result += i.toStr()
            result += '\n'
        result += "步数：%d" % (self.step-1)
        return result
        #G = nx.Graph()
        
        # n1 = l.pop()
        # G.add_node(n1.toStr())
        # while l:
        #     n2 = l.pop()
        #     for i in n1.next:
        #         if i in self.close:
        #             G.add_edge(n2.toStr(), i.toStr())
        #     G.add_edge(n1.toStr(), n2.toStr())
        #     print(len(n1.next))
            
        #     n1 = n2

        # q = queue.Queue()
        # q.put(self.start)
        # while not q.empty():
        #     temp = q.get()
        #     for i in temp.next:
        #         if i in self.close:
        #             G.add_edge(temp.toStr(), i.toStr())
        #             q.put(i)

        # pos = nx.spectral_layout(G)
        # nx.draw_shell(G, with_labels=True, node_color = 'w')
        # plt.show()
        


    def updateChild(self, curNode):
        #print('fuck you')
        #print (curNode.state)
        #time.sleep(5)
        if not curNode.next:
            return
        for p in curNode.next:
            if p in self.open:
                if curNode.g + 1 < p.g:
                    p.g = curNode.g + 1
                    p.pre = curNode
                    # print('p:', p.g)
                    # print('open[p]:', open[open.index(p)].g)
            elif p in self.close:
                if curNode.g + 1 < self.close[self.close.index(p)].g:
                    p.g = curNode.g + 1
                    p.pre = curNode
                    # print('p:', p.g)
                    # print('close[p]:', close[close.index(p)].g)
                    self.updateChild(p)

    def initOpen(self):
        self.isFinish = 0
        self.close.clear()
        self.open.clear()
        self.start.next = []
        self.open.append(self.start)

    def run(self):
        #startTime = time.time()
        #self.open.append(self.start)
        #while len(self.open) > 0:
        curNode = self.minNode()
        self.optNode = curNode
        self.close.append(curNode)
        if curNode.state == self.target.state:
            #self.path(curNode)
            self.optNode = curNode
            self.isFinish = 1
        if not curNode.next:
            nextNodes = self.createChild(curNode)
            curNode.next = nextNodes
        for p in curNode.next:
            if p in self.open:
                if p.g < self.open[self.open.index(p)].g:
                    #print('1')
                    self.open[self.open.index(p)].g = p.g
                    self.open[self.open.index(p)].pre = curNode
            elif p in self.close:
                if p.g < self.close[self.close.index(p)].g:
                    self.close[self.close.index(p)].g = p.g
                    self.close[self.close.index(p)].pre = p.pre
                    self.updateChild(self.close[self.close.index(p)])
            else:
                self.open.append(p)
        if len(self.open) == 0:
            self.isFinish = 1
        return curNode
        #endTime = time.time()    

if __name__ == '__main__':
    a = aStar()
    a.run()
    # print ('step:', step)
    # print ('time:', endTime - startTime)
    # print ('Num of expanded:', len(close))
    # print ('Num of generated:', len(open) + len(close))
