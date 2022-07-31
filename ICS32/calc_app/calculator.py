# calculator.py
#
# ICS 32 Winter 2020
# Code Example
#
# A partial implementation of the "model" for our calculator.
# What it supports is what is testing in "test_calculator.py",
# but it is not complete.  For example, it has no support
# for multiplication or division, even though these buttons
# exist in the user interface).
#
# How our model works is like this:
#
# * Keep track of the "current value", which is what would be
#   displayed on the calculator at any given time.
# * Keep track of the "remembered value", which is the value
#   that would be used as the first operand to any operation.
#   For example, if you press the '+' button, the remembered
#   value is the current value, the current value is 0, and
#   we can begin entering our second operation.
# * Starting an operation (like '+') or pressing the '=' key
#   performs any operation that's pending.
#
# Much about this remains skeletal, but it's a very nice start.


class Calculator:
    def __init__(self):
        self._current_value = 0
        self._remembered_value = 0
        self._last_operation = _no_operation

    def display(self) -> str:
        return str(self._current_value)

    def handle(self, key: str) -> None:
        if key.isdigit():
            self._current_value *= 10
            self._current_value += int(key[0])
        elif key in ['=', '+', '-']:
            result = self._last_operation(
                self._remembered_value, self._current_value)

            if key == '=':
                self._remembered_value = 0
                self._current_value = result
            else:
                self._remembered_value = result
                self._current_value = 0

            if key == '+':
                self._last_operation = _add
            elif key == '-':
                self._last_operation = _subtract
            else:
                self._last_operation = _no_operation


# These functions are the operations that can be performed.
# Note that we're storing these in our model in an attribute
# that keeps track of what function needs to be called to
# to perform the last operation someone asked for.

def _no_operation(remembered: int, current: int) -> int:
    return current


def _add(remembered: int, current: int) -> int:
    return remembered + current


def _subtract(remembered: int, current: int) -> int:
    return remembered - current
