from agent import Agent
from wallet.wallet import Wallet
import random

class RandomAgent(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        random_amount_basis = random.uniform(0,self.wallet.basis)
        random_amount_usd = random.uniform(0,self.wallet.usd)
        random_amount_shares = random.uniform(0,self.wallet.shares)
        choice = random.choice(["buy_basis", "sell_basis", "sell_share", "buy_share", "buy_bond"])
        if choice == "buy_basis":
            self.buy_basis(random_amount_usd)
        if choice = "sell_basis":
            self.sell_basis(random_amount_basis)
        if choice == "buy_bond":
            self.buy_bond(random_amount_basis)
        if choice = "buy_share":
            self.buy_share(random_amount_usd)
        if choice = "sell_share":
            self.sell_share(random_amount_shares)