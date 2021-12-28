from assets.bond import Bond
from oracles.oracle import get_token_price
from utils.sys_time import current_date, convert_time
from agents_database import wallets, address_to_wallet

treasury = 10 ** 10
sharetokens = 10 ** 2
bond_queue = []
available_bonds = 0
bond_expire = convert_time(years=5)


def create_bond():  # calculate available bonds for sell to agents
    global available_bonds
    if get_token_price[0] < 0.9:  # first element of "get price tuple" is basis
        amount = (1 - get_token_price[0]) * treasury
        available_bonds += amount


def issue_bond(wallet, amount, price_per_one):  # create bond and add it to wallet
    global treasury
    if amount > available_bonds:
        raise "Currently, there are not enough bonds available"
    new_bond = Bond(owner_id=wallet.address, create_date=current_date(), amount=amount)
    bond_queue.append(new_bond)
    wallet.add_bond(new_bond)
    treasury -= amount * price_per_one
    available_bonds -= amount


def pay_share_token_holder(amount):  # pay extra basis token to all share holders
    each_token = amount / sharetokens
    for wallet in wallets:
        wallet.add_basis(wallet.sharetokens * each_token)


def create_tokens():
    if get_token_price[0] > 1.1:  # first element of "get price tuple" is basis
        amount = (get_token_price[0] - 1) * treasury
        treasury += amount
        amount = redeem_bonds(amount)
        pay_share_token_holder(amount)


def redeem_certain_bond(bond, amount):  # redeem a certain bond
    bond.amount -= amount
    address_to_wallet[bond.owner_id].add_basis(amount)


def redeem_bonds(can_redeem):  # redeem bonds from bond_queue
    while len(bond_queue) > 0 and can_redeem > 0:
        while len(bond_queue) > 0 and bond_queue[0].amount == 0:
            bond_queue.pop(0)
        amount = min(bond_queue[0].amount, can_redeem)
        redeem_certain_bond(bond_queue[0], amount)
        can_redeem -= amount
    return can_redeem


def prone_bond_queue():  # remove expired bonds and redeem some of them
    today = current_date()
    while len(bond_queue) > 0 and bond_queue[0].create_date >= today + bond_expire:
        bond_queue.pop(0)

    redeem_bonds()


def get_price():  # get a tuple which contains token prices (basis, shares, bond)
    # use get_token_price function in oracles.oracle for get the prices
    pass
