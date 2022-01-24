from agents.agent import Agent
from wallet.wallet import Wallet


class Trader(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        random_amount_usd = random.uniform(0, self.wallet.usd // 10)
        self.buy_basis(random_amount_usd)
