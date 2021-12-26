import secrets
import os
from flask import redirect, url_for, render_template, request, jsonify
from SudokuSolver import app
from SudokuSolver.get_puzzle import *
from SudokuSolver.solve_sudoku import *


@app.route('/')
def home():
    return render_template("index.html")


def save_image(img, ext):
    random_hex = secrets.token_hex(8)
    filename = f"{random_hex}.{ext}"
    path = os.path.join(app.root_path, "static/sudoku", filename)
    img.save(path)
    return path


def make_str(grid, type="np-array"):
    puzzle_str = ''
    for row in grid:
        for ele in row:
            if type == "np-array":
                puzzle_str += str(ele.item())
            elif type == "list":
                puzzle_str += str(ele)

    return puzzle_str


@app.route('/', methods=["POST"])
def get_image():
    # Receive and save image
    img = request.files.get('sudoku_image', '')
    ext = request.form.get('ext')
    path = save_image(img, ext)

    # Detect the puzzle
    puzzle_grid = get_puzzle(path)

    if puzzle_grid is None:
        return jsonify({'success': 0, 'reason': 'cannot find puzzle'})

    # Solve the puzzle
    solved = solve_sudoku(puzzle_grid)

    if solved is None:
        return jsonify({'success': 0, 'reason': 'puzzle incorrect'})

    # Stringify Result
    original_str = make_str(puzzle_grid, "list")
    solved_str = make_str(solved)

    # Remove the original file
    os.remove(path)

    return jsonify({'original': original_str, 'solved': solved_str, 'success':1})