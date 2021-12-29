from agent import Agent
from wallet.wallet import Wallet
from oracles.oracle import get_token_price


class ShareLover(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        if self.wallet.usd > 0:
            self.buy_share(self.wallet.usd)

