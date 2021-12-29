# we can create a class for oracles.
from utils.random_generator import random_gauss, random_uniform
from oracles.token_stat import *


def get_token_price():
    # returns a tuple which contains token prices (basis, shares, bond)
    basis_price = get_basis_price()
    share_token_price = get_share_token_price()
    bond_price = get_bond_price()

    return basis_price, share_token_price, bond_price


def get_basis_price():
#Basis Price prediction assumes that the price is depend on last 10 days.
    basis_price_history = get_basis_history()
    if len(basis_price_history) < 10:
        price = max(basis_price_history[-1] + random_gauss(0, 0.1), random_uniform(0.1,0.5))
        basis_price_history.append(price)
        return price
        

    basis_price_temp = basis_price_history[-10:]
    basis_price_temp = basis_price_temp[::-1]

    alpha = 0.9  # or get mean of daily interest rate
    discount_factors = [alpha ** i for i in range(10)]
    weights, overall_price = 0,0
    for day in range(10):
        overall_price += basis_price_temp[day] * discount_factors[day]
        weights *= discount_factors[day]
        overall_price /= (10 * weights)

    return random_gauss(overall_price, overall_price // 4)


def get_share_token_price():
    """
        Share holders get rewarded when no prior bound exists, and each rewarded equally

        define Ratio of debt, wit
    """
    basis_price = get_basis_price()
    prior_bond = get_prior_bond_sum()
    treasury = get_treasury()
    each_token_reward = get_each_basis_reward()
    discount_factor = get_daily_inflation_rate()

    minimum_reward = each_token_reward * basis_price
    maximum_price = minimum_reward / (1 - discount_factor)  # Geometric Series goes to infinity
    price = random_uniform(minimum_reward, maximum_price)
    ratio = prior_bond / treasury

    expected_to_rewarded = 1 - ratio  # honestly, linear expectation for no reason

    if ratio > 1:
        return 0
    else:
        return expected_to_rewarded * price


def get_bond_price():
    """
    1. Basis price is an upper bound price for Bond price
    2. Expected days is an exponential function of the ratio of debt
    3. After five years, bonds are worthless

    Upon calculating the expected days to redeem the bonds, we calculate the bond price using the daily interest rate
    The model for calculating expected days depends on the ratio between debt and all tokens:

              1
      ( ______________  - 1) * (maximum_date / 2)
          1 - ratio

    The bond price is calculated using the expected days, the daily rate, and the expected days to get the basis tokens

      [(daily interest rate) ** (expected days)] * basis price

     If ratio → 1 , expected days → ∞, bond price → 0
     %%% Zero division Error when ratio = 1 %%%
    """

    basis_price = get_basis_price()
    prior_bond = get_prior_bond_sum()
    treasury = get_treasury()
    maximum_date = 5 * 365

    ratio = prior_bond / treasury
    expected_days_to_redeem = ((1 / (1 - ratio)) - 1) * maximum_date / 2
    alpha = get_daily_inflation_rate()
    if ratio < 1:
        return (alpha ** expected_days_to_redeem) * basis_price
    else:
        return 0
