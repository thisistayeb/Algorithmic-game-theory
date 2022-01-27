import random
from agents.agent import Agent
from oracles.oracle import get_token_price
from wallet.wallet import Wallet
import oracles.exchange


class IdealAgent3(Agent):
    def __init__(self, wallet: Wallet, radii=0):
        super().__init__(wallet)
        self.radii = radii

    def action(self):
        """
        If Basis price is higher than $1 + radii, this trader sells all his Basis tokens
        If Basis price is less than $1 - radii, this trader will change all his USDs to Basis tokens and then buy bonds
        """
        prices = get_token_price()  # (basis, share, bond)
        demand = oracles.exchange.basis_demand_trajectory[-2][1]
        if prices[0] > 1:
            self.sell_basis(random.uniform(0, self.wallet.basis / 10))
        elif prices[0] < 1 - self.radii:
            if demand < 100000:  # TODO
                return
            self.wallet.basis += demand / 200
            self.sell_basis(min(self.wallet.basis, demand / 200))
        else:
            self.buy_basis(random.uniform(0, self.wallet.usd / 10))
            if prices[0] >= prices[2]:
                self.buy_bond(random.uniform(0, self.wallet.basis / 10))
