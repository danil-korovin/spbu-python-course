from typing import List, Dict, Tuple, Optional
from enum import Enum
from abc import ABC, abstractmethod
import random


class Color(Enum):
    """Color of number."""

    RED = "RED"
    BLACK = "BLACK"
    GREEN = "GREEN"


class Wheel:
    """A roulette wheel"""

    NUMBERS: List[int] = [
        0,
        32,
        15,
        19,
        4,
        21,
        2,
        25,
        17,
        34,
        6,
        27,
        13,
        36,
        11,
        30,
        8,
        23,
        10,
        5,
        24,
        16,
        33,
        1,
        20,
        14,
        31,
        9,
        22,
        18,
        29,
        7,
        28,
        12,
        35,
        3,
        26,
    ]

    RED: List[int] = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]

    BLACK: List[int] = [
        15,
        4,
        2,
        17,
        6,
        13,
        11,
        8,
        10,
        24,
        33,
        20,
        31,
        22,
        29,
        28,
        35,
        26,
    ]

    def __init__(self) -> None:
        """Initializes and creates a list of dozens."""
        self.number_to_dozen: Dict[int, Optional[int]] = {0: None}
        for n in range(1, 37):
            if 1 <= n <= 12:
                self.number_to_dozen[n] = 1
            elif 13 <= n <= 24:
                self.number_to_dozen[n] = 2
            else:
                self.number_to_dozen[n] = 3

    def spin(self) -> int:
        """
        Roulette spin.

        Returns:
            int: The winning number.
        """
        return random.choice(self.NUMBERS)

    def numbers(self) -> List[int]:
        """Returns all ordered numbers."""
        return self.NUMBERS

    def get_color(self, number: int) -> Color:
        """
        Gets the color of number.

        Args:
            number (int): The roulette number.

        Returns:
            Color: The color of the number.
        """
        if number == 0:
            return Color.GREEN
        elif number in self.RED:
            return Color.RED
        elif number in self.BLACK:
            return Color.BLACK
        else:
            raise ValueError("Wrong number")

    def get_dozen(self, number: int) -> Optional[int]:
        """
        Gets the number of dozen.

        Args:
            number (int): Roulette number.

        Returns:
            Optional[int]: The dozen number.
        """
        return self.number_to_dozen.get(number)


class Bet(ABC):
    """Abstract class for a bet."""

    def __init__(self, amount: int) -> None:
        """
        Initializes a bet.

        Args:
            amount (int): Bet amount.
        """
        self.amount = amount

    @abstractmethod
    def is_win(self, number: int, wheel: Wheel) -> bool:
        """Check if the bet wins."""
        pass

    @abstractmethod
    def coefficient(self) -> int:
        """Return the payout coefficient."""
        pass

    @abstractmethod
    def prints(self) -> str:
        """Return a string representation of the bet."""
        pass


class SingleBet(Bet):
    """Single number bet."""

    def __init__(self, number: int, amount: int) -> None:
        """
        Initialize single number bet.

        Args:
            number (int): Number to bet.
            amount (int): Amount of money on the bet.
        """
        self.amount = amount
        self.number = number

    def is_win(self, number: int, wheel: Wheel) -> bool:
        """
        Check if the bet wins.

        Args:
            number (int): The number of the wheel.
            wheel (Wheel): The roulette wheel.

        Returns:
            bool: True if number matches.
        """
        return self.number == number

    def coefficient(self) -> int:
        """Return the payout coefficient."""
        return 35

    def prints(self) -> str:
        """Return a string representation of the bet."""
        return f"SingleBet({self.number})"


class SplitBet(Bet):
    """Split bet."""

    def __init__(self, numbers: Tuple[int, int], amount: int) -> None:
        """
        Initialize split bet.

        Args:
            numbers (Tuple[int, int]): Two numbers to bet.
            amount (int): The amount of money placed on the bet.
        """
        self.amount = amount
        self.numbers = numbers

    def is_win(self, number: int, wheel: Wheel) -> bool:
        """
        Check if the bet wins.

        Args:
            number (int): The number of the wheel.
            wheel (Wheel): The roulette wheel.

        Returns:
            bool: True if the number is in Split.
        """
        if number in self.numbers:
            return True
        else:
            return False

    def coefficient(self) -> int:
        """Return the payout coefficient."""
        return 17

    def prints(self) -> str:
        """Return a string representation of the bet."""
        return f"SplitBet{self.numbers}"


class StreetBet(Bet):
    """Street bet."""

    def __init__(self, number: int, amount: int) -> None:
        """
        Initialize street bet.

        Args:
            number (int): The first number in street.
            amount (int): Amount of money placed on the bet.
        """
        self.amount = amount
        self.number = number

    def is_win(self, number: int, wheel: Wheel) -> bool:
        """
        Check if the bet wins.

        Args:
            number (int): The number of the wheel.
            wheel (Wheel): The roulette wheel.

        Returns:
            bool: True if the number is in street.
        """
        street = (self.number, self.number + 1, self.number + 2)
        if number in street:
            return True
        else:
            return False

    def coefficient(self) -> int:
        """Return the payout coefficient."""
        return 11

    def prints(self) -> str:
        """Return a string representation of the bet."""
        return f"StreetBet({self.number}-{self.number + 2})"


class ColorBet(Bet):
    """Bet on color."""

    def __init__(self, color: Color, amount: int) -> None:
        """
        Initialize color bet.

        Args:
            color (Color): The color to bet.
            amount (int): Amount of money placed on the bet.
        """
        self.amount = amount
        self.color = color

    def is_win(self, number: int, wheel: Wheel) -> bool:
        """
        Check if the bet wins.

        Args:
            number (int): The number of the wheel.
            wheel (Wheel): The roulette wheel.

        Returns:
            bool: True if the color matches the bet.
        """
        return wheel.get_color(number) == self.color

    def coefficient(self) -> int:
        """Return the payout coefficient."""
        return 1

    def prints(self) -> str:
        """Return a string representation of the bet."""
        return f"Color({self.color.name})"


class DozenBet(Bet):
    """Bet on dozens."""

    def __init__(self, dozen: int, amount: int) -> None:
        """
        Initialize dozen bet.

        Args:
            dozen (int): The dozen to bet.
            amount (int): Amount of money placed on the bet.
        """
        self.amount = amount
        self.dozen = dozen

    def is_win(self, number: int, wheel: Wheel) -> bool:
        """
        Check if the bet wins.

        Args:
            number (int): The number of the wheel.
            wheel (Wheel): The roulette wheel.

        Returns:
            bool: True if the number is in chosen dozen.
        """
        return wheel.get_dozen(number) == self.dozen

    def coefficient(self) -> int:
        """Return the payout coefficient."""
        return 2

    def prints(self) -> str:
        """Return a string representation of the bet."""
        return f"Dozen({self.dozen})"


class SnakeBet(Bet):
    """Snake bet"""

    SNAKE = {1, 5, 9, 12, 14, 16, 19, 23, 27, 30, 32, 34}

    def __init__(self, amount: int) -> None:
        """
        Initialize a snake bet.

        Args:
            amount (int): Amount of money placed on the bet.
        """
        self.amount = amount

    def is_win(self, number: int, wheel: Wheel) -> bool:
        """
        Check if the bet wins.

        Args:
            number (int): The number of the wheel.
            wheel (Wheel): The roulette wheel.

        Returns:
            bool: True if the number is in Snake.
        """
        return number in self.SNAKE

    def coefficient(self) -> int:
        """Return the payout coefficient."""
        return 2

    def prints(self) -> str:
        return "SnakeBet"
