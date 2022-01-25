from agents.agent import Agent
from wallet.wallet import Wallet
from oracles.oracle import get_token_price
import random


class TenStep(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        prices = get_token_price()  # (basis, share, bond)

        random_amount_basis = random.uniform(0, self.wallet.basis / 10)
        ten_percent_usd = self.wallet.usd / 10
        random_amount_shares = random.uniform(0, self.wallet.shares / 10)

        if self.wallet.usd < 1:
            self.sell_basis(random_amount_basis)

        else:
            self.buy_basis(ten_percent_usd)
