import sys
import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.fixed = set()
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        # Each node is a cell on the sudoku
        # When we add the arcs into the ac3, the node-node refers to the relation between two cells

    def solve(self):
        # TODO: Write your code here
        self.initialise()
        self.backtrack(puzzle)
        # self.ans is a list of lists
        return self.ans

    def initialise(self):
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] != 0:
                    set_values = {puzzle[row][col]}
                    puzzle[row][col] = set_values
                    self.fixed.add((row, col))
                #else:
                #    puzzle[row][col] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] == 0: # Find the empty cells
                    possible_values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
                    for same_row_col in range(9):
                        if (row, same_row_col) in self.fixed:
                            value_to_remove = list(puzzle[row][same_row_col])[0]
                            if value_to_remove in possible_values:
                                possible_values.remove(value_to_remove)
                    for same_col_row in range(9):
                        if (same_col_row, col) in self.fixed:
                            value_to_remove = list(puzzle[same_col_row][col])[0]
                            if value_to_remove in possible_values:
                                possible_values.remove(value_to_remove)                    
                    top_row_in_box = int(row / 3) * 3
                    top_col_in_box = int(col / 3) * 3
                    for same_box_row_value in range(top_row_in_box, top_row_in_box + 3):
                        for same_box_col_value in range(top_col_in_box, top_col_in_box + 3):
                             if (same_box_row_value, same_box_col_value) in self.fixed:
                                value_to_remove = list(puzzle[same_box_row_value][same_box_col_value])[0]
                                if value_to_remove in possible_values:
                                        possible_values.remove(value_to_remove)
                    self.puzzle[row][col] = possible_values
                    
                    #for same_row_value in range(9):
                     #   print("Same row value:")
                      #  print(same_row_value)
                       # if self.puzzle[row][same_row_value] in possible_values:
                        #    print("Removing above value")
                         #   possible_values.remove(self.puzzle[row][same_row_value])
                    #for same_col_value in range(9):
                     #   if self.puzzle[same_col_value][col] in possible_values:
                      #      possible_values.remove(self.puzzle[same_col_value][col])
                    #top_row_in_box = int(row / 3) * 3
                    #top_col_in_box = int(col / 3) * 3
                    #for same_box_row_value in range(top_row_in_box, top_row_in_box + 3):
                     #   for same_box_col_value in range(top_col_in_box, top_col_in_box + 3):
                      #      if self.puzzle[same_box_row_value][same_box_col_value] in possible_values:
                       #         possible_values.remove(puzzle[same_box_row_value][same_box_col_value])
                    #self.puzzle[row][col] = possible_values
                    print("Initialising")
                    print((row, col))
                    print(self.puzzle[row][col])
                #else :
                 #   set_values = {puzzle[row][col]}
                  #  puzzle[row][col] = set_values
                   # self.fixed.add((row, col))

    # In this problem, we are ensured that the puzzle is valid and well-formed.
    def find_mrv(self):
        mrv = 10
        mrv_position = None
        for row in range(9):
            for col in range(9):
                possible_values = puzzle[row][col]
                if len(possible_values) < mrv and (row, col) not in self.fixed:
                    mrv = len(possible_values)
                    mrv_position = (row, col)
        return mrv_position
                    
    # Model the problem such that we are able to see the available domains
    # Put it as a a dictionary, key is a tuple of the position, the values is a list of the possible values
    # At first, we will run ac3 to find the initial possible domains of everything. When we do this, we can find the smallest 
    # domain item as a variable and use it next (Most constrained value MRV Heuristics)
    # Select this variable and assign it the first value in the domain
    # Repeats ac3 to revise and find all possible domains again. If any of this domain becomes empty, failure, choose another value
    # else continue until it is all done. Do this is a recursion call to backtrack again with the new puzzle 

    
    # Does backtrack first
    # If assignment is complete, return assignment
    # Use one of the heuristic to select the first variable
    # Dict is a dictionary of all the arcs and its possible domain values
    def backtrack(self, puzzle):
        if self.puzzle_is_completed(puzzle):
            #print("Checking is puzzle is complete")
            return puzzle
        mrv_row, mrv_col = self.find_mrv()
        mrv_values = puzzle[mrv_row][mrv_col]
        i = 0
        for value in mrv_values:
            i += 1
            print("im here for the")
            print(i)
            print("times")
            print("value is")
            print(value)
            current_value_failed = False
            #print("Iterating through all the values in MRV values. MRV position:")
            #print(mrv_row, mrv_col)
            #print("Current Value:")
            #print(value)
            self.check_consistent(puzzle, (mrv_row, mrv_col), value)
            current_puzzle = copy.deepcopy(puzzle)
            current_puzzle[mrv_row][mrv_col] = {value}
            print("What is the current puzzle value assigned?")
            print((mrv_row,mrv_col))
            print(current_puzzle[mrv_row][mrv_col])
            if not self.ac3(current_puzzle, (mrv_row, mrv_col)):
                continue
            #for same_row_col in range(9):
             #   if mrv_col != same_row_col:
              #      if not self.ac3(current_puzzle, (mrv_row, same_row_col)):
               #         current_value_failed = True
            #if current_value_failed:
             #   continue
            #for same_col_row in range(9):
             #   if mrv_row != same_col_row:
              #      if not self.ac3(current_puzzle, (same_col_row, mrv_col)):
               #         current_value_failed = True
            #if current_value_failed:
             #   continue
            #top_row_in_box = int(mrv_row / 3) * 3
            #top_col_in_box = int(mrv_col / 3) * 3
            #for same_box_row_value in range(top_row_in_box, top_row_in_box + 3):
             #   for same_box_col_value in range(top_col_in_box, top_col_in_box + 3):
              #      if same_box_row_value != mrv_row and same_box_col_value != mrv_col:
               #         if not self.ac3(current_puzzle, (same_box_row_value, same_box_col_value)):
                #            current_value_failed = True
            #if current_value_failed:
             #   continue
            print("True that it is ac3")
            new_puzzle = copy.deepcopy(current_puzzle)
            if self.backtrack(new_puzzle):
                return True
        return False

    def check_consistent(self, puzzle, position, value):
        mrv_row, mrv_col = position
        for same_row_col in range(9):
            if mrv_col != same_row_col:
                if len(puzzle[mrv_row][same_row_col]) == 1 and value in puzzle[mrv_row][same_row_col]:
                    return False
        for same_col_row in range(9):
            if mrv_row != same_col_row:
                if len(puzzle[same_col_row][mrv_col]) == 1 and value in puzzle[same_col_row][mrv_col]:
                    return False
        top_row_in_box = int(mrv_row / 3) * 3
        top_col_in_box = int(mrv_col / 3) * 3
        for same_box_row_value in range(top_row_in_box, top_row_in_box + 3):
            for same_box_col_value in range(top_col_in_box, top_col_in_box + 3):
                if same_box_row_value != mrv_row and same_box_col_value != mrv_col:
                    if len(puzzle[same_box_row_value][same_box_col_value]) == 1 and value in puzzle[same_box_row_value][same_box_col_value]:
                        return False
        return True

    # When we call this function, there are already previous checks for whether the assignment is correct.
    # Hence, no need to do so again
    def puzzle_is_completed(self, puzzle):
        for row in range(9):
            for col in range(9):
                if len(puzzle[row][col]) != 1:
                    return False
        return True

    # Over here, we have a queue of all the possible arcs (i.e. position of the current box we are looking at) (Inference)
    # Pop first item from queue, 
    def ac3(self, puzzle, position):
        queue = []
        row, col = position
        for same_row_col in range(9):
            if col != same_row_col:
                queue.append((row, same_row_col))
        for same_col_row in range(9):
            if row != same_col_row:
                queue.append((same_col_row, col))
        top_row_in_box = int(row / 3) * 3
        top_col_in_box = int(col / 3) * 3
        for same_box_row_value in range(top_row_in_box, top_row_in_box + 3):
            for same_box_col_value in range(top_col_in_box, top_col_in_box + 3):
                if same_box_row_value != row and same_box_col_value != col:
                    queue.append((same_box_row_value, same_box_col_value))
        #print("After appending at AC3?")
        while len(queue) != 0:
            print("Getting item in queue")
            current_position = queue.pop()
            print(current_position)
            row, col = current_position
            #print(puzzle[row][col])
            if self.revise(puzzle, current_position):
                print("Has been revised")
                row, col = current_position
                print(puzzle[row][col])
                if len(puzzle[row][col]) == 0: # Means that there is a wrong domain assignment
                    print("Length is 0")
                    return False
                for col_value in range(9): # Items in same row
                    if col_value != col:
                        #print("Appending col_value")
                        queue.append((row, col_value))
                for row_value in range(9): # Items in same col
                    if row_value != row:
                        #print("Appending row_value")
                        queue.append((row_value, col))
                top_row_in_box = int(row / 3) * 3 # Items in the same box
                top_col_in_box = int(col / 3) * 3
                for same_box_row_value in range(top_row_in_box, top_row_in_box + 3):
                    for same_box_col_value in range(top_col_in_box, top_col_in_box + 3):
                        if same_box_row_value != row and same_box_col_value != col:
                            #print("Appending box value")
                            queue.append((same_box_row_value, same_box_col_value))
        return True
            
    
    # Check to see if row / cols / boxes satisfy the constraint
    def revise(self, puzzle, position):
        is_revised = False
        row, col = position
        values = puzzle[row][col]
        values_to_remove = set()
        print("Start of revise")
        print(values)
        for value in values:
            value_found = False
            for col_value in range(9): # Items in the same row
                if col_value != col:
                    #print("I'm rly here")
                    if len(puzzle[row][col_value]) == 1 and value in puzzle[row][col_value]:
                        print("At revise col value")
                        print(value)
                        print("Row")
                        print(row)
                        print("Col")
                        print(col_value)
                        print("item inside is ")
                        print(puzzle[row][col_value])
                        values_to_remove.add(value)
                        break

            for row_value in range(9): # Items in the same col
                if row_value != row:
                    if len(puzzle[row_value][col]) == 1 and value in puzzle[row_value][col]:
                        print("At revise row value")
                        print(value)
                        values_to_remove.add(value)
                        break
            #if value_found:
            #    break        

            top_row_in_box = int(row / 3) * 3 # Items in the same box
            #print("Top row in box:")
            #print(top_row_in_box)
           # print("Top col in box:")
            top_col_in_box = int(col / 3) * 3
            #print(top_col_in_box)
            for same_box_row_value in range(top_row_in_box, top_row_in_box + 3):
                for same_box_col_value in range(top_col_in_box, top_col_in_box + 3):
                    if same_box_row_value != row and same_box_col_value != col:
                        #print(same_box_row_value, same_box_col_value)
                        #print(puzzle[same_box_row_value][same_box_col_value])
                        if len(puzzle[same_box_row_value][same_box_col_value]) == 1 and value in puzzle[same_box_row_value][same_box_col_value]:
                            values_to_remove.add(value)
                            print("At revise box value")
                            print(value)
                            break

        for value in values_to_remove:
            is_revised = True
            #print("Removing")
            #print(value)
            values.remove(value)
       # print("Values remaining after revision")
       # print(position)
      #  print(values)
        return is_revised


    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

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
