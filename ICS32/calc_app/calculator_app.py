# calculator_app.py
#
# ICS 32 Winter 2020
# Code Example
#
# This is a tkinter-based user interface for our calculator.
# It consists of a grid containing a label in the top row,
# then a few rows and columns of the calculator's buttons.

from calculator import Calculator
import tkinter


_DEFAULT_FONT = ('Helvetica', 20)


class CalculatorApp:
    def __init__(self):
        # First, we create the model for our calculator.  It knows
        # how to do the calculations, but knows nothing about the
        # user interface.
        self._calculator = Calculator()

        # Next, we create a Tk object for our application, which gives
        # us (among other things) a "root window" for it.
        self._root_window = tkinter.Tk()

        # Then, we create a label that we'll use to display the
        # calculator's result.  The "anchor" option is used to specify
        # that we want the text within the label to be (in this case)
        # right-justified.
        self._display_label = tkinter.Label(
            master = self._root_window,
            text = '', font = _DEFAULT_FONT,
            anchor = tkinter.E)

        # We'll have our display label span the entire top row of our
        # grid, and we'll set "sticky" so that it will stretch when the
        # size of the window stretches to become wider (or compress when
        # the window becomes narrower).
        self._display_label.grid(
            row = 0, column = 0, columnspan = 4,
            sticky = tkinter.W + tkinter.E)

        # Rather than set up sixteen separate buttons by hand, we realized
        # that what we need to do for each button is almost identical:
        # Decide what text should be in it, where it should be, and what
        # should be sent to the model when that button is pressed.
        # So we wrote a method that we could call to create and return
        # us each button.
        button_7 = self._create_button('7', 1, 0)
        button_8 = self._create_button('8', 1, 1)
        button_9 = self._create_button('9', 1, 2)
        button_divide = self._create_button('/', 1, 3)
        button_4 = self._create_button('4', 2, 0)
        button_5 = self._create_button('5', 2, 1)
        button_6 = self._create_button('6', 2, 2)
        button_multiply = self._create_button('*', 2, 3)
        button_1 = self._create_button('1', 3, 0)
        button_2 = self._create_button('2', 3, 1)
        button_3 = self._create_button('3', 3, 2)
        button_subtract = self._create_button('-', 3, 3)
        button_clear = self._create_button_with_command('C', 4, 0, self._clear)
        button_0 = self._create_button('0', 4, 1)
        button_dot = self._create_button('=', 4, 2)
        button_plus = self._create_button('+', 4, 3)

        # This is where we configure how the widths and heights of the
        # rows and columns of the grid change as the size of the window
        # changes.  This, in turn, causes the widgets to either move or
        # resize within those rows and columns -- depending on the
        # "sticky" values given to them when we associated them with
        # the grid.
        self._root_window.rowconfigure(0, weight = 0)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.rowconfigure(2, weight = 1)
        self._root_window.rowconfigure(3, weight = 1)
        self._root_window.rowconfigure(4, weight = 1)

        self._root_window.columnconfigure(0, weight = 1)
        self._root_window.columnconfigure(1, weight = 1)
        self._root_window.columnconfigure(2, weight = 1)
        self._root_window.columnconfigure(3, weight = 1)


    def run(self) -> None:
        # When we first start our application, we'll refresh the
        # display (ask the model "What should I show?" and then
        # show it).
        self._refresh_display()

        # Then we'll put Tkinter in charge by calling mainloop()
        # on our root window.
        self._root_window.mainloop()


    def _create_button(self, text, row, column) -> tkinter.Button:
        return self._create_button_with_command(
            text, row, column, self._make_command(text))


    def _create_button_with_command(self, text, row, column, command) -> tkinter.Button:
        button = tkinter.Button(
            master = self._root_window,
            text = text, font = _DEFAULT_FONT,
            command = command)

        button.grid(
            row = row, column = column,
            sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)

        return button


    # Notice that the _make_command method is using the
    # function-that-builds-and-returns-function pattern
    # discussed in the notes, because each button needs a
    # slightly different function, but we didn't want to write
    # all sixteen of them by hand.

    def _make_command(self, key: str) -> 'function':
        def command_function() -> None:
            self._calculator.handle(key)
            self._refresh_display()

        return command_function


    def _refresh_display(self) -> None:
        # This sets the "text" option of the label, which causes
        # it to display different text.
        self._display_label['text'] = self._calculator.display()


    def _clear(self) -> None:
        self._calculator = Calculator()
        self._refresh_display()



if __name__ == '__main__':
    CalculatorApp().run()