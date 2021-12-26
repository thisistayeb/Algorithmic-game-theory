from utils.random_generator import generate_bond_address


class Bond:
    def __init__(self, owner_id, create_date):
        self.owner_id = owner_id
        self.create_date = create_date
        self.id = generate_bond_address()
