# Datthew Nguyen - 61886297
import socket

R_WIN = 'WINNER_RED\n'
Y_WIN = 'WINNER-YELLOW\n'


def address_and_port_from_user() -> (str, int, str):
    """Prompt the user to enter an IP address, a port and a username."""
    valid_host = False
    while not valid_host:
        host = input('Please enter an IP address you would like to connect to: ').strip()
        if host != '':
            valid_host = True
        else:
            print('Please enter something.')
    valid_port = False
    while not valid_port:
        try:
            port = int(input('Please enter a port to connect to the given host(0-65535): '))
            if 0 <= port <= 65535:
                valid_port = True
            else:
                print('That port is not in between 0 and 65535.')
        except ValueError:
            print("Please enter a number")
    space = False
    while not space:
        username = input('Please enter your username without spaces: ').strip()
        if ' ' not in username and username != '':
            space = True
    return host, port, username


def server_connection(host: str, p_num: int, username: str) -> str or None or [c4_server, server_input, user_message]:
    """Try to connect to the server. If the game is ready, print a message. Return a message and stop the program if there is a problem. Else, return the socket objects."""
    try:
        c4_server = socket.socket()
        address = (host, p_num)
        c4_server.connect(address)
        server_input = c4_server.makefile('r')
        user_message = c4_server.makefile('w')
        _write_to_server(user_message ,'I32CFSP_HELLO {}'.format(username))
        server_message = server_input.readline()
        if server_message != ('WELCOME {}\n'.format(username)):
            print('Sorry, you might be in a wrong server.')
            return 'FAILED'
        else:
            print('You are connected to the correct server.')
        _write_to_server(user_message, 'AI_GAME')
        server_message = server_input.readline()
        if server_message == 'READY\n':
            print('The server is ready to play the game')
            return [c4_server, server_input, user_message]
        else:
            print('Sorry, the server refused to play with you.')
            return
    except (socket.gaierror, ConnectionRefusedError, TimeoutError) as e:
        print('Sorry, please check your Internet Connection, your VPN connection and your input.')
        return 'FAILED'


def send_move(move: str, server_input: socket, user_message: socket) -> str or None:
    """Send the user's move to the connected server."""
    if move.startswith('DROP') or move.startswith('POP'):
        _write_to_server(user_message, move)
    else:
        return
    server_respone = server_input.readline()
    if server_respone == 'INVALID\n':
        server_respone = server_input.readline()
        if server_respone == 'READY\n':
            return 'INVALID'
        else:
            return
    elif server_respone == 'OKAY\n' or server_respone == R_WIN or server_respone == Y_WIN:
        return 'VALID'
    else:
        return


def receive_move(server_input: socket) -> str or None:
    """Receive the AI's move from the connected server."""
    server_respone = server_input.readline()
    if server_respone.startswith('DROP') or server_respone.startswith('POP'):
        print('\nThe AI has made the move: {}'.format(server_respone))
        server_input.readline()
        return server_respone
    else:
        return


def _write_to_server(user_message: socket, text: str) -> None:
    """Write a message to the server's output stream and flush it."""
    user_message.write(text + '\r\n')
    user_message.flush()

def disconnect(c4_server, server_input: socket, user_message: socket) -> bool:
    c4_server.close()
    server_input.close()
    user_message.close()
    return True