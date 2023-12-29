# Tanner DeGrazia; Assignment 10; April 16th, 2023; CS051A
# This program looks to solve a started Sudoku Board.


import copy
import time


class SudokuState:
    """
    Class creates functions that look to initialize a Sudoku Board state and then solve it.
    """

    def __init__(self):
        """
        Constructor initializes global variables like the size, spaces filled, and the board itself
        """
        self.size = 9
        self.num_placed = 0

        m1 = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                row.append(SudokuEntry())
                # appends the possible answers of 1-9 to each possible instance
            m1.append(row)
            # appends the 9 possibilities of the row to a list to be the whoel board

        self.board = m1

    def remove_conflict(self, row, col, num):
        """
        This function ensures there is no space that can use the same number called here
        :param row: calls what row to look for
        :param col: calls what column to look for
        :param num: calls what number should be no longer a possiblity for neighboring openings and this space
        :return: none
        """
        if not self.board[row][col].is_fixed():
            # ensures a spot is not full as it iterates through every spot
            self.board[row][col].eliminate(num)
            # takes out the called num from every appropriate instance

    def remove_all_conflicts(self, row, col, num):
        """
        Looks to remove every conflict from corresponding row, col, and quadrant
        :param row: the row that the number should be removed as a possibility from
        :param col: the col that the number should be removed as a possibility from
        :param num: the number that needs to be removed from possiblities
        :return: none
        """
        for i in range(self.size):
            self.remove_conflict(i, col, num)
            # removes conflicts from same row
            self.remove_conflict(row, i, num)
            # removes conflicts from same col
        for r in range(self.size):
            for c in range(self.size):
                # iterates through whole grid
                if self.get_subgrid_number(r, c) == self.get_subgrid_number(row, col):
                    # checking to see if in same quadrant number
                    self.remove_conflict(r, c, num)

    def add_number(self, row, col, num):
        """
        inserts a number into the called spot
        :param row: inserts at this row
        :param col: inserts at this column
        :param num: inserts this number
        :return: none
        """
        self.board[row][col].fix(num)
        # adds number at called place
        self.remove_all_conflicts(row, col, num)
        # ensures there are no conflicts
        self.num_placed += 1
        # increments every time a space is filled

    def get_most_constrained_cell(self):
        """
        Finds the cell with the least amount of possible values
        :return: a tuple containing the row and col where the most constrained cell is
        """
        tup = None
        least_options = self.size + 1
        # creates a base of most constrained
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c].width() < least_options and not self.board[r][c].is_fixed():
                    tup = (r, c)
                    # makes a tuple of where the most constrained spot is
                    least_options = self.board[r][c].width()
                    # updates the smallest width as of right now

        return tup

    def solution_is_possible(self):
        """
        checks to see if we can achieve a solution from current state
        :return: boolean T/F
        """
        for r in range(self.size):
            for c in range(self.size):
                if not self.board[r][c].width() >= 1:
                    return False
                else:
                    return True

    def next_states(self):
        """
        discovers the next states with possible additions to the board
        :return: a list of all the possibilities
        """
        next_states = []
        r, c = self.get_most_constrained_cell()
        # r, c = self.get_any_available_cell()
        # declares the row and col as the most constrained possibilities
        for next_constraint in self.board[r][c].values():
            # iterates through all the values of each possible spot
            next_open_states = copy.deepcopy(self)
            # creates a deepcopy
            next_open_states.add_number(r, c, next_constraint)
            # self.propagate()
            if next_open_states.solution_is_possible():
                # if the possibility will not break the solution
                next_states.append(next_open_states)
        return next_states

    def is_goal(self):
        """
        checks if board is complete
        :return: boolean T/F
        """
        return (self.size ** 2) == self.num_placed

    def get_subgrid_number(self, row, col):
        """
        Returns a number between 1 and 9 representing the subgrid
        that this row, col is in.  The top left subgrid is 1, then
        2 to the right, then 3 in the upper right, etc.
        """
        row_q = int(row / 3)
        col_q = int(col / 3)
        return row_q * 3 + col_q + 1

    def get_any_available_cell(self):
        """
        An uninformed cell finding variant.  If you use
        this instead of find_most_constrained_cell
        the search will perform a depth first search.
        """
        for r in range(self.size):
            for c in range(self.size):
                if not self.board[r][c].is_fixed():
                    return r, c
        return None

    def propagate(self):
        """
        determines next state in a different manner
        :return: propogate
        """
        for ri in range(self.size):
            for ci in range(self.size):
                if not self.board[ri][ci].is_fixed() and \
                        self.board[ri][ci].width() == 1:
                    self.add_number(ri, ci, self.board[ri][ci].values()[0])
                    if self.solution_is_possible():
                        self.propagate()
                        return

    def get_raw_string(self):
        """
        gets raw string of pretty board
        :return: string of how many spots have been filled and the lists of possibilities of each instances
        """
        board_str = ""

        for r in self.board:
            board_str += str(r) + "\n"

        return "num placed: " + str(self.num_placed) + "\n" + board_str

    def __str__(self):
        """
        prints all numbers assigned to cells.  Unassigned cells (i.e.
        those with a list of options remaining are printed as blanks
        """
        board_string = ""

        for r in range(self.size):
            if r % 3 == 0:
                board_string += " " + "-" * (self.size * 2 + 5) + "\n"

            for c in range(self.size):
                entry = self.board[r][c]

                if c % 3 == 0:
                    board_string += "| "

                board_string += str(entry) + " "

            board_string += "|\n"

        board_string += " " + "-" * (self.size * 2 + 5) + "\n"

        return "num placed: " + str(self.num_placed) + "\n" + board_string


# -----------------------------------------------------------------------
"""
Make all of your changes to the SudokuState class above.
only when you're running the last experiments will
you need to change anything below here and then only
the different problem inputs
"""


class SudokuEntry:
    def __init__(self):
        self.fixed = False
        self.domain = list(range(1, 10))

    def is_fixed(self):
        return self.fixed

    def width(self):
        return len(self.domain)

    def values(self):
        return self.domain

    def has_conflict(self):
        return len(self.domain) == 0

    def __str__(self):
        if self.fixed:
            return str(self.domain[0])
        return "_"

    def __repr__(self):
        if self.fixed:
            return str(self.domain[0])
        return str(self.domain)

    def fix(self, n):
        assert n in self.domain
        self.domain = [n]
        self.fixed = True

    def eliminate(self, n):
        if n in self.domain:
            assert not self.fixed
            self.domain.remove(n)


# -----------------------------------
"""
Even though this is the same DFS code
that we used last time, our next_states
function is making an "informed" decision
so this algorithm performs similarly to
best first search.
"""


def dfs(state):
    """
    Recursive depth first search implementation

    Input:
    Takes as input a state.  The state class MUST have the following
    methods implemented:
    - is_goal(): returns True if the state is a goal state, False otherwise
    - next_states(): returns a list of the VALID states that can be
    reached from the current state

    Output:
    Returns a list of ALL states that are solutions (i.e. is_goal
    returned True) that can be reached from the input state.
    """
    # if the current state is a goal state, then return it in a list
    if state.is_goal():
        return [state]
    else:
        # make a list to accumulate the solutions in
        result = []

        for s in state.next_states():
            result += dfs(s)

        return result


# ------------------------------------
"""
Three different board configurations:
 - problem1
 - problem2
 - heart (example from class notes)
"""


def problem1():
    b = SudokuState()
    b.add_number(0, 1, 7)
    b.add_number(0, 7, 1)
    b.add_number(1, 2, 9)
    b.add_number(1, 3, 7)
    b.add_number(1, 5, 4)
    b.add_number(1, 6, 2)
    b.add_number(2, 2, 8)
    b.add_number(2, 3, 9)
    b.add_number(2, 6, 3)
    b.add_number(3, 1, 4)
    b.add_number(3, 2, 3)
    b.add_number(3, 4, 6)
    b.add_number(4, 1, 9)
    b.add_number(4, 3, 1)
    b.add_number(4, 5, 8)
    b.add_number(4, 7, 7)
    b.add_number(5, 4, 2)
    b.add_number(5, 6, 1)
    b.add_number(5, 7, 5)
    b.add_number(6, 2, 4)
    b.add_number(6, 5, 5)
    b.add_number(6, 6, 7)
    b.add_number(7, 2, 7)
    b.add_number(7, 3, 4)
    b.add_number(7, 5, 1)
    b.add_number(7, 6, 9)
    b.add_number(8, 1, 3)
    b.add_number(8, 7, 8)
    return b


def problem2():
    b = SudokuState()
    b.add_number(0, 1, 2)
    b.add_number(0, 3, 3)
    b.add_number(0, 5, 5)
    b.add_number(0, 7, 4)
    b.add_number(1, 6, 9)
    b.add_number(2, 1, 7)
    b.add_number(2, 4, 4)
    b.add_number(2, 7, 8)
    b.add_number(3, 0, 1)
    b.add_number(3, 2, 7)
    b.add_number(3, 5, 9)
    b.add_number(3, 8, 2)
    b.add_number(4, 1, 9)
    b.add_number(4, 4, 3)
    b.add_number(4, 7, 6)
    b.add_number(5, 0, 6)
    b.add_number(5, 3, 7)
    b.add_number(5, 6, 5)
    b.add_number(5, 8, 8)
    b.add_number(6, 1, 1)
    b.add_number(6, 4, 9)
    b.add_number(6, 7, 2)
    b.add_number(7, 2, 6)
    b.add_number(8, 1, 4)
    b.add_number(8, 3, 8)
    b.add_number(8, 5, 7)
    b.add_number(8, 7, 5)
    return b


def heart():
    b = SudokuState()
    b.add_number(1, 1, 4)
    b.add_number(1, 2, 3)
    b.add_number(1, 6, 6)
    b.add_number(1, 7, 7)
    b.add_number(2, 0, 5)
    b.add_number(2, 3, 4)
    b.add_number(2, 5, 2)
    b.add_number(2, 8, 8)
    b.add_number(3, 0, 8)
    b.add_number(3, 4, 6)
    b.add_number(3, 8, 1)
    b.add_number(4, 0, 2)
    b.add_number(4, 8, 5)
    b.add_number(5, 1, 5)
    b.add_number(5, 7, 4)
    b.add_number(6, 2, 6)
    b.add_number(6, 6, 7)
    b.add_number(7, 3, 5)
    b.add_number(7, 5, 1)
    b.add_number(8, 4, 8)
    return b


# --------------------------------
"""
Code that actually runs a sudoku problem, times it and prints out the solution.
You can vary which problem your running on between problem1(), problem2() and heart() by changing the line below
This code will run the problem! Comment it out to work on the code above.
"""


problem = problem1()
print("Starting board:")
print(problem)

start_time = time.time()
solutions = dfs(problem)
search_time = time.time() - start_time

print("Search took " + str(round(search_time, 2)) + " seconds")
print("There was " + str(len(solutions)) + " solution.\n\n")
if len(solutions) > 0:
    print(solutions[0])


"""
Takeaways:
When experimenting, it was interesting to see the differences in response time dependent upon what function was
 called. To begin the difference between getting the most constrained cell and getting any cell made sense to me.
 As getting the most constrained cell should be quicker, as it will address the problem faster than going through all
 cells and possibly going down many wrong rabbit holes. The experiment proved this by once running in .02 seconds when
 constrained cell was called and .8 seconds when any cells were called. However, when propagate was then involved
 getting the most constrained cell finished in .05 seconds and any cell in .04 which I found very interesting.
 But finding any cell using propagate actually broke the code and returned no answer possible, which I would
 assume occurs due to memory filling and killing the code.
 """