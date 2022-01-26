import numpy as np

import history_eraser
import main
import plotter


def launch(_maximum_date=10, p_treasury=10 ** 5, p_shares=100, _rounds=20, _update_period=24):
    history_eraser.clean(_maximum_date, p_treasury, p_shares)
    return main.start(rounds=_rounds, update_period=_update_period)


basis_std = []
basis_mean = []
bond_mean = []

# launch(_rounds=30)
# exit(0)

for max_date in [10, 50, 100]:
    for _period in [1, 2, 6, 12, 24]:
        print(max_date, _period)
        mean1 = 0
        mean2 = 0
        mean3 = 0
        turns = 3
        for i in range(turns):
            basis_s, basis_m, bond_m = launch(_maximum_date=max_date, _update_period=_period, _rounds=100)
            mean1 += basis_s
            mean2 += basis_m
            mean3 += bond_m
        basis_std.append(mean1 / turns)
        basis_mean.append(mean2 / turns)
        bond_mean.append(mean3 / turns)

print(basis_std)
print(basis_mean)
print(bond_mean)

plotter.plot_heatmap(np.asarray(basis_std).reshape(5, 3),
                     [1, 2, 6, 12, 24],
                     [10, 50, 100], "res1.png", "std of basis price")
plotter.plot_heatmap(np.asarray(basis_mean).reshape(5, 3),
                     [1, 2, 6, 12, 24],
                     [10, 50, 100], "res2.png", "mean of basis price")
plotter.plot_heatmap(np.asarray(bond_mean).reshape(5, 3),
                     [1, 2, 6, 12, 24],
                     [10, 50, 100], "res3.png", "mean of bond price")
