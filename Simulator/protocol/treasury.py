from assets.bond import Bond
from utils.random_generator import current_date
from oracles.oracle import get_token_price


class Treasury:
    def __init__(self):
        self.treasury = 10 ** 10
        self.sharetokens = 10 ** 2
        self.bond_queue = []
        self.available_bonds = 0
        self.expire_days = 365 * 5
        

    def create_bond(self):
        if self.get_token_price[0] < 0.9 :   # first element of "get price tuple" is basis
            amount = (1/ self.get_token_price[0]) ** self.treasury
            self.available_bonds += amount


    def issue_bond(self, wallet, amount):
        if amount > self.available_bonds:
            raise "Currently, there are not enough bonds available"
        new_bond = Bond(owner_id=wallet.address, create_date=current_date())
        self.bond_queue.append(new_bond)
        wallet.add_bond(new_bond)
        self.treasury -= amount

    def pay_share_token_holder(self, amount):
        pass

        
    def create_tokens(self):
        if self.get_token_price[0] > 1.1: # first element of "get price tuple" is basis
            amount = self.get_token_price[0] ** self.treasury
            

    def redeem_bond(self, bond):  # redeem a certain bond
        pass

    def prone_bond_queue(self):  # remove expired bonds and redeem some of them
    """
    We could replace this function with "Binary search" a more efficient algorithm
    since bond queue is ascending by the time
    """
        for bond in range(len(bond_queue):
            if bond.create_date >= today + self.expire_days:
                bond_queue.remove(bond)
## Today need to define

    def get_price(self):  # get a tuple which contains token prices (basis, shares, bond)
        # use get_token_price function in oracles.oracle for get the prices
        pass

