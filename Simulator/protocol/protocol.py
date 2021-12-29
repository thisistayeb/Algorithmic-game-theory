# in this file, we do actions of protocol in each time step. (daily action)
import oracles.oracle as oracle
import treasury
import oracles.exchange as exchange


def action():  # some simple actions are here. TODO
    exchange.handle_transactions()
    exchange.payback_transactions()
    token_price = oracle.get_token_price()  # (basis, shares, bond)
    if token_price[0] > 1.1:
        treasury.create_tokens()
    elif token_price[0] < 0.9:
        treasury.create_bond()
        # TODO
        pass
    else:  # the basis price is between 0.9$ and 1.1$
        pass
    pass
