import numpy as np

def is_correct(grid, i, j, k):
    boxi = (i // 3) * 3
    boxj = (j // 3) * 3

    if k in grid[i] or k in grid[:, j]:
        return False

    if k in grid[boxi:boxi + 3, boxj:boxj + 3]:
        return False

    return True


def find_empty(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None


def solve(grid):
    empty = find_empty(grid)

    if empty is None:
        return True

    i, j = empty

    for k in range(1, 10):
        if is_correct(grid, i, j, k):
            grid[i, j] = k

            if solve(grid):
                return True

            grid[i, j] = 0

    return False


def is_puzzle_correct(puzzle):
    for i in range(9):
        for j in range(9):
                if puzzle[i][j] != 0:
                    k = puzzle[i][j]
                    puzzle[i][j] = 0
                    if not is_correct(puzzle, i, j, k):
                        return False
                    puzzle[i][j] = k
    return True


def solve_sudoku(grid):
    puzzle = np.array(grid)

    if is_puzzle_correct(puzzle):
        solve(puzzle)
        return puzzle

    return None
