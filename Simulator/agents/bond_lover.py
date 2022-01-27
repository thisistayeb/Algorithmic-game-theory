from agents.agent import Agent
from wallet.wallet import Wallet
from oracles.oracle import get_token_price
from utils.random_generator import random_uniform


class BondLover(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)
        self.random_price = random_uniform(1.2, 10)

    def action(self):
        prices = get_token_price()  # (basis, share, bond)
        if prices[0] > self.random_price:
            self.sell_basis(self.wallet.basis)
        else:
            if self.wallet.usd > 0:
                self.buy_basis(self.wallet.usd)
            if self.wallet.basis > 0 and prices[0] > prices[2]:
                self.buy_bond(self.wallet.basis)
