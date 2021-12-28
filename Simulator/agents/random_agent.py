from agent import Agent
from wallet.wallet import Wallet


class RandomAgent(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        pass
