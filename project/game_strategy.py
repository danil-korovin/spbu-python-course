from typing import Optional, TYPE_CHECKING
from abc import ABC, abstractmethod
from project.game_bet import (
    Color,
    ColorBet,
    DozenBet,
    SnakeBet,
    StreetBet,
    SplitBet,
    SingleBet,
)
import random

if TYPE_CHECKING:
    from project.game_bot import Bot
    from project.game_bet import Wheel, Bet


class Strategy(ABC):
    """Abstract class for strategies."""

    @abstractmethod
    def bet(self, bot: "Bot", wheel: "Wheel") -> "Bet":
        """Make a bet based on the bot's balance and strategy logic."""
        pass


class ClassicStrategy(Strategy):
    """Classic strategy with colors bat."""

    def bet(self, bot: "Bot", wheel: "Wheel") -> "Bet":
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

    def bet(self, bot: "Bot", wheel: "Wheel") -> "Bet":
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

    def bet(self, bot: "Bot", wheel: "Wheel") -> "Bet":
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

    def bet(self, bot: "Bot", wheel: "Wheel") -> "Bet":
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

    def bet(self, bot: "Bot", wheel: "Wheel") -> "Bet":
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

    def bet(self, bot: "Bot", wheel: "Wheel") -> "Bet":
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
