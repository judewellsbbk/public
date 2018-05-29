""" Jude Wells
Student Number: 13129680
Principles of Programming: Assignment Three - Sudoku
This programme attempts to solve 9x9 sudoku problems that are read from a file.
It prints the initial problem, attempts to solve it and prints the transformed
puzzle (solved or unsolved). If the problem is unsolved it prints a list of locations
where the number is unknown and possible values for each location.
The problem must be in the form of a 2 dimensional array, where a list of 9 lists
represent the 9 rows, and there are 9 integers in each list. Each integer will be
a single digit from 1 to 9 if the number in the position is given, or 0 if the
number in the position is unknown.
"""


def read_sudoku(file):
    """Reads and returns a Sudoku problem from a text file."""
    stream = open(file)
    data = stream.readlines()
    stream.close()
    return eval("".join(data))


def arrayValidate(problem):
    """Takes the input problem and checks whether it is in a format that the programme will be able to compute.
    Returns True if the problem is in the form of a 9 x 9 array where each element is an integer between 0 and 9,
    otherwise returns False and prints a message explaining why the input is invalid.
    """
    sudoku_size = 9
    if len(problem) != sudoku_size:
        print('Programme only accepts 2D arrays with dimensions of %i x %i' % (sudoku_size, sudoku_size))
        return False
    for row in problem:
        if type(row) != list or len(row) != sudoku_size:
            print('Programme only accepts 2D arrays with dimensions of %i x %i' % (sudoku_size, sudoku_size))
            return False
        for element in row:
            if type(element) != int or element > sudoku_size or element < 0:
                print('Input array should only contain integers from 0 to %i' % sudoku_size)
                return False
    return True


def convertToSets(problem):
    """Takes a sudoku problem which must be in the form of a 2D array.
    The function replaces each position in the problem with
    a set containing the number or 1:9 if the position number is unknown.
    The function returns the array of sets.
    """
    sets_array = []
    for row in problem:
        sets_array.append([{1, 2, 3, 4, 5, 6, 7, 8, 9} if e == 0 else {e} for e in row])
    return sets_array


def convertToInts(problem):
    """Takes the problem in the form of an array of sets and converts it
    and returns an array of integers.
    """
    list_array = []
    for row in problem:
        list_array.append([0 if (len(e) > 1) else sum(e) for e in row])
    return list_array


def getRowLocations(rowNumber):
    """Given a row number return a list of all nine locations
    ((row, column)  tuples) in that row.
    """
    return [(rowNumber, c) for c in range(9)]


def getColumnLocations(columnNumber):
    """Given a column number returns a list of tuples representing
    all locations in that column. (row, column).
    """
    return [(r, columnNumber) for r in range(9)]


def getBoxLocations(location):
    """Returns a list of all nine locations ((row, column) tuples)
    in the same box as the given location.
    """
    location_dict = {
        1: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
        2: [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)],
        3: [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)],
        4: [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)],
        5: [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)],
        6: [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)],
        7: [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)],
        8: [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)],
        9: [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]
    }
    for key, value in location_dict.items():
        if location in value:
            return value


def eliminate(problem, location, listOfLocations):
    """ Given a location for a set eliminate checks the length of the set.
    if the length of the set is > 1 it returns zero. If len(set) == 1 eliminate
    transforms the problem by removing all occurrences of the number contained
    in the location set from all sets referenced in listOfLocations.
    :param problem: an array of sets representing the problem
    :param location: a tuple (row, column) which is the location of a set
    :param listOfLocations: a list of locations which are in the same box, row or column as 'location'
    :return: a count of the number times a number was removed from a set
    """
    count = 0
    row1, column1 = location
    if len(problem[row1][column1]) > 1:
        return count
    listOfLocations[:] = [l for l in listOfLocations if l != location] #removes location from listOfLocations
    for list_location in listOfLocations:
        row2, column2 = list_location
        if problem[row1][column1].issubset(problem[row2][column2]):
            problem[row2][column2].difference_update(problem[row1][column1])
            count += 1
    return count


def isSolved(problem):
    """Returns True if every set in the problem has only one number,
    otherwise returns false."""
    return all([len(problem[r][c]) == 1 for r in range(0, 9) for c in range(0, 9)])


def print_sudoku(problem):
    """Prints the Sudoku array (given as a list of integers)
    in a form that looks like a Sudoku puzzle. Unknown numbers
    are represented with '.'.
    """
    horizontal = '+-------+-------+-------+'
    row_array = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    for row_trio in row_array:
        print(horizontal)
        for row_index in row_trio:
            dot_row = [n if n != 0 else '.' for n in problem[row_index]]
            one_row = '| ' + str(dot_row[0]) + ' ' + str(dot_row[1]) + ' ' + str(dot_row[2]) + ' | ' \
                + str(dot_row[3]) + ' ' + str(dot_row[4]) + ' ' + str(dot_row[5]) + ' | ' \
                + str(dot_row[6]) + ' ' + str(dot_row[7]) + ' ' + str(dot_row[8]) + ' |'
            print(one_row)
    print(horizontal)


def solve(problem_sets):
    """ For each position in the problem it generates a list of locations that are in the
    same row, column and box as the location with just one element. It then
    passes the location, list of locations and problem to the eliminate function.
    Solve repeats the steps above until either the problem is solved or eliminate
    returns zero for every position.
    The function returns the value of calling isSolved on the problem:
    True if the problem is solved False if the problem is unsolved.
    """
    elimination_count = 1
    while elimination_count > 0:
        if isSolved(problem_sets):
            return True     # Prevents the elimination process running after the problem has been solved.
        elimination_count = 0
        row_index = 0
        for row in problem_sets:
            column_index = 0
            for _ in row:
                main_location = (row_index, column_index)
                main_loc_list = set()
                main_loc_list = main_loc_list.union(getBoxLocations(main_location))
                main_loc_list = main_loc_list.union(getColumnLocations(column_index))
                main_loc_list = main_loc_list.union(getRowLocations(row_index))
                main_loc_list = list(main_loc_list)
                elimination_count += eliminate(problem_sets, main_location, main_loc_list)
                column_index += 1
            row_index += 1
    return False    # This returns the value of isSolved() without having to call the function again.


def solveAnother():
    """ Asks user if they want to solve another problem returns True if input begins with Y or y,
    false if input begins N or n.
    """
    while True:
        response = input("\nWould you like to solve another problem? (Y/N) \n")
        try:
            if response[0] in {'Y', 'y'}:
                return True
            elif response[0] in {'N', 'n'}:
                return False
            print('Invalid input please enter \"Y\" or \"N\"')
        except:
            print('Invalid input please enter \"Y\" or \"N\"')
            continue


def print_unsolved_locations(problem_sets):
    """ Takes a problem as an input parameter in the form of an
    array of sets. Prints locations and possible value of each unsolved
    location in the problem.
    """
    row_number = 0
    print('\n(Unsolved Locations) and {Possible Values}:')
    for row in problem_sets:
        set_number = 0
        for one_set in row:
            if len(one_set) > 1:
                print('(' + str(row_number) + ',' + str(set_number) + ')', one_set)
            set_number += 1
        row_number += 1


def main():
    """Asks user for file directory of a Sudoku puzzle.
    Checks if the filename is valid and checks for a valid format
    by calling arrayValidate. If the file name or format is invalid
    it asks for the file name again.
    Prints the puzzle, attempts to solve the puzzle by calling other functions.
    Prints out the solution (which may be incomplete.)
    Prints out a list of unsolved locations and what numbers are still possible
    for the unsolved locations.
    Asks if user wants to read in and solve another puzzle.
    """
    valid_filename = False
    valid_array = False
    while not valid_filename or not valid_array:
        problem_name = input('\nEnter the file name for the problem you want to solve:\n')
        try:
            problem_int = read_sudoku(problem_name)
            valid_filename = True
        except:
            print('Invalid file or file path.')
            continue
        valid_array = arrayValidate(problem_int)
    print('Unsolved Sudoku:')
    print_sudoku(problem_int)
    problem_sets = convertToSets(problem_int)
    if not solve(problem_sets):
        print('Attempted Sudoku:')
        print_sudoku(convertToInts(problem_sets))
        print_unsolved_locations(problem_sets)
    else:
        print('Solved Sudoku:')
        print_sudoku(convertToInts(problem_sets))
    if solveAnother():
        main()


if __name__ == "__main__":
    main()
