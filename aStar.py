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

def calH(start, target):
    count = 0
    for i in range(3):
        for j in range(3):
            v = start.state[i][j]
            for k in range(3):
                for l in range(3):
                    if v == target.state[k][l]:
                        count += abs(i -k) + abs(j - l)
    # for i in range(3):
    #     for j in range(3):
    #         if start.state[i][j] != 0 and start.state[i][j] != target.state[i][j]:
    #             count += 1
    return count


open = []
close = []

target = node()
target.state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
target.blank = 0

start = node()
start.state = [[7, 2, 4], [5, 0, 6], [8, 3, 1]]
start.blank = 4
start.g = 0
start.h = calH(start, target)
step = 0

def minNode(open):
    l = sorted(open)
    return open.pop(open.index(l[0]))

def canMove(a, b):
    return a >= 0 and a < 3 and b >= 0 and b < 3

def createChild(curNode):
    xtran = (-1, 0, 1, 0)
    ytran = (0, 1, 0, -1)
    x = curNode.blank // 3
    y = curNode.blank % 3
    result = []
    for i in range(4):
        nx = x + xtran[i]
        ny = y + ytran[i]

        if canMove(nx, ny):
            nextNode = node()
            nextNode.blank = nx * 3 + ny
            nextNode.state = copy.deepcopy(curNode.state)
            temp = nextNode.state[x][y]
            nextNode.state[x][y] = nextNode.state[nx][ny]
            nextNode.state[nx][ny] = temp
            nextNode.g = curNode.g + 1
            nextNode.h = calH(nextNode, target)
            nextNode.pre = curNode
            if not curNode.pre or nextNode != curNode.pre:
                result.append(nextNode)
    return result

def path(curNode):
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

def updateChild(curNode):
    #print('fuck you')
    #print (curNode.state)
    #time.sleep(5)
    if not curNode.next:
        return
    for p in curNode.next:
        if p in open:
            if curNode.g + 1 < p.g:
                p.g = curNode.g + 1
                p.pre = curNode
                # print('p:', p.g)
                # print('open[p]:', open[open.index(p)].g)
        elif p in close:
            if curNode.g + 1 < close[close.index(p)].g:
                p.g = curNode.g + 1
                p.pre = curNode
                # print('p:', p.g)
                # print('close[p]:', close[close.index(p)].g)
                updateChild(p)



if __name__ == '__main__':
    startTime = time.time()
    open.append(start)
    while len(open) > 0:
        curNode = minNode(open)
        close.append(curNode)
        if curNode.state == target.state:
            path(curNode)
            break
        if not curNode.next:
            nextNodes = createChild(curNode)
            curNode.next = nextNodes
        for p in curNode.next:
            if p in open:
                if p.g < open[open.index(p)].g:
                    #print('1')
                    open[open.index(p)].g = p.g
                    open[open.index(p)].pre = curNode
            elif p in close:
                if p.g < close[close.index(p)].g:
                    close[close.index(p)].g = p.g
                    close[close.index(p)].pre = p.pre
                    updateChild(close[close.index(p)])
            else:
                open.append(p)
    endTime = time.time()
    print ('step:', step)
    print ('time:', endTime - startTime)
    print ('Num of expanded:', len(close))
    print ('Num of generated:', len(open) + len(close))
