# Datthew Nguyen - 61886297
import connectfour as c4
import common_library as c4_lib
import protocol_and_socket as network


def run_c4_online() -> None:
    """Dashboard of the program. It connects to a server then plays Connect Four against that server."""
    c4_lib.welcome_player()
    host, port, username = network.address_and_port_from_user()
    connection_list = network.server_connection(host, port, username)
    if connection_list == 'FAILED':
        return
    else:
        c4_server = connection_list[0]
        server_input = connection_list[1]
        user_message = connection_list[2]
    game = c4.new_game()
    end_game = False
    while not end_game:
        if game.turn == 1:
            c4_lib.print_board(game)
            print('Red, it is your turn.')
            player_move = c4_lib.ask_for_move()
            game = c4_lib.process_move(player_move, game)
            server_respone = network.send_move(player_move, server_input, user_message)
            if server_respone is None:
                print('Sorry, you might have done something that upsets the server.\nOr the server is acting weird.')
                end_game = network.disconnect(c4_server, server_input, user_message)
            elif server_respone == 'VALID' or server_respone == 'INVALID':
                pass
        else:
            c4_lib.print_board(game)
            respone = network.receive_move(server_input)
            if respone is None:
                end_game = network.disconnect(c4_server, server_input, user_message)
            game = c4_lib.process_move(respone, game)
            if game.turn == 2:
                end_game = network.disconnect(c4_server, server_input, user_message)
        winner = c4.winner(game)
        if winner != 0:
            if winner == 1:
                print('You have won the game.')
            elif winner == 2:
                print('The winner is the server')
            end_game = True
            c4_lib.print_board(game)


if __name__ == '__main__':
    run_c4_online()
