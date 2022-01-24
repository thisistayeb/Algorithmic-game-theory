from agents.agent import Agent
from wallet.wallet import Wallet
from oracles.oracle import get_basis_history, get_token_price
import random


class Trader(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        basis_price_history = get_basis_history()
        if len(basis_price_history) < 10:
            pass

        basis_price_temp = basis_price_history[-10:]
        basis_price_temp = basis_price_temp[::-1]

        alpha = random.random()
        discount_factors = [alpha ** i for i in range(10)]
        weights, overall_price = 1, 0
        for day in range(10):
            overall_price += basis_price_temp[day] * discount_factors[day]
            weights *= discount_factors[day]
            overall_price /= 10 * weights

        basis_price = get_token_price()[0]

        if overall_price > basis_price:
            random_amount_usd = random.uniform(0, self.wallet.usd // 10)
            self.buy_basis(random_amount_usd)
        else:
            random_amount_basis = random.uniform(0, self.wallet.basis // 10)
            self.sell_basis(random_amount_basis)
