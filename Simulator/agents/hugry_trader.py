from agent import Agent
from wallet.wallet import Wallet

class HungryTraderAgent(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        """
        If Basis price is higher than $1.5, this trader sells all his Basis tokens
        If Basis price is less than $0.5, this trader will change all his USDs to Basis tokens
        """
        prices = get_token_price()  # (basis, share, bond)
        if price[0] == 0 :
            pass
        elif prices[0] > 1.5:
            self.sell_basis(self.wallet.basis)
        elif price[0] < 0.5:
            self.buy_basis(self.wallet.usd)