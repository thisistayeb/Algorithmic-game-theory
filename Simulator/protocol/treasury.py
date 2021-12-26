from assets.bond import Bond
from oracles.oracle import get_token_price
from utils.sys_time import current_date, convert_time
from agents_database import wallets, address_to_wallet

treasury = 10 ** 10
sharetokens = 10 ** 2
bond_queue = []
available_bonds = 0
prior_bonds = 0
expire_days = convert_time(years=5)


def create_bond():
    global available_bonds
    if get_token_price[0] < 0.9:  # first element of "get price tuple" is basis
        amount = (1 / get_token_price[0]) ** treasury
        available_bonds += amount


def issue_bond(wallet, amount, price_per_one):
    global treasury, prior_bonds
    if amount > available_bonds:
        raise "Currently, there are not enough bonds available"
    new_bond = Bond(owner_id=wallet.address, create_date=current_date(), amount=amount)
    bond_queue.append(new_bond)
    wallet.add_bond(new_bond)
    treasury -= amount * price_per_one
    available_bonds -= amount
    prior_bonds += amount


def pay_share_token_holder(amount):
    pass


def redeem_bond_amount():  # calculate how much bonds we can buy from agents
    pass


def create_tokens():
    if get_token_price[0] > 1.1:  # first element of "get price tuple" is basis
        amount = get_token_price[0] ** treasury
        if prior_bonds != 0:
            for item in bond_queue:
                if amount - item.amount > 0:
                    amount -= item.amount
                    prior_bonds -= item.amount
                    address_to_wallet[item.owner_id].add_basis(amount)
                    # TODO: add amount to owner of bond

        if amount > 0:
            eache_token = amount / sharetokens
            for wallet in wallets:
                wallet.basis += wallet.sharetokens * eache_token


def redeem_certain_bond(bond, amount):  # redeem a certain bond
    bond.amount -= amount


def redeem_bonds():  # redeem a certain bond
    can_redeem = redeem_bond_amount()
    while len(bond_queue) > 0 and can_redeem > 0:
        while len(bond_queue) > 0 and bond_queue[0].amount == 0:
            bond_queue.pop(0)
        amount = min(bond_queue[0].amount, can_redeem)
        redeem_certain_bond(bond_queue[0], amount)
        can_redeem -= amount


def prone_bond_queue():  # remove expired bonds and redeem some of them
    today = current_date()
    while len(bond_queue) > 0 and bond_queue[0].create_date >= today + expire_days:
        bond_queue.pop(0)

    redeem_bonds()


def get_price():  # get a tuple which contains token prices (basis, shares, bond)
    # use get_token_price function in oracles.oracle for get the prices
    pass
