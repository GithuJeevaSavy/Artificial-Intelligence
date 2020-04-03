
class KnightTour:

    m_x = 0
    n_y = 0
    steps = 0
    position = (0, 0)
    moves = []
    po_map = {}
    po_stack = []

    def __init__(self, m, n, startpo):
        self.m_x = m
        self.n_y = n
        self.steps = 0
        self.position = startpo

        self.moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                      (-2, -1), (-1, -2), (1, -2), (2, -1)]

        for j in range(n-1, -1, -1):
            for i in range(0, m):
                temppo = (i, j)
                tempnum = 0
                self.po_map[temppo] = tempnum
        
    def printboard(self):
        for j in range(self.n_y - 1, -1, -1):
            row = ""
            for i in range(0, self.m_x):
                temppo = (i, j)
                row = row + str(self.po_map[temppo]) + ", "
            print(row)

    def inboard(self, po):
        if (po[0] < 0 or po[0] >= self.m_x or po[1] < 0 or po[1] >= self.n_y):
            return False
        else:
            return True

    def validstep(self, po):
        if self.po_map[po] == 0:
            return True
        else:
            return False

    def adjnum(self, po):
        num = 0
        for i in self.moves:
            newx = po[0] + i[0]
            newy = po[1] + i[1]
            if (self.inboard((newx, newy)) and self.validstep((newx, newy))):
                num = num + 1
        return num

    def sort_pairnum(self, x):
        return x['num']

    def SortAdj(self):
        pairnum = {}
        pairnum_list = []

        for i in self.moves:
            newx = self.position[0] + i[0]
            newy = self.position[1] + i[1]
            newpair = (newx, newy)
            if (self.inboard(newpair) and self.validstep(newpair)):
                newnum = self.adjnum(newpair)
                newpairnum = {}
                newpairnum['ipair'] = newpair
                newpairnum['num'] = newnum
                pairnum_list.append(newpairnum)

        pairnum_list.sort(key=self.sort_pairnum)

        SAdj = []
        for n in pairnum_list:
            SAdj.append(n['ipair'])
        return SAdj

    def DFSTour(self):
        self.steps = self.steps+1
        self.po_map[self.position] = self.steps
        self.po_stack.append(self.position)
        #flag = False
        if self.steps < self.m_x*self.n_y:
            flag = False
            adj_list = self.SortAdj()

            if len(adj_list) != 0:
                for i in adj_list:
                    if(flag == False):
                        self.position = i
                        flag = self.DFSTour()
                    else:
                        break

            if flag == False:
                self.steps = self.steps - 1
                if (self.steps == 0):
                    return flag
                self.po_map[self.position] = 0
                self.po_stack.pop()
                self.position = po_stack[-1]
        else:
            flag = True

        return flag


col = int(input("columns on board: "))
row = int(input("rows on board: "))
col_s = int(input("starting column (1 - " + str(col) + "): "))
col_s = col_s - 1
row_s = int(input("starting row (1 - " + str(row) + "): "))
row_s = row_s - 1

knightTour = KnightTour(col, row, (col_s, row_s))

possible = knightTour.DFSTour()
if possible:
    print("Knight's Tour is possible.")
    knightTour.printboard()
else:
    print("Knight's Tour is not possible.")
