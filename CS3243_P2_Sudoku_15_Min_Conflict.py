from random import choice
import sys
import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        self.fixed = set()

    def solve(self):
        # TODO: Write your code here
        self.initialise()
        self.randomiseStartState()
        self.minConflicts()
        # self.ans is a list of lists
        return self.ans

    def initialise(self):
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] != 0:
                    self.fixed.add((row, col))
                else:
                    puzzle[row][col] = set()
                    puzzle[row][col].add(1)
                    puzzle[row][col].add(2)
                    puzzle[row][col].add(3)
                    puzzle[row][col].add(4)
                    puzzle[row][col].add(5)
                    puzzle[row][col].add(6)
                    puzzle[row][col].add(7)
                    puzzle[row][col].add(8)
                    puzzle[row][col].add(9)

    def randomiseStartState(self):
        for row in range(9):
            for col in range(9):
                if (row, col) not in self.fixed:
                    # reduce domains by sudoku rules
                    self.reduceDomain((row, col))
                    # randomly choose 1 value from the domain
                    puzzle[row][col] = choice(list(puzzle[row][col]))

    def reduceDomain(self, coord):
        # reduce domain by sudoku rules
        for fixedCoord in self.fixed:
            if self.isInSameSpace(coord, fixedCoord):
                # need to remove val from domain
                valOfFixedCoord = puzzle[fixedCoord[0]][fixedCoord[1]]
                if valOfFixedCoord in puzzle[coord[0]][coord[1]]:
                    puzzle[coord[0]][coord[1]].remove(valOfFixedCoord)

    def isInSameSpace(self, coord1, coord2):
        # checks if both coords have the same row or col
        if coord1[0] == coord2[0] or coord1[1] == coord2[1]:
            return True
        else:
            # checks if both coords are in the same region
            if self.getBoxVal(coord1) == self.getBoxVal(coord2):
                return True
            else:
                return False

    def getBoxVal(self, coord):
        sum = 0
        for i in range(2):
            val = coord[i]
            if (val > 2):
                if (val < 6):
                    sum = sum + 1
                else:
                    sum = sum + 2
            if i == 0:
                sum = sum * 3
        return sum

    def numOfConflicts(self, coord):
        row = coord[0]
        col = coord[1]
        val = puzzle[row][col]
        num = 0
        # check row, col and region
        for i in range(9):
            if self.isInSameSpace((row, i), coord) and i != col and val == puzzle[row][i]:
                num = num + 1
            if self.isInSameSpace((i, col), coord) and i != row and val == puzzle[i][col]:
                num = num + 1

        boxVal = self.getBoxVal(coord)
        rStart = -1
        cStart = (boxVal % 3) * 3
        if boxVal < 3:
            rStart = 0
        elif boxVal < 6:
            rStart = 3
        elif boxVal >= 5:
            rStart = 6
        for r in range(rStart, rStart + 3):
            for c in range(cStart, cStart + 3):
                if c != col and r != row and val == puzzle[r][c] and self.isInSameSpace((r, c), coord):
                    num = num + 1
        return num

    def getVarWithConflict(self):
        # returns a random conflicted var
        Range = [(r, c) for r in range(9) for c in range(9)]
        while Range:
            pos = choice(Range)
            if pos in self.fixed:
                Range.remove(pos)
                continue
            if self.numOfConflicts(pos) > 0:
                return pos
            else:
                Range.remove(pos)
        return -1

    def assignVal(self, pos):
        # get val => val should be chosen such that it causes least conflicts
        # ties are broken randomly
        curMinVal = self.puzzle[pos[0]][pos[1]]
        curMin = self.numOfConflicts(pos)
        ls = [curMinVal]
        for x in range(9):
            self.puzzle[pos[0]][pos[1]] = x + 1
            if self.numOfConflicts(pos) < curMin:
                curMin = self.numOfConflicts(pos)
                curMinVal = x + 1
                ls = [curMinVal]
            elif self.numOfConflicts(pos) == curMin:
                ls.append(x + 1)
        # update the pos with new min val
        self.puzzle[pos[0]][pos[1]] = choice(ls)

    def minConflicts(self):
        numOfIteration = 100000
        for i in range(numOfIteration):
            varWithConflict = self.getVarWithConflict()
            if varWithConflict == -1:
                self.ans = self.puzzle
                print("done!")
                break

            # else get the value which will be assigned
            # value should be chosen such that it causes least conflicts
            # ties are broken randomly
            # update state
            else:
                self.assignVal(varWithConflict)
                if (i % 10000 == 0):
                    print("iteration " + str(i) + ":")
                    self.printSudoku()

    def printSudoku(self):
        print(puzzle[0])
        print(puzzle[1])
        print(puzzle[2])
        print(puzzle[3])
        print(puzzle[4])
        print(puzzle[5])
        print(puzzle[6])
        print(puzzle[7])
        print(puzzle[8])
        print("")

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
