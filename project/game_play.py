from typing import List
from project.game_bet import Wheel
from project.game_bot import Bot


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
