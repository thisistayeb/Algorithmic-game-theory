# we can create a class for oracles.
from utils.random_generator import random_gauss, random_uniform
from oracles.token_stat import *
from utils.sys_time import current_date
from oracles.exchange import (
    basis_supply_trajectory,
    basis_demand_trajectory,
    share_supply_trajectory,
    share_demand_trajectory,
)

last_date = -1
last_prices = [0, 0, 0]


def get_token_price():
    global last_date, last_prices
    cur_date = current_date()
    if cur_date == last_date:
        return last_prices
    # returns a tuple which contains token prices (basis, shares, bond)
    basis_price = get_basis_price()
    share_token_price = get_share_token_price()
    bond_price = get_bond_price()

    last_date = cur_date
    last_prices = [basis_price, share_token_price, bond_price]

    return last_prices


def get_basis_price():
    global basis_supply_trajectory
    global basis_demand_trajectory

    basis_demand_price = basis_demand_trajectory[-1][0]
    basis_demand_size = basis_demand_trajectory[-1][1]
    basis_supply_price = basis_supply_trajectory[-1][0]
    basis_supply_size = basis_supply_trajectory[-1][1]

    price = (
        (basis_demand_price * basis_demand_size)
        + (basis_supply_price * basis_supply_size)
    ) / (basis_supply_size + basis_demand_size)

    return price


def get_share_token_price():
    global share_supply_trajectory
    global share_demand_trajectory

    share_demand_price = share_demand_trajectory[-1][0]
    share_demand_size = share_demand_trajectory[-1][1]
    share_supply_price = share_supply_trajectory[-1][0]
    share_supply_size = share_supply_trajectory[-1][1]

    price = (
        (share_demand_price * share_demand_size)
        + (share_supply_price * share_supply_size)
    ) / (share_supply_size + share_demand_size)

    return price


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
