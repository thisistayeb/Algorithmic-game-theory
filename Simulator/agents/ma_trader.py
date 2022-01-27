"""
In this trader, the moving average is calculated based on the last N days.
N is randomly chosen for an agent between 10 and 40.
"""

from agents.agent import Agent
from wallet.wallet import Wallet
from oracles.oracle import get_token_price
from oracles.token_stat import get_basis_history
from utils.random_generator import random_uniform
import random


class MATrader(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)
        self.N = random_uniform(10, 40)

    def action(self):
        basis_price_history = get_basis_history()  # (basis,share,bond)
        prices = get_token_price()
        if len(basis_price_history) < self.N:
            pass
        else:
            moving_average = sum(basis_price_history[-self.N :]) / self.N

            if moving_average >= prices[0]:
                random_amount_usd = random.uniform(0, self.wallet.usd / 10)
                self.buy_basis(random_amount_usd)
            else:
                random_amount_basis = random.uniform(0, self.wallet.basis / 10)
                self.sell_basis(random_amount_basis)
