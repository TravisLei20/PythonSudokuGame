import pygame
import cv2
import pytesseract
import copy
import time

import SolveSudoku


pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\travi\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

# WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = (540, 600)
WINDOW_SIZE = (850, 600)
WINDOW_WIDTH, WINDOW_HEIGHT = (540, 600)
LINE_WIDTH = 2
GAP = 60
GREY_COLOR = (128, 128, 128)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 255, 0)
RED_COLOR = (255, 0, 0)
BLUE_COLOR = (0, 0, 255)
SUDOKU_LENGTH = 9

DEBUG = False

guess_board = []
correct_board = []
info_board = []
mistakes = 0
previous_mistakes_num = 0
fnt = 0
previous_time = ""


########################################################################################################################
########################################################################################################################
########################################################################################################################


class Cell:
    wrong_guesses = []
    correct_answer = "UnKnown"

    def __int__(self, value):
        if value != 0:
            self.correct_answer = value
            self.wrong_guesses = []


########################################################################################################################
########################################################################################################################
########################################################################################################################


def drawGrid(window, complete):
    color = BLACK_COLOR
    if complete:
        color = BLUE_COLOR
    for i in range(SUDOKU_LENGTH+1):
        line_size = LINE_WIDTH
        if i % 3 == 0:
            line_size = 5
        pygame.draw.rect(window, color, (i * (WINDOW_WIDTH / SUDOKU_LENGTH), 0, line_size, WINDOW_WIDTH))
        pygame.draw.rect(window, color, (0, i * (WINDOW_WIDTH / SUDOKU_LENGTH), WINDOW_WIDTH, line_size))


########################################################################################################################
########################################################################################################################
########################################################################################################################


def init_board(window, game):
    drawGrid(window, False)
    for row in range(SUDOKU_LENGTH):
        for col in range(SUDOKU_LENGTH):
            if game[row][col] != 0:
                text = fnt.render(str(game[row][col]), True, BLACK_COLOR)
                window.blit(text, (col * GAP + 20, row * GAP + 5))


########################################################################################################################
########################################################################################################################
########################################################################################################################


def draw(window, pos, value, game_board):
    global guess_board
    row = pos[0]
    col = pos[1]
    gap = 60
    x = col * gap
    y = row * gap

    if game_board[row][col] == 0:
        if guess_board[row][col] != 0:
            text = fnt.render(str(guess_board[row][col]), True, WHITE_COLOR)
            window.blit(text, (x + 5, y + 5))
        if value != 0:
            text = fnt.render(str(value), True, GREY_COLOR)
            window.blit(text, (x + 5, y + 5))

        guess_board[row][col] = value


########################################################################################################################
########################################################################################################################
########################################################################################################################


def check_guess(window, game_board):
    global mistakes
    for row in range(SUDOKU_LENGTH):
        for col in range(SUDOKU_LENGTH):
            if guess_board[row][col] != 0:
                if guess_board[row][col] == correct_board[row][col]:
                    text = fnt.render(str(guess_board[row][col]), True, WHITE_COLOR)
                    window.blit(text, (col*60 + 5, row*60 + 5))
                    game_board[row][col] = correct_board[row][col]
                    text = fnt.render(str(game_board[row][col]), True, BLACK_COLOR)
                    window.blit(text, (col * GAP + 20, row * GAP + 5))
                    info_board[row][col].correct_answer = correct_board[row][col]
                else:
                    wrong_list = info_board[row][col].wrong_guesses.copy()
                    if not guess_board[row][col] in wrong_list:
                        wrong_list.append(guess_board[row][col])
                        info_board[row][col].wrong_guesses = wrong_list
                        mistakes += 1
                    text = fnt.render(str(guess_board[row][col]), True, RED_COLOR)
                    window.blit(text, (col * 60 + 5, row * 60 + 5))

    update_mistake_count(window)


########################################################################################################################
########################################################################################################################
########################################################################################################################


def update_mistake_count(window):
    global previous_mistakes_num
    if mistakes != previous_mistakes_num:
        text = fnt.render(f"You have made: {previous_mistakes_num} mistake(s)", True, WHITE_COLOR)
        window.blit(text, (15, 545))
        text = fnt.render(f"You have made: {mistakes} mistake(s)", True, BLACK_COLOR)
        window.blit(text, (15, 545))
        previous_mistakes_num = mistakes


########################################################################################################################
########################################################################################################################
########################################################################################################################


def check_game_over(window, game_board):
    for row in range(SUDOKU_LENGTH):
        for col in range(SUDOKU_LENGTH):
            if game_board[row][col] != correct_board[row][col]:
                return False
    text = fnt.render("You Win!!!", True, RED_COLOR)
    window.blit(text, (565, 450))
    return True


########################################################################################################################
########################################################################################################################
########################################################################################################################


def format_time(play_time):
    sec = play_time % 60
    minute = play_time//60
    hour = minute//60
    return f"{str(hour)}:{str(minute)}:{str(sec)}"


########################################################################################################################
########################################################################################################################
########################################################################################################################


def redraw_time(window, game_time):
    global previous_time
    this_time = format_time(game_time)
    if previous_time != this_time:
        text = fnt.render("Time: " + previous_time, True, WHITE_COLOR)
        window.blit(text, (580, 550))
        text = fnt.render("Time: " + this_time, True, BLACK_COLOR)
        window.blit(text, (580, 550))
        previous_time = this_time


########################################################################################################################
########################################################################################################################
########################################################################################################################


def draw_info(window, previous, row, col):
    cell = info_board[row][col]
    wrong_guesses = cell.wrong_guesses
    correct_guess = cell.correct_answer

    diff_fnt = pygame.font.SysFont("comicsans", 30)

    if previous is not None:
        text = diff_fnt.render(str(previous[0]), True, WHITE_COLOR)
        window.blit(text, (550, 90))
        text = diff_fnt.render(str(previous[1]), True, WHITE_COLOR)
        window.blit(text, (550, 160))

    text = diff_fnt.render(str(correct_guess), True, BLACK_COLOR)
    window.blit(text, (550, 90))
    text = diff_fnt.render(str(wrong_guesses), True, BLACK_COLOR)
    window.blit(text, (550, 160))
    return [correct_guess, wrong_guesses]


########################################################################################################################
########################################################################################################################
########################################################################################################################


def cheat(window):
    drawGrid(window, True)
    text = fnt.render("Cheater", True, RED_COLOR)
    window.blit(text, (560, 450))
    for row in range(SUDOKU_LENGTH):
        for col in range(SUDOKU_LENGTH):
            text = fnt.render(str(guess_board[row][col]), True, WHITE_COLOR)
            window.blit(text, (col * 60 + 5, row * 60 + 5))
            text = fnt.render(str(correct_board[row][col]), True, BLUE_COLOR)
            window.blit(text, (col * GAP + 20, row * GAP + 5))


########################################################################################################################
########################################################################################################################
########################################################################################################################


def start_game(game_board):
    pygame.init()
    global fnt
    fnt = pygame.font.SysFont("comicsans", 40)
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Sudoku")
    window.fill(WHITE_COLOR)
    init_board(window, game_board)
    global correct_board
    correct_board = copy.deepcopy(game_board)
    SolveSudoku.sudokuGame(correct_board, 0, 0)
    global guess_board
    guess_board = copy.deepcopy(game_board)
    global info_board
    for row in range(SUDOKU_LENGTH):
        arr = []
        for col in range(SUDOKU_LENGTH):
            cell = Cell()
            if game_board[row][col] != 0:
                cell.correct_answer = game_board[row][col]
            arr.append(cell)
        info_board.append(arr)
    text = fnt.render(f"You have made: 0 mistake(s)", True, BLACK_COLOR)
    window.blit(text, (15, 545))
    diff_fnt = pygame.font.SysFont("comicsans", 30)
    text = fnt.render("Cell Info", True, BLACK_COLOR)
    window.blit(text, (550, 5))
    text = fnt.render("--------------", True, BLACK_COLOR)
    window.blit(text, (550, 25))
    text = diff_fnt.render("Correct Answer:", True, BLACK_COLOR)
    window.blit(text, (550, 60))
    text = diff_fnt.render("Wrong Guesses:", True, BLACK_COLOR)
    window.blit(text, (550, 130))
    text = fnt.render("--------------", True, BLACK_COLOR)
    window.blit(text, (550, 185))
    text = fnt.render("Game Info", True, BLACK_COLOR)
    window.blit(text, (550, 220))
    text = fnt.render("--------------", True, BLACK_COLOR)
    window.blit(text, (550, 250))
    small_fnt = pygame.font.SysFont("comicsans", 20)
    text = small_fnt.render("* Select a cell to input your", True, BLACK_COLOR)
    window.blit(text, (550, 300))
    text = small_fnt.render("answer. Then press enter to", True, BLACK_COLOR)
    window.blit(text, (550, 325))
    text = small_fnt.render("check your guess.", True, BLACK_COLOR)
    window.blit(text, (550, 350))
    text = small_fnt.render("* Press space to show answers", True, BLACK_COLOR)
    window.blit(text, (550, 385))
    text = fnt.render("--------------", True, BLACK_COLOR)
    window.blit(text, (550, 400))
    return window


########################################################################################################################
########################################################################################################################
########################################################################################################################


def play_game(window, game_board):
    run_game = True
    exit_immediately = False
    game_key = None
    start = time.time()
    row_and_col = []
    previous_info = None

    while run_game:
        for event in pygame.event.get():
            event_type = event.type
            if event_type == pygame.QUIT or event.key == pygame.K_ESCAPE if event_type == pygame.KEYDOWN else False:
                run_game = False
                exit_immediately = True
            if event_type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_1 or key == pygame.K_KP1 and row_and_col != []:
                    game_key = 1
                elif key == pygame.K_2 or key == pygame.K_KP2 and row_and_col != []:
                    game_key = 2
                elif key == pygame.K_3 or key == pygame.K_KP3 and row_and_col != []:
                    game_key = 3
                elif key == pygame.K_4 or key == pygame.K_KP4 and row_and_col != []:
                    game_key = 4
                elif key == pygame.K_5 or key == pygame.K_KP5 and row_and_col != []:
                    game_key = 5
                elif key == pygame.K_6 or key == pygame.K_KP6 and row_and_col != []:
                    game_key = 6
                elif key == pygame.K_7 or key == pygame.K_KP7 and row_and_col != []:
                    game_key = 7
                elif key == pygame.K_8 or key == pygame.K_KP8 and row_and_col != []:
                    game_key = 8
                elif key == pygame.K_9 or key == pygame.K_KP9 and row_and_col != []:
                    game_key = 9
                elif key == pygame.K_SPACE:
                    cheat(window)
                    run_game = False
                elif key == pygame.K_BACKSPACE:
                    game_key = 0
                elif key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
                    check_guess(window, game_board)
                    previous_info = draw_info(window, previous_info, row_and_col[0], row_and_col[1])
                    if check_game_over(window, game_board):
                        drawGrid(window, True)
                        run_game = False

                if game_key is not None:
                    draw(window, row_and_col, game_key, game_board)
                    game_key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] < 540 and pos[1] < 540:
                    if row_and_col:
                        row = row_and_col[0]
                        col = row_and_col[1]
                        x = col * GAP
                        y = row * GAP
                        pygame.draw.rect(window, BLACK_COLOR, (x, y, GAP, GAP), LINE_WIDTH)

                    row = pos[1] // 60
                    col = pos[0] // 60
                    x = col * GAP
                    y = row * GAP
                    row_and_col = [row, col]
                    pygame.draw.rect(window, RED_COLOR, (x, y, GAP, GAP), LINE_WIDTH)
                    previous_info = draw_info(window, previous_info, row, col)

        redraw_time(window, round(time.time() - start))
        pygame.display.update()

    while not exit_immediately:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.key == pygame.K_ESCAPE if event.type == pygame.KEYDOWN else False:
                exit_immediately = True
                break

    pygame.quit()


########################################################################################################################
########################################################################################################################
########################################################################################################################


def main():
    img = cv2.imread('Images\\game7.png')
    image_text = pytesseract.image_to_string(img)

    game_board = SolveSudoku.getGame(image_text)
    valid_game = SolveSudoku.validateGame(game_board)

    ###################################################
    ###################################################
    ###################################################
    if DEBUG:
        SolveSudoku.puzzle(game_board)
    ###################################################
    ###################################################
    ###################################################

    if valid_game:
        window = start_game(game_board)
        play_game(window, game_board)
    else:
        print("Invalid game\n")
        print(image_text)


########################################################################################################################
########################################################################################################################
########################################################################################################################


if __name__ == "__main__":
    main()
