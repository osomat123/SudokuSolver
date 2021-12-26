import cv2
import imutils
import numpy as np
from imutils.perspective import four_point_transform
from SudokuSolver import model


def find_puzzle_in_image(img):
    blur = cv2.GaussianBlur(img, (7, 7), 3)

    # Apply Adaptive Thresholding
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)

    # Find Contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # Get Grid Coordinates
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            puzzle_cnts = approx
            break

    # Warping along the contour
    try:
        puzzle = four_point_transform(img, puzzle_cnts.reshape(4, 2))
    except Exception:
        return None

    puzzle = cv2.resize(puzzle, (252, 252))

    return puzzle


def extract_cells(puzzle):
    x_step = int(puzzle.shape[1]//9)
    y_step = int(puzzle.shape[0]//9)

    cells = []
    for y in range(9):
        row = []
        for x in range(9):
            x_start = x * x_step
            y_start = y * y_step
            x_end = (x + 1) * x_step
            y_end = (y + 1) * y_step
            row.append((x_start, x_end, y_start, y_end))
        cells.append(row)

    return cells


def remove_noise(img):
    r,mask = cv2.threshold(img,10,255,cv2.THRESH_BINARY)
    eout = cv2.bitwise_and(mask,img)
    return eout


def extract_digit(cell):
    # invert image and add padding
    inv = 255 - cell
    pad = np.zeros(cell.shape, dtype="uint8")
    pad[2:26, 2:26] = inv[2:26, 2:26]
    cell = pad

    cnts, hierarchy = cv2.findContours(cell, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    t = cell.copy()
    t2 = cell.copy() * 0

    maxc = max(cnts, key=cv2.contourArea)

    cv2.drawContours(t2, [maxc], -1, 255, 2)
    cv2.fillPoly(t2, pts =[maxc], color=255)

    digit = cv2.bitwise_and(t, t2)
    digit = remove_noise(digit)
    _, digit = cv2.threshold(digit,115,255,cv2.THRESH_BINARY)

    return digit


def recognize(digit):
    roi = digit.astype("float32") / 255
    roi = roi.reshape((1,28,28,1))
    res = model.predict(roi)[0, :]
    pred = res.argmax()
    confidence = max(res)

    if confidence < 0.5:
        return 0

    return pred


def get_puzzle(path):
    img = cv2.imread(path, 0)
    puzzle = find_puzzle_in_image(img)

    # No grid found
    if puzzle is None:
        return None

    cells = extract_cells(puzzle)

    puzzle_grid = []
    for y in range(9):
        row = []
        for x in range(9):
            cell = puzzle[cells[y][x][2]:cells[y][x][3], cells[y][x][0]:cells[y][x][1]]
            digit = extract_digit(cell)
            row.append(recognize(digit))
        puzzle_grid.append(row)

    return puzzle_grid
