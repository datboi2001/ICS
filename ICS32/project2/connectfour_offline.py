# Datthew Nguyen - 61886297
import connectfour as c4
import common_library as c4_lib


def run_c4_offline() -> None:
    """Dashboard of console-version Connect Four."""
    c4_lib.welcome_player()
    game = c4.new_game()
    c4_lib.print_board(game)
    end_game = False
    while not end_game:
        print("It is {}'s turn".format(c4_lib.print_turn(game)))
        player_move = c4_lib.ask_for_move()
        game = c4_lib.process_move(player_move, game)
        c4_lib.print_board(game)
        winner = c4.winner(game)
        if winner == 1:
            print('The winner is Red.')
            end_game = True
        elif winner == 2:
            print('The winner is Yellow')
            end_game = True


if __name__ == '__main__':
    run_c4_offline()
