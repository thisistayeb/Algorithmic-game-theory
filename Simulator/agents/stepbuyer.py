from agents.agent import Agent
from wallet.wallet import Wallet
import random


class StepBuyer(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)
        self.N = random.uniform(5, 20)

    def action(self):
        usd_portion = self.wallet.usd / self.N
        if self.wallet.usd > 0:
            self.buy_basis(usd_portion)

        elif self.wallet.basis > 0:
            random_amount_basis = random.uniform(0, self.wallet.basis / 10)
            self.sell_basis(random_amount_basis)

        elif self.wallet.shares > 0:
            self.sell_share(self.wallet.shares)
