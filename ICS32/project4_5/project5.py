import game_logic_1 as lib
import pygame
import random

ROW = 13
COLUMNS = 6
FPS = 12
jewels_list = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']


class ColumnsGame:
    def __init__(self):
        self._state = lib.new_game(ROW, COLUMNS)
        self._running = True
        self._background_color = pygame.Color(0, 0, 0)  # Black
        self._board_color = pygame.Color(116, 119, 122)  # Gray
        self._window = None
        self._time_counter = FPS
        self._jewel_size = 1 / (self._state.row - 3)

    def start_game(self) -> None:
        """Start the game."""
        pygame.init()
        try:
            clock = pygame.time.Clock()
            self._resize_surface((300, 500))
            while self._running:
                clock.tick(FPS)
                self._time_counter -= 1
                self._handle_events()
                if self._time_counter == int(FPS/2):
                    self._flow()
                    self._time_counter = FPS
                self._draw_game()
        finally:
            pygame.quit()

    def _handle_events(self) -> None:
        """Handle all events happening inside the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
        self._handle_keys()

    def _handle_keys(self) -> None:
        """Handle the keys from the user."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self._state.faller is None:
                self._draw_board()
            else:
                self._state.shift_faller_left(2 + self._state.count, self._state.faller.position)
        if keys[pygame.K_RIGHT]:
            if self._state.faller is None:
                self._draw_board()
            else:
                self._state.shift_faller_right(2 + self._state.count, self._state.faller.position)
        if keys[pygame.K_SPACE]:
            if self._state.faller is None:
                self._draw_board()
            else:
                self._state.rotate_faller(2 + self._state.count, self._state.faller.position)
        if keys[pygame.K_LSHIFT]:
            self._time_counter = 0
        if keys[pygame.K_RSHIFT]:
            self._time_counter = FPS

    def _flow(self):
        """This function handles the flow of time."""
        while self._state.match:
            self._state._erase_and_push_down()
            self._state._matching()
        if self._state.faller is None:
            jewel1 = jewels_list[random.randint(0, len(jewels_list) - 1)]
            jewel2 = jewels_list[random.randint(0, len(jewels_list) - 1)]
            jewel3 = jewels_list[random.randint(0, len(jewels_list) - 1)]
            column = self.get_random_column()
            faller_list = [jewel1, jewel2, jewel3]
            faller = lib.Faller(column, faller_list)
            self._state.find_stop_position(faller)
            self._state.handle_faller(faller)
        else:
            self._state.handle_faller()
        if self._state.game_over:
            self._running = False

    def get_random_column(self) -> int:
        """Check if the column is full of jewels.
        If it is, then the randint will generate
        a new number. If all columns are full, randint
        will generate a random number and set self._state.game_over to True."""
        content_list = []
        is_full = True
        while is_full:
            column = random.randint(1, COLUMNS)
            for x in range(3, self._state.row):
                content_list.append(self._state.cells[x][column - 1])
            if any(x == '   ' for x in content_list):
                is_full = False
                return column
            else:
                content_list.clear()
        return random.randint(1, COLUMNS)

    def _draw_game(self) -> None:
        """Draw the window and the board of the game."""
        self._window.fill(self._background_color)
        self._draw_board()
        pygame.display.flip()

    def _draw_board(self):
        """
        Draw the board then loop through the two dimensional list
        to draw each jewel.
        """
        top_leftX = self._frac_x_to_pixel_x(0)
        top_leftY = self._frac_y_to_pixel_y(0)
        width = self._frac_x_to_pixel_x(1)
        height = self._frac_y_to_pixel_y(1)

        board = pygame.Rect(top_leftX, top_leftY, width, height)
        pygame.draw.rect(self._window, self._board_color, board, 0)

        for row in range(self._state.row - 1, 2, -1):
            for column in range(self._state.column):
                self._draw_jewel(row, column)

    def _draw_jewel(self, row: int, column: int) -> None:
        """
        This function draws a jewel from the board.
        If the jewel is '   ' then a gray jewel with green outline will be drawn.
        The jewel will be white if it is in a matched line.
        The jewel will have a white outline if it's landed.
        """
        cell = self._state.cells[row][column]
        status = self._state.cells_status(cell)
        if cell == '   ':
            cell_color = (116, 119, 122)  # Gray
        if status == 'matched':
            cell_color = (252, 255, 255)  # White
        if status == 'falling' or status == 'landed' or status == 'frozen':
            cell_color = self._get_jewel_color(cell)
        jewel_color = pygame.Color(cell_color[0], cell_color[1], cell_color[2])
        jewel_x_coor = (column * 1 / 6)
        jewel_y_coor = ((row - 3) * self._jewel_size)

        jewel_x_pixel_coor = self._frac_x_to_pixel_x(jewel_x_coor)
        jewel_y_pixel_coor = self._frac_y_to_pixel_y(jewel_y_coor)

        jewel_width = self._frac_x_to_pixel_x(1 / 6)
        jewel_height = self._frac_y_to_pixel_y(self._jewel_size)

        jewel_rect = pygame.Rect(jewel_x_pixel_coor, jewel_y_pixel_coor, jewel_width, jewel_height)
        pygame.draw.rect(self._window, cell_color, jewel_rect, 0)
        if status == 'landed':
            pygame.draw.rect(self._window, pygame.Color(255, 255, 255), jewel_rect, 2)  # White
        elif status == 'falling':
            pygame.draw.rect(self._window, pygame.Color(116, 119, 122), jewel_rect, 2)  # Gray
        elif status == 'empty' or status == 'frozen':
            pygame.draw.rect(self._window, pygame.Color(2, 51, 34), jewel_rect, 2)

    def _get_jewel_color(self, jewel) -> (int, int, int):
        """Define the RGB code of the jewels."""
        if 'S' in jewel:  # Red
            return (252, 3, 3)
        if 'T' in jewel:  # Yellow
            return (252, 244, 3)
        if 'V' in jewel:  # Green
            return (11, 252, 3)
        if 'W' in jewel:  # Black
            return (0, 0, 0)
        if 'X' in jewel:  # Purple
            return (252, 3, 248)
        if 'Y' in jewel:  # Blue
            return (57, 3, 252)
        if 'Z' in jewel:  # Teal:
            return (15, 217, 210)

    def _resize_surface(self, size: (int, int)) -> None:
        """Resize the window and name the window."""
        self._window = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption("Columns by Datthew Nguyen")

    def _frac_x_to_pixel_x(self, frac: float) -> int:
        """Converts a fractional x value to its pixel value."""
        return int(frac * self._window.get_width())

    def _frac_y_to_pixel_y(self, frac: float) -> int:
        """Converts a fractional y value to its pixel value."""
        return int(frac * self._window.get_height())


if __name__ == "__main__":
    ColumnsGame().start_game()
