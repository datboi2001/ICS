# Datthew Nguyen - 61886297
from collections import namedtuple
import connectfour as c4


def welcome_player() -> None:
    """Print out a welcome message."""
    print('Welcome to Connect Four designed by Datthew Nguyen.')
    print('---------------------------------------------------')


def print_turn(game_state) -> str:
    """Determine whose turn it is."""
    turn = None
    if game_state.turn == 1:
        turn = 'Red'
    elif game_state.turn == 2:
        turn = 'Yellow'
    return turn


def print_board(game: c4.GameState) -> None:
    """Print out the game board."""
    print('1  2  3  4  5  6  7')
    for row in range(0, c4.BOARD_ROWS):
        for col in range(0, c4.BOARD_COLUMNS):
            chr = '.'
            if game.board[col][row] == 1:
                chr = 'R'
            elif game.board[col][row] == 2:
                chr = 'Y'
            if col == c4.BOARD_COLUMNS - 1:
                print('{}'.format(chr))
            else:
                print('{}  '.format(chr), end='')


def process_move(move: str, state: namedtuple) -> c4.GameState:
    """Execute the move with the given input from the user."""
    try:
        if move.startswith('DROP'):
            col_number = int(move.replace('DROP', '')) - 1
            updated_game = c4.drop(state, col_number)
            return updated_game
        elif move.startswith('POP'):
            col_number = int(move.replace('POP', '')) - 1
            updated_game = c4.pop(state, col_number)
            return updated_game
        else:
            print('Sorry, that command does not exist.')
            return state
    except (ValueError, c4.InvalidMoveError) as e:
        if state.turn == 1:
            print('Sorry Red, that was an invalid command.')
        else:
            print('Sorry Yellow, that was an invalid command.')
        return state


def ask_for_move() -> str:
    """Prompt the user to input their moves."""
    user_input = input('Please enter your move (DROP or POP) followed by a space then a number(1-7): ')
    return user_input

