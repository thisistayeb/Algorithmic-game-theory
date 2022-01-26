from agents.agent import Agent
from oracles.oracle import get_token_price
from wallet.wallet import Wallet
from utils.random_generator import random_uniform

class IdealAgent3(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):

        max_basis=20
        random_split = random_uniform(2,100)
        prices = get_token_price()  # (basis, share, bond)
        if prices[0] == 1:
            pass
        elif prices[0] > random_uniform(1,max_basis):
            self.sell_basis(self.wallet.basis / random_split)
        elif prices[0] < random_uniform(0.1,0.99):
            self.buy_basis(self.wallet.usd / random_split)
            if prices[0] > prices[2]:
                self.buy_bond(self.wallet.basis / random_split)
