from agents.agent import Agent
from wallet.wallet import Wallet
from oracles.oracle import get_token_price
import random


class BondLover(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)
        self.random_price = random.uniform(1.2, 10)

    def action(self):
        prices = get_token_price()  # (basis, share, bond)
        if prices[0] > self.random_price:
            self.sell_basis(random.uniform(0, self.wallet.basis / 5))
        else:
            if self.wallet.usd > 0:
                self.buy_basis(random.uniform(0, self.wallet.usd / 5))
            if self.wallet.basis > 0 and 1 >= prices[0] >= prices[2]:
                self.buy_bond(random.uniform(0, self.wallet.basis / 5))
