from wallet.wallet import Wallet
from oracles.oracle import get_token_price
from protocol.treasury import available_bonds, issue_bond

transaction_queue = []
share_usd = []  # positive: share to usd, negative: usd to share, (amount, wallet)
basis_usd = []  # positive: basis to usd, negative: usd to basis, (amount, wallet)
bond_basis = []


# convert amount of first token to second token from wallet
def add_transaction(first, second, amount, wallet: Wallet):
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
    transaction_queue.append((first, second, amount, wallet))


"""
share <-> usd
basis <-> usd
basis -> bond
"""


def handle_transactions():
    """
    give order pairs from agents and pay them with a FIFO algorithm.
    """
    prices = get_token_price()  # (basis, share, bond)
    prices[2] /= prices[0]  # basis -> bond
    """
    prices[2] = usd / bond
    prices[0] = usd / basis
    prices[2] / prices[0] = basis / bond
    """

    for transaction in transaction_queue:
        if transaction[0] == "share":  # share -> usd
            while (len(share_usd) != 0) and (share_usd[0][0] < 0) and (transaction[2] > 0):
                amount = min(abs(share_usd[0][0]), transaction[2])
                # pay usd to transaction[3]
                transaction[2] -= amount
                transaction[3].add_usd(amount * prices[1])
                # pay share to share_usd[0][1]
                share_usd[0][0] += amount
                share_usd[0][1].add_share(amount / prices[1])
                # remove transaction from queue if needed
                if share_usd[0][0] == 0:
                    share_usd.pop(0)

            if transaction[2] > 0:
                share_usd.append((transaction[2], transaction[3]))
        elif transaction[1] == "bond":  # basis -> bond
            amount = min(available_bonds, transaction[2] / prices[2])
            transaction[2] -= amount
            issue_bond(transaction[3], amount, prices[2])
            if transaction[2] > 0:
                bond_basis.append((transaction[2], transaction[3]))
        elif transaction[0] == "basis":  # basis -> usd
            while (len(basis_usd) != 0) and (basis_usd[0][0] < 0) and (transaction[2] > 0):
                amount = min(abs(basis_usd[0][0]), transaction[2])
                # pay usd to transaction[3]
                transaction[2] -= amount
                transaction[3].add_usd(amount * prices[0])
                # pay basis to basis_usd[0][1]
                basis_usd[0][0] += amount
                basis_usd[0][1].add_basis(amount / prices[0])
                # remove transaction from queue if needed
                if basis_usd[0][0] == 0:
                    basis_usd.pop(0)

            if transaction[2] > 0:
                basis_usd.append((transaction[2], transaction[3]))
        elif transaction[1] == "share":  # usd -> share
            while (len(share_usd) != 0) and (share_usd[0][0] > 0) and (transaction[2] > 0):
                amount = min(share_usd[0][0], transaction[2])
                # pay share to transaction[3]
                transaction[2] -= amount
                transaction[3].add_share(amount / prices[1])
                # pay usd to share_usd[0][1]
                share_usd[0][0] -= amount
                share_usd[0][1].add_usd(amount * prices[1])
                # remove transaction from queue if needed
                if share_usd[0][0] == 0:
                    share_usd.pop(0)

            if transaction[2] > 0:
                share_usd.append((-transaction[2], transaction[3]))
        elif transaction[1] == "basis":  # usd -> basis
            while (len(basis_usd) != 0) and (basis_usd[0][0] > 0) and (transaction[2] > 0):
                amount = min(basis_usd[0][0], transaction[2])
                # pay basis to transaction[3]
                transaction[2] -= amount
                transaction[3].add_basis(amount / prices[0])
                # pay usd to basis_usd[0][1]
                basis_usd[0][0] -= amount
                basis_usd[0][1].add_usd(amount * prices[0])
                # remove transaction from queue if needed
                if basis_usd[0][0] == 0:
                    basis_usd.pop(0)

            if transaction[2] > 0:
                basis_usd.append((-transaction[2], transaction[3]))

    transaction_queue.clear()


def payback_transactions():
    """
    after paying transactions, some transactions will be canceled
    and payed tokens will returns to agent's wallets
    """
    for transaction in share_usd:
        if transaction[0] > 0:
            transaction[1].add_share(transaction[0])
        elif transaction[0] < 0:
            transaction[1].add_usd(transaction[0])

    for transaction in basis_usd:
        if transaction[0] > 0:
            transaction[1].add_basis(transaction[0])
        elif transaction[0] < 0:
            transaction[1].add_usd(transaction[0])

    for transaction in bond_basis:
        if transaction[0] != 0:
            transaction[1].add_basis(transaction[0])

    share_usd.clear()
    basis_usd.clear()
    bond_basis.clear()
