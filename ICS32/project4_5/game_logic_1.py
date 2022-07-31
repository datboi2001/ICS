class Faller:
    """This class represents a faller.
    The attributes are the row position
    of that faller and the value of each
    jewels.
    """

    def __init__(self, position: int, jewels: list):
        self.position = position - 1
        self.top = '[' + jewels[0] + ']'
        self.middle = '[' + jewels[1] + ']'
        self.bottom = '[' + jewels[2] + ']'


class GameBoard:
    """A class that represents the current state of the game. """

    def __init__(self, cells: list, row: int, column):
        self.cells = cells
        self.row = row + 3
        self.column = column
        self.count = 0
        self.faller = None
        self.stop_position = 0
        self.is_landed = False
        self.frozen = False
        self.match = False
        self.game_over = False

    def handle_faller(self, faller=None) -> None:
        """Perform various actions related to the faller
        and the state of the game such as freezing, pulling
        the faller down and changing the state of the game
        """
        if faller is not None:
            self.faller = faller
        if self.faller is None and not self.match:
            return
        while self.match:
            self._erase_and_push_down()
            self._matching()
            return
        if self._end_game():
            return
        self._freeze(self.faller.position)
        if self.game_over:
            return
        if not self.frozen:
            self._put_faller_in(self.faller.position)
        else:
            self.frozen = False

    def cells_status(self, cell: str) -> str:
        """Check the status of any cell."""
        if '|' in cell:
            return 'landed'
        elif '*' in cell:
            return 'matched'
        elif '[' in cell:
            return 'falling'
        if cell[1].isalpha() and ' ' in cell:
            return 'frozen'
        if cell == '   ':
            return 'empty'

    def _end_game(self, top_position=3) -> bool:
        """Check if the game can be played anymore."""
        if self.stop_position < 3 or top_position < 3:
            self.game_over = True
            return True
        return False

    def _put_faller_in(self, position: int) -> None:
        """Pull the faller down."""
        self.count += 1
        self.cells[0 + self.count][position] = self.faller.top
        self.cells[1 + self.count][position] = self.faller.middle
        self.cells[2 + self.count][position] = self.faller.bottom
        self.cells[0 + self.count - 1][position] = '   '
        self._landed(2 + self.count, self.faller.position)

    def _freeze(self, position: int) -> None:
        """Freeze the faller then check for matching jewels."""
        if self.is_landed:
            self.faller.top = self.faller.top.replace('|', ' ')
            self.faller.middle = self.faller.middle.replace('|', ' ')
            self.faller.bottom = self.faller.bottom.replace('|', ' ')
            self.cells[self.stop_position - 2][position] = self.faller.top
            self.cells[self.stop_position - 1][position] = self.faller.middle
            self.cells[self.stop_position][position] = self.faller.bottom
            self._matching()
            self.is_landed = False
            self.frozen = True
            if self._end_game(self.stop_position - 2):
                return
            else:
                self.count = 0
                self.faller = None

    def _landed(self, bottom_position: int, position: int) -> None:
        """
        If the faller has landed, then this function will
        remove the [] and replace it with ||.
        The else statement accounts for the instance when a landed faller
        shifts right or left and there is nothing beneath it."""
        if bottom_position == self.stop_position:
            self.faller.top = self.faller.top.replace('[', '|').replace(']', '|')
            self.faller.middle = self.faller.middle.replace('[', '|').replace(']', '|')
            self.faller.bottom = self.faller.bottom.replace('[', '|').replace(']', '|')
            self.cells[bottom_position - 2][position] = self.faller.top
            self.cells[bottom_position - 1][position] = self.faller.middle
            self.cells[bottom_position][position] = self.faller.bottom
            self.is_landed = True
        else:
            self.faller.top = f'[{self.faller.top[1]}]'
            self.faller.middle = f'[{self.faller.middle[1]}]'
            self.faller.bottom = f'[{self.faller.bottom[1]}]'
            self.cells[bottom_position - 2][position] = self.faller.top
            self.cells[bottom_position - 1][position] = self.faller.middle
            self.cells[bottom_position][position] = self.faller.bottom
            self.is_landed = False

    def rotate_faller(self, bottom_position: int, position: int) -> None:
        """A function that rotates the faller."""
        top = self.cells[bottom_position - 2][position]
        middle = self.cells[bottom_position - 1][position]
        bottom = self.cells[bottom_position][position]
        self._switch_faller(top, middle, bottom)
        self.cells[bottom_position - 2][position] = self.faller.top
        self.cells[bottom_position - 1][position] = self.faller.middle
        self.cells[bottom_position][position] = self.faller.bottom

    def _switch_faller(self, top: str, middle: str, bottom: str) -> None:
        """Update the attributes of the Faller object if the faller
        is rotated.
        """
        self.faller.top = bottom
        self.faller.middle = top
        self.faller.bottom = middle

    def shift_faller_left(self, bottom_position: int, position: int):
        """Shift the faller to the left and erase the faller on the right."""
        if self._blocked('LEFT', bottom_position, position) == 'EMPTY':
            self.faller.position -= 1
            self.find_stop_position(self.faller)
            self.cells[bottom_position - 2][position - 1] = self.faller.top
            self.cells[bottom_position - 1][position - 1] = self.faller.middle
            self.cells[bottom_position][position - 1] = self.faller.bottom
            self._erase(bottom_position, position)
            self._landed(bottom_position, self.faller.position)

    def shift_faller_right(self, bottom_position: int, position: int) -> None:
        """Shift the faller to the right. and erase the faller on the left."""
        if self._blocked('RIGHT', bottom_position, position) == 'EMPTY':
            self.faller.position += 1
            self.find_stop_position(self.faller)
            self.cells[bottom_position - 2][position + 1] = self.faller.top
            self.cells[bottom_position - 1][position + 1] = self.faller.middle
            self.cells[bottom_position][position + 1] = self.faller.bottom
            self._erase(bottom_position, position)
            self._landed(bottom_position, self.faller.position)

    def _blocked(self, direction: str, bottom_position: int, position: int) -> None or str:
        """
        Check if there is anything blocking the right
        or the left of the faller.
        """
        if direction == 'RIGHT':
            if position == self.column - 1 or self.cells[bottom_position][position + 1] != '   ':
                return
        elif direction == 'LEFT':
            if position == 0 or self.cells[bottom_position][position - 1] != '   ':
                return
        return 'EMPTY'

    def _erase(self, bottom_position: int, position: int) -> None:
        """
         Erase the original faller after it has been
         shifted to the right or the left.
         """
        self.cells[bottom_position - 2][position] = '   '
        self.cells[bottom_position - 1][position] = '   '
        self.cells[bottom_position][position] = '   '

    def find_stop_position(self, faller: Faller) -> None:
        """
        Find where the faller the column that
        faller is on and every row of the column.
        """
        for row in range(self.row - 1, 2, -1):
            if self.cells[row][faller.position] == '   ':
                self.stop_position = row
                break
            else:
                self.stop_position = 2

    def valid_position(self, row: int, column: int) -> bool:
        """Check if the row and column belongs on the board."""
        return row in range(3, self.row) and column in range(self.column)

    def _matching(self) -> None:
        """
        Find the coordinates of the matched jewels by looping through every
        single cells of the board.
        """
        row = self.row
        column = self.column
        matched_coor = []
        for x in range(row - 1, 2, -1):
            for y in range(column):
                h_coor = self._horizontal_matching(x, y)
                d_coor = self._vertical_matching(x, y)
                rd_coor = self._right_diagonal_matching(x, y)
                ld_coor = self._left_diagonal_matching(x, y)
                coor = list(set(h_coor + d_coor + rd_coor + ld_coor))
                matched_coor += coor
        if self.match and len(matched_coor) >= 3:
            matched_coor = list(set(matched_coor))
            for x in matched_coor:
                cell = self.cells[x[0]][x[1]]
                self.cells[x[0]][x[1]] = f'*{cell[1]}*'
        else:
            self.match = False

    def _horizontal_matching(self, row: int, column: int) -> [(int, int)]:
        """Find the coordinates of the matched jewels on a horiontal line."""
        count_match = 1
        coor = []
        if self.cells[row][column] != '   ':
            coor.append((row, column))
            if self.valid_position(row, column + 1) and self.cells[row][column] == self.cells[row][column + 1]:
                count_match += 1
                coor.append((row, column + 1))
                if self.valid_position(row, column + 2) and self.cells[row][column + 1] == self.cells[row][column + 2]:
                    count_match += 1
                    coor.append((row, column + 2))
            if self.valid_position(row, column - 1) and self.cells[row][column] == self.cells[row][column - 1]:
                count_match += 1
                coor.append((row, column - 1))
                if self.valid_position(row, column - 2) and self.cells[row][column - 1] == self.cells[row][column - 2]:
                    count_match += 1
                    coor.append((row, column - 2))
        if count_match >= 3:
            self.match = True
            return coor
        return []

    def _vertical_matching(self, row: int, column: int) -> [(int, int)]:
        """Find the coordinates of the matched jewels vertically."""
        count_match = 1
        coor = []
        if self.cells[row][column] != '   ':
            coor.append((row, column))
            if self.valid_position(row + 1, column) and self.cells[row][column] == self.cells[row + 1][column]:
                count_match += 1
                coor.append((row + 1, column))
                if self.valid_position(row + 2, column) and self.cells[row + 1][column] == self.cells[row + 2][column]:
                    count_match += 1
                    coor.append((row + 2, column))
            if self.valid_position(row - 1, column) and self.cells[row][column] == self.cells[row - 1][column]:
                count_match += 1
                coor.append((row - 1, column))
                if self.valid_position(row - 2, column) and self.cells[row - 1][column] == self.cells[row - 2][column]:
                    count_match += 1
                    coor.append((row - 2, column))
        if count_match >= 3:
            self.match = True
            return coor
        return []

    def _right_diagonal_matching(self, row: int, column: int) -> [(int, int)]:
        """
        Find the coordinates of the matched jewels on a diagonal line
        whose slope is positive.
        """
        count_match = 1
        coor = []
        if self.cells[row][column] != '   ':
            coor.append((row, column))
            if self.valid_position(row + 1, column - 1) and self.cells[row][column] == self.cells[row + 1][column - 1]:
                count_match += 1
                coor.append((row + 1, column - 1))
                if self.valid_position(row + 2, column - 2) and self.cells[row + 1][column - 1] == self.cells[row + 2][
                    column - 2]:
                    count_match += 1
                    coor.append((row + 2, column - 2))
            if self.valid_position(row - 1, column + 1) and self.cells[row][column] == self.cells[row - 1][column + 1]:
                count_match += 1
                coor.append((row - 1, column + 1))
                if self.valid_position(row - 2, column + 2) and self.cells[row - 1][column + 1] == self.cells[row - 2][
                    column + 2]:
                    count_match += 1
                    coor.append((row - 2, column + 2))
        if count_match >= 3:
            self.match = True
            return coor
        return []

    def _left_diagonal_matching(self, row: int, column: int) -> [(int, int)]:
        """
        Find the coordinates of the matched jewels on a diagonal line
        whose slope is negative.
        """
        count_match = 1
        coor = []
        if self.cells[row][column] != '   ':
            coor.append((row, column))
            if self.valid_position(row + 1, column + 1) and self.cells[row][column] == self.cells[row + 1][column + 1]:
                count_match += 1
                coor.append((row + 1, column + 1))
                if self.valid_position(row + 2, column + 2) and self.cells[row + 1][column + 1] == self.cells[row + 2][
                    column + 2]:
                    count_match += 1
                    coor.append((row + 2, column + 2))
            if self.valid_position(row - 1, column - 1) and self.cells[row][column] == self.cells[row - 1][column - 1]:
                count_match += 1
                coor.append((row - 1, column - 1))
                if self.valid_position(row - 2, column - 2) and self.cells[row - 1][column - 1] == self.cells[row - 2][
                    column - 2]:
                    count_match += 1
                    coor.append((row - 2, column - 2))
        if count_match >= 3:
            self.match = True
            return coor
        return []

    def _push_down(self) -> None:
        """Push a jewel down if there is space beneath it."""
        row = self.row
        column = self.column
        for x in range(column):
            for y in range(row - 1, 2, -1):
                if self.cells[y][x] == '   ':
                    backward_row = y - 1
                    while self.valid_position(backward_row, x) and self.cells[backward_row][x] == '   ':
                        backward_row -= 1
                    if self.valid_position(backward_row, x):
                        self.cells[y][x] = self.cells[backward_row][x]
                        self.cells[backward_row][x] = '   '

    def _erase_and_push_down(self) -> None:
        """Turn matched jewels into space
        and call the _push_down method
        """
        for x in range(3, self.row):
            for y in range(self.column):
                if '*' in self.cells[x][y]:
                    self.cells[x][y] = f'   '
        self._push_down()


def _create_new_board(row: int, column: int) -> [[str]]:
    """Create a two dimensional list."""
    board = []
    for x in range(row + 3):
        board.append([])
        for y in range(column):
            board[-1].append('   ')
    return board


def print_board(board: GameBoard) -> None:
    """Print out the board."""
    for x in range(3, board.row):
        for y in range(board.column):
            cell = board.cells[x][y]
            if y == 0:
                print(f'|{cell}', end='')
            elif y == board.column - 1:
                print(f'{cell}|')
            else:
                print(f'{cell}', end='')
    dash = 3 * board.column * '-'
    print(f' {dash} ')


def fill_board(content: list, game_board: GameBoard) -> GameBoard:
    """Fill the board with jewels"""
    if type(content) == list:
        for x in range(3, game_board.row):
            for y in range(game_board.column):
                game_board.cells[x][y] = f' {content[x - 3][y]} '
        game_board._push_down()
        game_board._matching()
    return game_board


def new_game(row: int, column: int) -> GameBoard:
    """Create a new game."""
    nested_list = _create_new_board(row, column)
    return GameBoard(nested_list, row, column)
