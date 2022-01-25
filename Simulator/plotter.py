import matplotlib.pyplot as plt
import numpy as np

from oracles import token_stat


def plot_basis_price():
    period = 24
    basis_history = np.asarray(token_stat.basis_price_history)
    bond_history = np.asarray(token_stat.bond_price_history)
    basis_history = basis_history[2:].reshape(basis_history[2:].shape[0] // period, period)
    basis_history = np.sum(basis_history, axis=1)
    basis_history /= period

    bond_history = bond_history[2:].reshape(bond_history[2:].shape[0] // period, period)
    bond_history = np.sum(bond_history, axis=1)
    bond_history /= period
    # history = np.minimum(history, 5)
    # plt.plot(np.minimum(bond_history, 3))
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(np.minimum(10, basis_history), label='basis per dollar')
    axs[0].plot(np.minimum(1, np.maximum(1, basis_history)))
    axs[1].plot(np.minimum(10, bond_history), label='bond per dollar')
    axs[1].plot(np.minimum(1, np.maximum(1, bond_history)))
    axs[0].legend()
    axs[1].legend()
    plt.show()
