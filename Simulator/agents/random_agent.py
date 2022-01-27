from agents.agent import Agent
from wallet.wallet import Wallet
from oracles.oracle import get_token_price
import random
import numpy as np


class RandomAgent(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        r = random.uniform(0, 0.1)
        choice = random.choice([1, 2, 3, 4, 5])
        prices = get_token_price()  # (basis, share, bond)
        if choice == 1:
            self.buy_basis(self.wallet.usd * r)
        if choice == 2:
            self.sell_basis(self.wallet.basis * r)
        if choice == 3 and prices[0] >= prices[2]:
            self.buy_bond(self.wallet.basis * r)
        if choice == 4:
            self.buy_share(self.wallet.usd * r)
        if choice == 5:
            self.sell_share(self.wallet.shares * r)
