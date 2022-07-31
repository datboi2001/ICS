import game_logic as lib


def _dimension_input() -> (int, int):
    """Ask for row and dimension."""
    row = int(input())
    column = int(input())
    content = input().upper()
    if content == 'CONTENTS':
        content_list = []
        count = 0
        while count < row:
            jewels = input().upper()
            content_list.append(jewels)
            count += 1
        return content_list, row, column
    return content, row, column


def handle_command(board: lib.GameBoard) -> None:
    """Handle the command from the users."""
    game_over = False
    while not game_over:
        action = input().upper()
        if action.startswith('F'):
            if board.faller is None:
                action_list = action.split()
                faller_list = []
                faller_list += [action_list[2], action_list[3], action_list[4]]
                faller = lib.Faller(int(action_list[1]), faller_list)
                board.find_stop_position(faller)
                board.handle_faller(faller)
            else:
                lib.print_board(board)
            if board.game_over == True:
                lib.print_board(board)
                print('GAME OVER')
                game_over = True
        elif action == '':
            board.handle_faller()
            if board.game_over:
                lib.print_board(board)
                print('GAME OVER')
                game_over = True
        elif action == 'R':
            if board.faller is None:
                lib.print_board(board)
            else:
                board.rotate_faller(2 + board.count, board.faller.position)
        elif action == '>':
            if board.faller is None:
                lib.print_board(board)
            else:
                board.shift_faller_right(2 + board.count, board.faller.position)
        elif action == '<':
            if board.faller is None:
                lib.print_board(board)
            else:
                board.shift_faller_left(2 + board.count, board.faller.position)
        elif action == 'Q':
            game_over = True


def run_game() -> None:
    """Main dashboard of the game."""
    content, row, column = _dimension_input()
    game = lib.new_game(row, column)

    if content == 'EMPTY':
        lib.print_board(game)
        handle_command(game)
    else:
        new_game = lib.fill_board(content, game)
        lib.print_board(new_game)
        handle_command(new_game)


if __name__ == '__main__':
    run_game()

