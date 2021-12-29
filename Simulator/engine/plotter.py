import matplotlib.pyplot as plt
from oracles import token_stat


def plot_basis_price():
    history = token_stat.basis_price_history
    plt.plot(history)
    plt.show()
