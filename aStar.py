import copy
import time

class node:
   
    def __init__(self):
        self.state = []
        self.blank = 0
        self.g = 0
        self.h = 0
        self.pre = None
        self.next = None

    def __eq__(self, other):
        if self.state != other.state:
            return False
        return True

    def __lt__(self, other):
        return self.h + self.g < other.h + other.g

    def __le__(self, other):
        return self.h + self.g <= other.h + other.g

class aStar:

    def __init__(self):
        self.open = []  #open表
        self.close = [] #close表
        self.step = 0 #总步数
        self.algorithm = 1 #启发函数
        self.optNode = None #最优节点

        self.target = node() #目标状态
        self.target.state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.target.blank = 0

        self.start = node() #初始状态
        self.start.state = [[7, 2, 4], [5, 0, 6], [8, 3, 1]]
        self.start.blank = 4
        self.start.g = 0
        self.start.h = self.calH(self.start, self.target, self.algorithm)
        
        

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

    def path(self, curNode):
        l = []
        while (curNode):
            l.append(curNode)
            curNode = curNode.pre
        global step
        step = len(l)

        while (l):
            i = l.pop()
            for j in i.state:
                print (j)
            print('---------')

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

    def run(self):
        startTime = time.time()
        self.open.append(self.start)
        while len(self.open) > 0:
            curNode = self.minNode()
            self.optNode = curNode
            self.close.append(curNode)
            if curNode.state == self.target.state:
                #self.path(curNode)
                break
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
        endTime = time.time()    

if __name__ == '__main__':
    a = aStar()
    a.run()
    # print ('step:', step)
    # print ('time:', endTime - startTime)
    # print ('Num of expanded:', len(close))
    # print ('Num of generated:', len(open) + len(close))
