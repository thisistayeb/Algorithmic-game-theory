from agent import Agent
from wallet.wallet import Wallet
from oracles.oracle import get_token_price


class BondLover(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        prices = get_token_price()  # (basis, share, bond)
        self.buy_bond()
