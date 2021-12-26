from assets.bond import Bond
from utils.random_generator import current_date
from oracles.oracle import get_token_price


class Treasury:
    def __init__(self):
        self.treasury = 10 << 10
        self.bond_queue = []
        self.expire_days = 365 * 5

    def create_bond(self, wallet, paid_value):
        new_bond = Bond(owner_id=wallet.address, create_date=current_date())
        self.bond_queue.append(new_bond)
        wallet.add_bond(new_bond)
        self.treasury -= paid_value
        # TODO

    def redeem_bond(self, bond):  # redeem a certain bond
        pass

    def prone_bond_queue(self):  # remove expired bonds and redeem some of them
        pass

    def can_redeem_bond(self):  # check if we can redeem a bond or not
        pass

    def get_price(self):  # get a tuple which contains token prices (basis, shares, bond)
        # use get_token_price function in oracles.oracle for get the prices
        pass

