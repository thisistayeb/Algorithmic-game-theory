import plotter
import numpy as np

ls = [0.23140392509837612, 0.42805255211388976, 6460852351872717.0,
0.2315888422436427, 0.44316035888836647, 274891757587.505,
1.3701797765599244, 0.5590321534219879, 6078.42781632651,
79.79519561681253, 23.918647241123118, 2447301.3777309866,
972.316621427303, 1363.7774233859734, 3.585698679748604e+18,
0.20826317652050685, 0.432283668572919, 2.5684294167369496e+16,
0.21412458721087066, 0.43742578011872707, 152899277717503.25,
698.6925003279862, 1617.1505842900922, 1839.483379031085,
1.4750122626426188, 0.5615234638551684, 10056.356610541767,
1034.9517675705074, 824.7916371569638, 1.1030367672977308e+21,
0.21890901739284283, 0.43425937667069314, 2566111841862401.5,
1051.0949239980064, 1331.4338855015824, 4714592349648.256,
569.9344333103293, 257.18533814131575, 8299000.3389541665,
1.3771894405876655, 0.5544022227371955, 549257.2562990021,
1.3987450062513893, 0.5461329775013716, 10711.675009587743,
0.19124481519057182, 0.43250165559027726, 13876668980381.617,
0.2131311623029778, 0.4340255497022694, 11702464395568.5,
1.3509572141668857, 0.5549880091469235, 653969531.5344545,
1.4085143148583432, 0.5437211674090332, 858309.2569099535,
1005.7100233570002, 1318.8914200700412, 4.7450555010623523e+30]

basis_std = ls[::3]
basis_mean = ls[1::3]
bond_mean = ls[2::3]

basis_std = np.minimum(basis_std, 2)
basis_mean = np.minimum(basis_mean, 1.5)

dates = [10, 25, 50, 100]
periods = [1, 2, 6, 12, 24]

plotter.plot_heatmap(
    np.asarray(basis_std).reshape(len(periods), len(dates)),
    periods,
    dates,
    "res1.png",
    "std of basis price",
)
plotter.plot_heatmap(
    np.asarray(basis_mean).reshape(len(periods), len(dates)),
    periods,
    dates,
    "res2.png",
    "mean of basis price",
)
plotter.plot_heatmap(
    np.asarray(bond_mean).reshape(len(periods), len(dates)),
    periods,
    dates,
    "res3.png",
    "mean of bond price",
)
