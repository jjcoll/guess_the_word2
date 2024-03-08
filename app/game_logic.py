from random import randint
from flask import session


def read_word_list(words_file):
    word_list = []
    file = open(f"app/wordlists/{words_file}", "r")
    for line in file:
        word_list.append(line.strip())
    return word_list


def choose_word(word_list):
    index = randint(0, len(word_list) - 1)
    return word_list[index]


def print_board(board):
    return "".join(board)


def check_board(letter, board, word, lives):
    looses_life = True
    for i in range(len(word)):
        if letter.lower() == word[i].lower():
            board[i] = word[i]
            looses_life = False
    if looses_life and lives > 0:
        lives -= 1

    if word == "".join(board):
        # session["score"] = session["score"] + 1
        return board, lives, 1

    # update session
    session["board"] = board
    session["lives"] = lives

    return board, lives, 0


def start_new_game(wordfile):

    words = read_word_list(wordfile)
    word = choose_word(words)
    lives = 6

    # allow words with spaces
    board = []
    for letter in word:
        if letter != " ":
            board.append("_")
        else:
            board.append(" ")

    # store in session so they can be accessed outside the scope of this function
    # and like this we create a new board and word each session
    session["word"] = word
    session["board"] = board
    session["lives"] = lives
    session["won"] = 0
    session["wordsfile"] = wordfile
    return word, board, lives
