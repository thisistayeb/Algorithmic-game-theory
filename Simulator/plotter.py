import matplotlib.pyplot as plt
import numpy as np

from oracles import token_stat


def analysis():
    period = 24
    basis_history = np.asarray(token_stat.basis_price_history)
    bond_history = np.asarray(token_stat.bond_price_history)
    basis_history = basis_history[2:].reshape(
        basis_history[2:].shape[0] // period, period
    )
    basis_history = np.mean(basis_history, axis=1)

    bond_history = bond_history[2:].reshape(bond_history[2:].shape[0] // period, period)
    bond_history = np.mean(bond_history, axis=1)

    return np.std(basis_history), np.mean(basis_history), np.mean(bond_history)


def plot_basis_price():
    period = 1
    basis_history = np.asarray(token_stat.basis_price_history)
    bond_history = np.asarray(token_stat.bond_price_history)
    basis_history = basis_history[2:].reshape(
        basis_history[2:].shape[0] // period, period
    )
    basis_history = np.mean(basis_history, axis=1)

    bond_history = bond_history[2:].reshape(bond_history[2:].shape[0] // period, period)
    bond_history = np.mean(bond_history, axis=1)
    # history = np.minimum(history, 5)
    # plt.plot(np.minimum(bond_history, 3))
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(basis_history, label="dollar per basis")
    axs[0].plot(np.minimum(1, np.maximum(1, basis_history)))
    axs[1].plot(bond_history, label="basis per bond")
    axs[1].plot(np.minimum(1, np.maximum(1, bond_history)))
    axs[0].legend()
    axs[1].legend()
    plt.show()


def plot_heatmap(table, rows, cols, filename, title):
    fig, axs = plt.subplots(1)
    im = axs.imshow(table)
    cbar = axs.figure.colorbar(im, ax=axs)
    axs.set_yticks(np.arange(len(rows)))
    axs.set_xticks(np.arange(len(cols)))
    axs.set_yticklabels(rows)
    axs.set_xticklabels(cols)
    plt.setp(axs.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    # for i in range(len(rows)):
    #     for j in range(len(cols)):
    #         axs.text(j, i, table[i, j], ha="center", va="center", color="w")
    axs.set_title(title)
    fig.tight_layout()
    plt.savefig(filename)
