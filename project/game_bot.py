from typing import Optional, TYPE_CHECKING
from project.game_bet import Wheel
from project.game_strategy import (
    Strategy,
    ClassicStrategy,
    RiskyStrategy,
    NoobStrategy,
    ProStrategy,
    ScamStrategy,
    AggressiveStrategy,
)

if TYPE_CHECKING:
    from project.game_bet import Bet
    from project.game_strategy import Strategy


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

    def make_bet(self, wheel: Wheel) -> "Bet":
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
