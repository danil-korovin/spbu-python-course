import pytest
from project.game import (
    Wheel,
    Color,
    SingleBet,
    SplitBet,
    StreetBet,
    ColorBet,
    DozenBet,
    SnakeBet,
    Bot,
    ClassicStrategy,
    RiskyStrategy,
    NoobStrategy,
    ProStrategy,
    ScamStrategy,
    AggressiveStrategy,
    Game,
)

import random


def test_wheel_spin():
    """Test spin() method"""
    wheel = Wheel()
    number = wheel.spin()
    assert number in wheel.NUMBERS
    number = random.randint(0, 36)
    assert number in wheel.NUMBERS


def test_get_color():
    """Test getting color"""
    wheel = Wheel()
    assert wheel.get_color(0) == Color.GREEN
    assert wheel.get_color(5) == Color.RED
    assert wheel.get_color(6) == Color.BLACK


def test_get_dozen():
    """Test getting dozens"""
    wheel = Wheel()
    assert wheel.get_dozen(0) is None
    assert wheel.get_dozen(5) == 1
    assert wheel.get_dozen(18) == 2
    assert wheel.get_dozen(30) == 3


def test_single_bet():
    """Test Single bet"""
    wheel = Wheel()
    bet = SingleBet(17, 10)
    assert bet.is_win(17, wheel)
    assert bet.coefficient() == 35


def test_split_bet():
    """Test Split bet"""
    wheel = Wheel()
    bet = SplitBet((1, 2), 20)
    assert bet.is_win(1, wheel)
    assert bet.is_win(2, wheel)
    assert bet.coefficient() == 17


def test_street_bet():
    """Test Street bet"""
    wheel = Wheel()
    bet = StreetBet(4, 10)
    assert bet.is_win(4, wheel)
    assert bet.is_win(5, wheel)
    assert bet.is_win(6, wheel)
    assert bet.coefficient() == 11


def test_color_bet():
    """Test Color bet"""
    wheel = Wheel()
    bet = ColorBet(Color.RED, 10)
    assert bet.is_win(19, wheel)
    assert bet.coefficient() == 1


def test_dozen_bet():
    """Test Dozen bet"""
    wheel = Wheel()
    bet = DozenBet(2, 15)
    assert bet.is_win(16, wheel)
    assert bet.coefficient() == 2


def test_snake_bet():
    """Test Snake bet"""
    wheel = Wheel()
    bet = SnakeBet(5)
    assert bet.is_win(1, wheel)
    assert bet.coefficient() == 2


def test_update_balance():
    """Test update balance"""
    bot = Bot("Bot", 500)
    old = bot.balance
    bot.update_balance(100)
    assert bot.balance == old + 100


@pytest.mark.parametrize(
    "balance, strategy_expect, bet_expect",
    [
        (50, "ClassicStrategy", ColorBet),
        (200, "RiskyStrategy", DozenBet),
        (400, "NoobStrategy", SnakeBet),
        (600, "ProStrategy", StreetBet),
        (800, "ScamStrategy", SplitBet),
        (1000, "AggressiveStrategy", SingleBet),
    ],
)
def test_strategy_and_bet(balance, strategy_expect, bet_expect):
    """Test strategy and bet"""
    bot = Bot("Bot", balance)
    bot.choose_strategy()
    assert bot.get_strategy_name() == strategy_expect
    wheel = Wheel()
    strategy = bot.strategy
    bet = strategy.bet(bot, wheel)
    assert isinstance(bet, bet_expect)


@pytest.mark.parametrize(
    "bet_class, init_args, win_number, lose_number, coefficient_expected",
    [
        (ColorBet, (Color.RED, 10), 32, 15, 1),
        (DozenBet, (1, 10), 5, 25, 2),
        (SnakeBet, (10,), 1, 2, 2),
        (StreetBet, (1, 10), 2, 5, 11),
        (SplitBet, ((2, 3), 10), 3, 10, 17),
        (SingleBet, (7, 10), 7, 8, 35),
    ],
)
def test_bet_payouts(
    bet_class, init_args, win_number, lose_number, coefficient_expected
):
    """Test bet payouts"""
    wheel = Wheel()
    bet = bet_class(*init_args)
    start_balance = 100
    bot = Bot("Bot", start_balance)
    win_balance = start_balance + bet.amount * bet.coefficient()
    assert bet.is_win(win_number, wheel)
    bot.update_balance(bet.amount * bet.coefficient())
    assert bot.balance == win_balance
    bot.balance = start_balance
    assert not bet.is_win(lose_number, wheel)
    bot.update_balance(-bet.amount)
    assert bot.balance == start_balance - bet.amount
    assert bet.coefficient() == coefficient_expected


@pytest.fixture
def bots():
    """Creates a list of bots"""
    return [
        Bot("Bot1", 50),
        Bot("Bot2", 200),
        Bot("Bot3", 400),
        Bot("Bot4", 600),
        Bot("Bot5", 800),
        Bot("Bot6", 1000),
    ]


@pytest.fixture
def main_game(bots):
    """Create game"""
    return Game(bots, max_rounds=5)


def test_game_initialization(main_game):
    """Test game initialization"""
    game = main_game
    assert game.round == 0
    assert len(game.bots) == 6
    for bot in game.bots:
        assert bot.balance > 0
        assert bot.strategy is None


def test_play_one_round(main_game):
    """Test one round"""
    game = main_game
    start_balances = {bot.name: bot.balance for bot in game.bots}
    game.play_round()
    assert game.round == 1
    balance_change = all(bot.balance != start_balances[bot.name] for bot in game.bots)
    assert balance_change
    assert not all(bot.strategy for bot in game.bots) is None


def test_final_results(main_game):
    """Test final result"""
    game = main_game
    game.play()
    assert game.round == game.max_rounds
    for bot in game.bots:
        assert isinstance(bot.balance, int)
        assert bot.balance >= 0
        assert bot.strategy is not None
        assert bot.get_strategy_name() in [
            "ClassicStrategy",
            "RiskyStrategy",
            "NoobStrategy",
            "ProStrategy",
            "ScamStrategy",
            "AggressiveStrategy",
        ]
        profit = bot.balance - bot.start_balance
        assert isinstance(profit, int)


def test_bot_with_zero_balance():
    """Test zero balance"""
    bot = Bot("Bot", 0)
    game = Game([bot], max_rounds=3)
    game.play()
    assert bot.balance == 0
    assert bot.get_strategy_name() == "None"
    assert game.round == game.max_rounds
