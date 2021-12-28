from wallet.wallet import Wallet

transaction_queue = []


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
    share_usd = []  # positive: share to usd, negative: usd to share, (amount, wallet)
    basis_usd = []  # positive: basis to usd, negative: usd to basis, (amount, wallet)
    for transaction in transaction_queue:
        if transaction[0] == "share":  # share -> usd
            while len(share_usd) != 0 and share_usd[0][0] < 0:
                amount = min(abs(share_usd[0][0]), transaction[2])
                transaction[2] -= amount
                share_usd[0][0] += amount
                transaction[3].add_usd(amount)
        elif transaction[1] == "bond":  # basis -> bond
            pass
        elif transaction[0] == "basis":  # basis -> usd
            pass
        elif transaction[1] == "share":  # usd -> share
            pass
        elif transaction[1] == "basis":  # usd -> basis
            pass
