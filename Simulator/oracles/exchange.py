import oracles.oracle
from wallet.wallet import Wallet
import oracles.oracle as oracle
import oracles.token_stat as token_stat
import protocol.treasury as treasury
from protocol.treasury import issue_bond
import numpy as np


transaction_queue = []
share_usd = []  # positive: share to usd, negative: usd to share, (amount, wallet)
basis_usd = []  # positive: basis to usd, negative: usd to basis, (amount, wallet)
bond_basis = []
basis_supply_trajectory = [[1, 1], [1, 1]]  # Save sum of basis's supply and mean price for each hour (price,size)
basis_demand_trajectory = [[1, 1], [1, 1]]  # Save sum of basis's demand and mean price for each hour (price,size)
share_supply_trajectory = [[1, 1], [1, 1]]  # Save sum of share's supply and mean price for each hour (price,size)
share_demand_trajectory = [[1, 1], [1, 1]]  # Save sum of share's demand and mean price for each hour (price,size)


# convert amount of first token to second token from wallet
def add_transaction(first, second, amount, wallet: Wallet):
    if amount < 1e-8:
        return False
    if first == "usd":
        if wallet.usd < amount:
            return False
        wallet.usd -= amount
    if first == "share":
        if wallet.shares < amount:
            return False
        wallet.shares -= amount
    if first == "basis":
        if wallet.basis < amount:
            return False
        wallet.basis -= amount
    transaction_queue.append([first, second, amount, wallet])


"""
share <-> usd
basis <-> usd
basis -> bond
"""


def handle_transactions():
    # asnp = np.asarray(transaction_queue)
    # print(asnp[:, :3])
    """
    give order pairs from agents and pay them with a FIFO algorithm.
    """
    prices = oracle.get_token_price()  # (basis, share, bond)
    prices = (prices[0], prices[1], prices[2] / prices[0])
    # 1 basis is equal to (prices[2] / prices[0]) amount of bonds

    """
    prices[2] = usd / bond
    prices[0] = usd / basis
    prices[2] / prices[0] = basis / bond
    """
    basis_demand = [1, 1]  # price and size
    basis_supply = [1, 1]  # price and size
    share_demand = [1, 1]  # price and size
    share_supply = [1, 1]  # price and size

    for transaction in transaction_queue:
        if transaction[0] == "usd":
            if transaction[1] == "basis":  # USD -> basis
                # price save weighted mean using 2 variables
                price = (
                                (basis_demand[0] * basis_demand[1]) + (transaction[2] * prices[0])
                        ) / (basis_demand[1] + transaction[2])
                basis_demand[0] = price
                basis_demand[1] += transaction[2]
            elif transaction[1] == "share":  # USD -> share
                # price save weighted mean using 2 variables
                price = (
                                (share_demand[0] * share_demand[1]) + (transaction[2] * prices[1])
                        ) / (share_demand[1] + transaction[2])
                share_demand[0] = price
                share_demand[1] += transaction[2]

            else:
                raise ValueError("Illegal transaction")
        elif transaction[0] == "share":
            if transaction[1] == "usd":  # share -> USD
                # price save weighted mean using 2 variables
                price = (
                                (share_supply[0] * share_supply[1]) + (transaction[2] * prices[1])
                        ) / (share_supply[1] + transaction[2])
                share_supply[0] = price
                share_supply[1] += transaction[2]

            else:
                raise ValueError("Illegal transaction")
        elif transaction[0] == "basis":
            if transaction[1] == "usd":  # basis -> USD
                # price save weighted mean using 2 variables
                price = (
                                (basis_supply[0] * basis_supply[1]) + (transaction[2] * prices[0])
                        ) / max(0.1, (basis_supply[1] + transaction[2]))
                basis_supply[0] = price
                basis_supply[1] += transaction[2]
        basis_demand_trajectory.append(basis_demand)
        basis_supply_trajectory.append(basis_supply)
        share_demand_trajectory.append(share_demand)
        share_supply_trajectory.append(share_supply)

    # print(f"Basis prices is {oracle.get_token_price()[0]}, Bond price is {oracle.get_token_price()[2] * prices[0]}")

    for transaction in transaction_queue:
        if transaction[0] == "share":  # share -> usd
            while (
                    (len(share_usd) != 0) and (share_usd[0][0] < 0) and (transaction[2] > 0)
            ):
                amount = min(abs(share_usd[0][0]), transaction[2] * prices[1])  # amount in dollars
                # pay usd to transaction[3]
                transaction[2] -= amount / prices[1]
                transaction[3].add_usd(amount)
                # pay share to share_usd[0][1]
                share_usd[0][0] += amount
                share_usd[0][1].add_share(amount / prices[1])
                # remove transaction from queue if needed
                if share_usd[0][0] == 0:
                    share_usd.pop(0)

            if transaction[2] > 0:
                share_usd.append([transaction[2], transaction[3]])
        elif transaction[1] == "bond":  # basis -> bond
            amount = 0
            if treasury.available_bonds > 0 and prices[0] < 1:
                amount = min(treasury.available_bonds, transaction[2] * prices[2])  # number of bonds
            transaction[2] -= amount / prices[2]
            issue_bond(transaction[3], amount, prices[2])  # catch error from treasury
            if transaction[2] > 0:
                bond_basis.append([transaction[2], transaction[3]])
        elif transaction[0] == "basis":  # basis -> usd
            while (
                    (len(basis_usd) != 0) and (basis_usd[0][0] < 0) and (transaction[2] > 0)
            ):
                amount = min(abs(basis_usd[0][0]), transaction[2] * prices[0])
                # pay usd to transaction[3]
                transaction[2] -= amount / prices[0]
                transaction[3].add_usd(amount)
                # pay basis to basis_usd[0][1]
                basis_usd[0][0] += amount
                basis_usd[0][1].add_basis(amount / prices[0])
                # remove transaction from queue if needed
                if basis_usd[0][0] == 0:
                    basis_usd.pop(0)

            if transaction[2] > 0:
                basis_usd.append([transaction[2], transaction[3]])
        elif transaction[1] == "share":  # usd -> share
            while (
                    (len(share_usd) != 0) and (share_usd[0][0] > 0) and (transaction[2] > 0)
            ):
                amount = min(share_usd[0][0] * prices[1], transaction[2])
                # pay share to transaction[3]
                transaction[2] -= amount
                transaction[3].add_share(amount / prices[1])
                # pay usd to share_usd[0][1]
                share_usd[0][0] -= amount / prices[1]
                share_usd[0][1].add_usd(amount)
                # remove transaction from queue if needed
                if share_usd[0][0] == 0:
                    share_usd.pop(0)

            if transaction[2] > 0:
                share_usd.append([-transaction[2], transaction[3]])
        elif transaction[1] == "basis":  # usd -> basis
            while (
                    (len(basis_usd) != 0) and (basis_usd[0][0] > 0) and (transaction[2] > 0)
            ):
                amount = min(basis_usd[0][0] * prices[0], transaction[2])
                # pay basis to transaction[3]
                transaction[2] -= amount
                transaction[3].add_basis(amount / prices[0])
                # pay usd to basis_usd[0][1]
                basis_usd[0][0] -= amount / prices[0]
                basis_usd[0][1].add_usd(amount)
                # remove transaction from queue if needed
                if basis_usd[0][0] == 0:
                    basis_usd.pop(0)

            if transaction[2] > 0:
                basis_usd.append([-transaction[2], transaction[3]])

    transaction_queue.clear()
    token_stat.basis_price_history.append(oracle.get_token_price()[0])
    token_stat.bond_price_history.append(oracle.get_token_price()[2])


def payback_transactions():
    """
    after paying transactions, some transactions will be canceled
    and payed tokens will returns to agent's wallets
    """
    # print("starting paybacks")
    for transaction in share_usd:
        if transaction[0] > 0:
            transaction[1].add_share(transaction[0])
        elif transaction[0] < 0:
            transaction[1].add_usd(-transaction[0])

    for transaction in basis_usd:
        if transaction[0] > 0:
            transaction[1].add_basis(transaction[0])
        elif transaction[0] < 0:
            transaction[1].add_usd(-transaction[0])

    for transaction in bond_basis:
        if transaction[0] != 0:
            transaction[1].add_basis(transaction[0])

    # if len(basis_usd) > 0:
    #     print(np.sum(np.asarray(basis_usd)[:, 0]))

    share_usd.clear()
    basis_usd.clear()
    bond_basis.clear()
