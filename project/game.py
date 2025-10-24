from typing import List, Dict, Tuple, Optional, Protocol, Set
from enum import Enum, auto
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


class Bot:
    """Simulation of a player"""

    def __init__(self, name: str, balance: int) -> None:
        """
        Initializes a bot.

        Args:
            name (str): Bot's name.
            balance (int): Starting balance.
        """
        self.name = name
        self.balance = balance
        self.start_balance = balance
        self.strategy: Optional[Strategy] = None

    def choose_strategy(self) -> None:
        """Selects a strategy based on balance."""
        if self.balance < 100:
            self.strategy = ClassicStrategy()
        elif self.balance < 300:
            self.strategy = RiskyStrategy()
        elif self.balance < 500:
            self.strategy = NoobStrategy()
        elif self.balance < 700:
            self.strategy = ProStrategy()
        elif self.balance < 900:
            self.strategy = ScamStrategy()
        else:
            self.strategy = AggressiveStrategy()

    def make_bet(self, wheel: Wheel) -> Bet:
        """
        Makes a bet based on strategy.

        Args:
            wheel (Wheel): The game wheel.

        Returns:
            Bet: Chosen bet.
        """
        self.choose_strategy()
        if self.strategy is None:
            raise RuntimeError("Strategy is not set for this bot.")
        return self.strategy.bet(self, wheel)

    def update_balance(self, amount: int) -> None:
        """
        Updates bot's balance.

        Args:
            amount (int): The amount of points.
        """
        self.balance += amount

    def get_strategy_name(self) -> str:
        """Returns the name of strategy."""
        if self.strategy:
            return self.strategy.__class__.__name__
        else:
            return "None"


class Strategy(ABC):
    """Abstract class for strategies."""

    @abstractmethod
    def bet(self, bot: Bot, wheel: Wheel) -> Bet:
        """Make a bet based on the bot's balance and strategy logic."""
        pass


class ClassicStrategy(Strategy):
    """Classic strategy with colors bat."""

    def bet(self, bot: Bot, wheel: Wheel) -> Bet:
        """
        Make a color bet.

        Args:
            bot (Bot): The bot makes the bet.
            wheel (Wheel): The roulette wheel.

        Returns:
            ColorBet: color RED or BLACK.
        """
        amount = max(1, bot.balance // 10)
        return ColorBet(random.choice([Color.RED, Color.BLACK]), amount)


class RiskyStrategy(Strategy):
    """Risky strategy with dozens bet."""

    def bet(self, bot: Bot, wheel: Wheel) -> Bet:
        """
        Make a dozen bet.

        Args:
            bot (Bot): The bot makes the bet.
            wheel (Wheel): The roulette wheel.

        Returns:
            DozenBet: Bet on random dozen.
        """
        amount = max(1, bot.balance // 5)
        return DozenBet(random.choice([1, 2, 3]), amount)


class NoobStrategy(Strategy):
    """Classic strategy with snake bet."""

    def bet(self, bot: Bot, wheel: Wheel) -> Bet:
        """
        Make a snake bet.

        Args:
            bot (Bot): The bot makes the bet.
            wheel (Wheel): The roulette wheel.

        Returns:
            SnakeBet: Snake bet
        """
        amount = max(1, bot.balance // 20)
        return SnakeBet(amount)


class ProStrategy(Strategy):
    """Pro strategy with street bet."""

    def bet(self, bot: Bot, wheel: Wheel) -> Bet:
        """
        Make a street bet.

        Args:
            bot (Bot): The bot makes the bet.
            wheel (Wheel): The roulette wheel.

        Returns:
            StreetBet: Bet on random street.
        """
        amount = max(1, bot.balance // 10)
        return StreetBet(
            random.choice([i for i in range(1, 35) if (i - 1) % 3 == 0]), amount
        )


class ScamStrategy(Strategy):
    """Scam strategy with split bet."""

    def bet(self, bot: Bot, wheel: Wheel) -> Bet:
        """
        Make a split bet.

        Args:
            bot (Bot): The bot makes the bet.
            wheel (Wheel): The roulette wheel.

        Returns:
            SplitBet: Split bet.
        """
        a = random.randint(1, 35)
        amount = max(1, bot.balance // 5)
        return SplitBet((a, a + 1), amount)


class AggressiveStrategy(Strategy):
    """Aggressive strategy with single bet."""

    def bet(self, bot: Bot, wheel: Wheel) -> Bet:
        """
        Make a single number bet.

        Args:
            bot (Bot): The bot makes the bet.
            wheel (Wheel): The roulette wheel.

        Returns:
            SingleBet: Single number bet.
        """
        amount = max(1, bot.balance // 10)
        return SingleBet(random.randint(1, 36), amount)


class Game:
    """Roulette game simulation."""

    def __init__(self, bots: List[Bot], max_rounds: int) -> None:
        """Initializes the game."""
        self.bots = bots
        self.max_rounds = max_rounds
        self.wheel = Wheel()
        self.round = 0

    def play_round(self) -> None:
        """Plays one round of the roulette game."""
        self.round += 1
        print(f"\nRound {self.round}")
        number = self.wheel.spin()
        color = self.wheel.get_color(number)
        print(f"Winning number: {number}")
        for bot in self.bots:
            if bot.balance <= 0:
                continue
            print(f"\n{bot.name}")
            print(f"Balance: {bot.balance}")
            main_bet = bot.make_bet(self.wheel)
            if main_bet.amount > bot.balance:
                print("Not enough balance")
                continue
            win = 0
            print(f"Bet amount: {main_bet.amount}")
            if main_bet.is_win(number, self.wheel):
                payout = main_bet.amount * main_bet.coefficient()
                print(f"Bet: {main_bet.prints()}")
                print(f"Coefficient: {main_bet.coefficient()}")
                print(f"Result: Wins {payout}")
                win += payout
                bot.update_balance(win)
            else:
                print(f"Bet: {main_bet.prints()}")
                print(f"Result: Loses {main_bet.amount}")
                bot.update_balance(-main_bet.amount)

            print(f"Strategy: {bot.get_strategy_name()}")
            print(f"New balance: {bot.balance}")

    def play(self) -> None:
        """Simulate all rounds of the game."""
        for i in range(self.max_rounds):
            self.play_round()
        print("\nGame Over")
        bot_profits = []
        for bot in self.bots:
            profit = bot.balance - bot.start_balance
            bot_profits.append((bot, profit))
            print(f"{bot.name}: Final Balance = {bot.balance}")
            if profit > 0:
                result = "Wins"
                print(f"{result} {profit}")
            elif profit < 0:
                result = "Loses"
                print(f"{result} {profit}")
            else:
                result = "Same"
                print(f"{result} {profit}")
