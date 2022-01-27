import oracles
from assets.bond import Bond
from utils.sys_time import current_date, convert_time
import protocol.agents_database as database

# TODO
"""
add Enum for handling different tokens
"""


treasury = 10 ** 5
share_tokens = 10 ** 2
bond_queue = []
available_bonds = 0
sum_issued_bonds = 0
expire_days = convert_time(days=10)


def create_bond():  # calculate available bonds for sell to agents
    global available_bonds
    if (
        oracles.oracle.get_token_price()[0] < 0.9
    ):  # first element of "get price tuple" is basis
        amount = ((1 / oracles.oracle.get_token_price()[0]) - 1) * treasury
        available_bonds = amount
    elif oracles.oracle.get_token_price()[0] > 1:
        available_bonds = 0


def issue_bond(wallet, amount, price_per_one):  # create bond and add it to wallet
    if amount == 0:
        return
    global treasury, sum_issued_bonds, available_bonds
    if amount > available_bonds:
        raise "Currently, there are not enough bonds available"
    new_bond = Bond(owner_id=wallet.address, create_date=current_date(), amount=amount)
    bond_queue.append(new_bond)
    wallet.add_bond(new_bond)
    treasury -= amount * price_per_one
    available_bonds -= amount
    sum_issued_bonds += amount


def pay_share_token_holder(amount):  # pay extra basis token to all share holders
    each_token = amount / share_tokens
    for wallet in database.wallets:
        wallet.add_basis(wallet.shares * each_token)


def create_tokens():
    global treasury
    if (
        oracles.oracle.get_token_price()[0] > 1.1
    ):  # first element of "get price tuple" is basis
        amount = (oracles.oracle.get_token_price()[0] - 1) * treasury
        treasury += amount
        amount = prone_bond_queue(amount)
        if amount < 0:
            print(amount)
        pay_share_token_holder(amount)


def redeem_certain_bond(bond, amount):  # redeem a certain bond
    global sum_issued_bonds
    bond.amount -= amount
    sum_issued_bonds -= amount
    database.address_to_wallet[bond.owner_id].add_basis(amount)


def redeem_bonds(can_redeem):  # redeem bonds from bond_queue
    while len(bond_queue) > 0 and can_redeem > 0:
        while len(bond_queue) > 0 and bond_queue[0].amount <= 1e-8:
            bond_queue.pop(0)
        if len(bond_queue) == 0:
            break
        amount = min(bond_queue[0].amount, can_redeem)
        redeem_certain_bond(bond_queue[0], amount)
        can_redeem -= amount
    return can_redeem


def prone_bond_queue(can_redeem):  # remove expired bonds and redeem some of them
    global sum_issued_bonds
    today = current_date()
    while len(bond_queue) > 0 and today >= bond_queue[0].create_date + expire_days:
        sum_issued_bonds -= bond_queue[0].amount
        bond_queue.pop(0)

    return redeem_bonds(can_redeem)


def launcher(_treasury=10 ** 5, _shares=10 ** 2, _bond_expire=0):
    global treasury, share_tokens, expire_days, bond_queue, available_bonds, sum_issued_bonds
    del (
        treasury,
        share_tokens,
        expire_days,
        bond_queue,
        available_bonds,
        sum_issued_bonds,
    )
    treasury = _treasury
    share_tokens = _shares
    expire_days = convert_time(days=_bond_expire)
    bond_queue = []
    available_bonds = 0
    sum_issued_bonds = 0
