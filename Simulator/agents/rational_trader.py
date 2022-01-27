from agents.agent import Agent
from wallet.wallet import Wallet
from oracles.oracle import get_token_price
from oracles.token_stat import get_basis_history
import random


class RationalTrader(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)
        self.alpha = random.random()

    def action(self):
        basis_price_history = get_basis_history()  # (basis,share,bond)
        prices = get_token_price()
        if len(basis_price_history) < 10:
            pass
        else:
            basis_price_temp = basis_price_history[-10:]
            basis_price_temp = basis_price_temp[::-1]

            discount_factors = [self.alpha ** i for i in range(10)]
            weights, overall_price = 0, 0
            for day in range(10):
                overall_price += basis_price_temp[day] * discount_factors[day]
                weights += discount_factors[day]
            overall_price /= weights

            if (overall_price > prices[0]) and (prices[0] > prices[2]):
                random_amount_usd = random.uniform(0, self.wallet.usd / 10)
                self.buy_basis(random_amount_usd)
            else:
                random_amount_basis = random.uniform(0, self.wallet.basis / 10)
                self.sell_basis(random_amount_basis)
