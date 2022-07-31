# test_calculator.py
#
# ICS 32 Winter 2020
# Code Example
#
# These are the unit tests for our calculator.py module.  Note that
# there's nothing here that attempts to unit test the tkinter-based
# GUI.  Our only goal here is to test the "model", yet that's where
# most of the complexity lies in a completed calculator implementation,
# anyway.
#
# We're using the "unittest" module for our testing, as we did in the
# "Test-Driven Development" notes earlier in the quarter.  There
# aren't a lot of new techniques, though we are trying to do a slightly
# better job of factoring our commonalities among the tests.

from calculator import Calculator
import unittest


class CalculatorTests(unittest.TestCase):
    # We realized early on that most of our tests were going to follow
    # the same basic pattern: handle a sequence of keys being sent to
    # a calculator, then see what the display says.  So we wrote this
    # one method that can run that test for us.  You give it a string
    # containing the sequence of keys, as well as a string containing
    # the expected result.  It creates a calculator, asks it to
    # handle each key in the sequence, then asserts that the
    # calculator's display has the correct result.
    def _assert_sequence_result(self, keys: str, result: str) -> None:
        calculator = Calculator()

        for key in keys:
            calculator.handle(key)

        self.assertEqual(calculator.display(), result)

    # Now that we have _assert_sequence_result, the tests themselves
    # become a bunch of calls to _assert_sequence_result.  I still
    # think there's value in having these categorized as separate,
    # named test methods, because the names are communicating
    # something important: What are we actually trying to verify
    # with each of these cases?  This way, when the tests fail, we'll
    # see the name and it will tell us something about what kind
    # of problem we should be looking for.

    def test_initial_display_is_zero(self):
        self._assert_sequence_result('', '0')

    def test_initially_pressing_equals_gives_zero(self):
        self._assert_sequence_result('=', '0')

    def test_starting_with_digit_replaces_zero(self):
        self._assert_sequence_result('3', '3')
        self._assert_sequence_result('4', '4')

    def test_two_digits_concatenates_instead_of_replacing(self):
        self._assert_sequence_result('74', '74')
        self._assert_sequence_result('89', '89')

    def test_many_digits_concatenates_instead_of_replacing(self):
        self._assert_sequence_result('12579', '12579')
        self._assert_sequence_result('3704', '3704')

    def test_equals_without_operation_changes_nothing(self):
        self._assert_sequence_result('35=', '35')
        self._assert_sequence_result('35===', '35')

    def test_addition_and_equals(self):
        self._assert_sequence_result('5+6=', '11')

    def test_subtraction_and_equals(self):
        self._assert_sequence_result('5-6=', '-1')

    def test_sequence_of_operations(self):
        self._assert_sequence_result('5+6+3+4=', '18')


if __name__ == '__main__':
    unittest.main()