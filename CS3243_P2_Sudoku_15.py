import sys
import copy
import time


class Sudoku(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle  # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle)  # self.ans is a list of lists

    def solve(self):
        start = time.clock()
        self.initialise()
        self.backtrack(puzzle)
        self.convert_to_output()
        end = time.clock()
        print(end - start)
        return self.ans

    # Initialise all the values in the puzzle as a set of values.
    # If there is a pre-existing value, we set it to be one single value inside the set.
    # If the value is 0, we provide it with a set of all possible values from 1-9.
    def initialise(self):
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] != 0:
                    set_values = set()
                    set_values.add(puzzle[row][col])
                    puzzle[row][col] = set_values
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

    # Converts from values in a set to values for output.
    def convert_to_output(self):
        for row in range(9):
            for col in range(9):
                for value in self.puzzle[row][col]:
                    self.ans[row][col] = value

    # Checks if every cell in the puzzle is ac3.
    # If all values are assigned, we return the puzzle.
    # If not, it chooses the position to set the new value based on the Minimum-Remaining-Values (MRV) heuristic.
    # For each possible value in this position, we try it and see if it returns a consistent solution.
    def backtrack(self, puzzle):
        for row in range(9):
            for col in range(9):
                if not self.ac3(puzzle, (row, col)):
                    return False
        mrv_row, mrv_col = self.find_mrv(puzzle)
        #mrv_row, mrv_col = self.find_mcv(puzzle)
        if mrv_row == -1 and mrv_col == -1:
            self.puzzle = puzzle
            return True

        mrv_values = puzzle[mrv_row][mrv_col].copy()
        #ordered_domain_values = self.get_ordered_domain_values((mrv_row, mrv_col), puzzle)

        #for value, frequency in ordered_domain_values:
        for value in mrv_values:
            current_puzzle = copy.deepcopy(puzzle)
            current_puzzle[mrv_row][mrv_col] = set()
            current_puzzle[mrv_row][mrv_col].add(value)
            if self.backtrack(current_puzzle):
                return True
        return False

    # In this problem, we are ensured that the puzzle is valid and well-formed.
    # Hence, we will just look through the given puzzles and count the number of possible values in it for our heuristic
    # If there are no values that are lesser than 10 and more than 1, we have found a solution, as every value is assigned.
    def find_mrv(self, puzzle):
        mrv = 10
        mrv_position = (-1, -1)
        for row in range(9):
            for col in range(9):
                possible_values = puzzle[row][col]
                if len(possible_values) < mrv and len(possible_values) != 1:
                    mrv = len(possible_values)
                    mrv_position = (row, col)
        return mrv_position

    # In this problem, we are ensured that the puzzle is valid and well-formed.
    # This heuristic is to find the most constraining variable
    def find_mcv(self, puzzle):
        mcv_position = (-1, -1)
        maximum_neighbours = -1
        for row in range(9):
            for col in range(9):
                if (len(puzzle[row][col]) == 0):
                    return (row, col)
                if (len(puzzle[row][col]) != 1):
                    free_connecting_cell_positions = self.get_empty_connecting_cell_positions(puzzle, (row, col))
                    if len(free_connecting_cell_positions) > maximum_neighbours:
                        maximum_neighbours = len(free_connecting_cell_positions)
                        mcv_position = (row, col)
        return mcv_position

    # Order the domain values of the variable using the 
    # least constraining value heuristic.
    def get_ordered_domain_values(self, position, puzzle):
        row, col = position
        possible_values = puzzle[row][col]
        free_connecting_cell_positions = self.get_empty_connecting_cell_positions(puzzle, position)
        ordered_value_tuples = []
        for value in possible_values:
            num_of_removed_values = 0
            for (free_row, free_col) in free_connecting_cell_positions:
                if value in puzzle[free_row][free_col]:
                    num_of_removed_values += 1
            ordered_value_tuples.append((value, num_of_removed_values))
        ordered_value_tuples.sort(key = lambda tup: tup[1])
        return ordered_value_tuples

    # Helper function to return positions of the connecting cells that have not been assigned a value yet.
    def get_empty_connecting_cell_positions(self, puzzle, position):
        connecting_cell_positions = self.get_connecting_cells_positions(puzzle, position)
        final_positions = list()
        for (row, col) in connecting_cell_positions:
            if len(puzzle[row][col]) != 1:
                final_positions.append((row, col))
        return final_positions
        
    # Helper function that returns all the cells that are connected (same row / same col / same box) to the given position, as a list.
    def get_connecting_cells_positions(self, puzzle, position):
        row, col = position
        output = list()
        for col_value in range(9):  # Items in same row
            if col_value != col:
                output.append((row, col_value))
        for row_value in range(9):  # Items in same col
            if row_value != row:
                output.append((row_value, col))
        top_row_in_box = int(row / 3) * 3  # Items in the same box
        top_col_in_box = int(col / 3) * 3
        for same_box_row_value in range(top_row_in_box, top_row_in_box + 3):
            for same_box_col_value in range(top_col_in_box, top_col_in_box + 3):
                if same_box_row_value != row and same_box_col_value != col:
                    output.append((same_box_row_value, same_box_col_value))
        return output

    # We will append the position, and if this position's domain is revised, we will add all the connecting cells back into the queue.
    # This continues until the domains of all the cells cannot be reduced anymore.
    def ac3(self, puzzle, position):
        queue = set()
        queue.add(position)
        while len(queue) != 0:
            current_position = queue.pop()
            if self.revise(puzzle, current_position):
                connecting_cells_positions = self.get_connecting_cells_positions(puzzle, current_position)
                for neighbouring_position in connecting_cells_positions:
                    if neighbouring_position not in queue:
                        queue.add(neighbouring_position)
        return True

    # Check to see if any of the connecting cell's domain consists of only a certain value of the cell we are looking at.
    # If it has, this means that this particular connecting cell's value is fixed.
    # Hence, we know that we can remove this value out of the cell we are looking at, as we cannot assign it that value regardless.
    def revise(self, puzzle, position):
        is_revised = False
        row, col = position
        values = puzzle[row][col]
        values_to_remove = set()
        connecting_cells_positions = self.get_connecting_cells_positions(puzzle, position)
        for value in values:
            for neighbouring_position in connecting_cells_positions:
                neighbour_row, neighbour_col = neighbouring_position
                if len(puzzle[neighbour_row][neighbour_col]) == 1 and value in puzzle[neighbour_row][neighbour_col]:
                    values_to_remove.add(value)
                    break
        for value in values_to_remove:
            is_revised = True
            puzzle[row][col].remove(value)
        return is_revised


if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
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
