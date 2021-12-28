from protocol.treasury import treasury, share_tokens, sum_issued_bonds
import math

basis_size_history = []
basis_price_history = []


def get_basis_history():
    return basis_size_history, basis_price_history


def get_prior_bond_sum():
    return sum_issued_bonds


def get_each_basis_reward():
    basis_price = basis_price_history[-1]
    if basis_price > 1:
        return ((1 - basis_price) * treasury) / share_tokens
    else:
        return 0


def get_daily_inflation_rate():
    daily = basis_price_history[-2] / basis_price_history[-1]
    contracted = math.sqrt(daily)
    return contracted


def get_treasury():
    return treasury
