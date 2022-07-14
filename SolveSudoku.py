SUDOKU_LENGTH = 9


def printBoard(a):
    for i in range(SUDOKU_LENGTH):
        for j in range(SUDOKU_LENGTH):
            print(a[i][j], end=" ")
        print()


def solveGame(grid, row, col, num):
    for x in range(SUDOKU_LENGTH):
        if grid[row][x] == num:
            return False

    for x in range(SUDOKU_LENGTH):
        if grid[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3

    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True


def sudokuGame(grid, row, col):
    if row == SUDOKU_LENGTH - 1 and col == SUDOKU_LENGTH:
        return True

    if col == SUDOKU_LENGTH:
        row += 1
        col = 0

    if grid[row][col] > 0:
        return sudokuGame(grid, row, col + 1)

    for num in range(1, SUDOKU_LENGTH + 1, 1):
        if solveGame(grid, row, col, num):
            grid[row][col] = num
            if sudokuGame(grid, row, col + 1):
                return True

        grid[row][col] = 0

    return False


def getGame(string):
    game = []
    row = []
    for num in string:
        if num == '\n':
            game.append(row.copy())
            row.clear()
        else:
            row.append(int(num))
    return game


def validateGame(game):
    if len(game) == SUDOKU_LENGTH:
        for row in game:
            if len(row) != SUDOKU_LENGTH:
                return False
    else:
        return False
    return True
