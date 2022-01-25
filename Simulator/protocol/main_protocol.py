# in this file, we do actions of protocol in each time step. (daily action)
from oracles.oracle import get_token_price
import oracles.exchange as exchange
import protocol.treasury as treasury


def action():  # some simple actions are here.
    exchange.handle_transactions()
    exchange.payback_transactions()


def main_action():
    token_price = get_token_price()  # (basis, shares, bond)
    if token_price[0] > 1.1:
        treasury.create_tokens()
        treasury.create_bond()
    elif token_price[0] < 0.9:
        treasury.create_bond()
    else:  # the basis price is between 0.9$ and 1.1$
        pass
