from oracles.token_stat import *
from utils.sys_time import current_date
import protocol.treasury as main_treasury
import oracles.exchange as ex

maximum_date = 10
last_date = -1
last_prices = [1, 1]


def share_supply_trajectory():
    return ex.share_supply_trajectory


def share_demand_trajectory():
    return ex.share_demand_trajectory


def basis_supply_trajectory():
    return ex.basis_supply_trajectory


def basis_demand_trajectory():
    return ex.basis_demand_trajectory


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
    basis_supply_tr = basis_supply_trajectory()
    basis_demand_tr = basis_demand_trajectory()

    basis_demand_size = basis_demand_tr[-1][1]
    basis_supply_size = basis_supply_tr[-1][1]

    if basis_demand_size <= 1 or basis_supply_size <= 1:
        return basis_price_history[-2]

    price = basis_demand_size / basis_supply_size

    return max(price, 0.01)


def get_share_token_price():
    share_supply_tr = share_supply_trajectory()
    share_demand_tr = share_demand_trajectory()

    share_demand_price = share_demand_tr[-1][0]
    share_demand_size = share_demand_tr[-1][1]
    share_supply_size = share_supply_tr[-1][1]

    if share_demand_size < 1 or share_supply_size < 1:
        return share_demand_price[-2]

    price = share_demand_size / share_supply_size
    return max(price, 0.01)


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
    global maximum_date

    basis_price = get_basis_price()
    prior_bond = get_prior_bond_sum()
    treasury = get_treasury()

    ratio = prior_bond / treasury
    expected_days_to_redeem = ((1 / (1 - ratio)) - 1) * maximum_date / 2
    alpha = get_daily_inflation_rate()
    if alpha < 0:
        raise "Alpha should be a positive constant."
    if (basis_price > 0.9) and (basis_price < 1.1):
        return basis_price

    if expected_days_to_redeem > maximum_date:
        return 0.01

    elif ratio < 1:
        return (alpha ** expected_days_to_redeem) * basis_price
    else:
        return basis_price


def get_prior_bond_sum():
    return main_treasury.sum_issued_bonds


def get_treasury():
    return main_treasury.treasury


def launcher(_maximum_date=10):
    global maximum_date, last_date, last_prices
    del last_prices
    maximum_date = _maximum_date
    last_date = -1
    last_prices = [1, 1]
