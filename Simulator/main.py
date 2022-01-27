import oracles.exchange
from utils.sys_time import update_time
import protocol.main_protocol as protocol
import protocol.agent_handler as agent_creator
import random
import time
from agents import (
    bond_lover,
    hungry_trader,
    naive_trader,
    random_agent,
    ideal_agent,
    hodler,
    rational_trader,
    ideal_agent2,
    ideal_agent3,
)
import plotter


# from tqdm import tqdm


def start(rounds=100, update_period=24, plot=False):
    # we make agents of different types here
    # create agents from agent_handler
    agents = []
    t_basis = protocol.treasury.treasury
    a = 500
    b = 500
    c = 500
    d = 500
    e = 500
    f = 500
    w1 = 0.1  # ideal
    w2 = 0.45  # ideal 2
    w3 = 0.25  # ideal 3
    w4 = 0.05  # random
    w5 = 0.1  # bond lover
    w6 = 0.05  # ma trader
    # for i in range(a):
    #     agents.append(
    #         agent_creator.create_trader_agent(usd=w1 * t_basis / a, basis=w1 * t_basis / a, share=w1 * 100 / a))
    for i in range(a):
        agents.append(agent_creator.create_ideal_trader(
            usd=w1 * t_basis / a,
            basis=w1 * t_basis / a,
            share=w1 * 100 / a,
            radii=random.uniform(0, 2)))
    for i in range(b):
        agents.append(agent_creator.create_ideal_trader2(
            usd=w2 * t_basis / b,
            basis=w2 * t_basis / b,
            share=w2 * 100 / b,
            radii=random.uniform(0, 5)))
    # for i in range(c):
    #     agents.append(agent_creator.create_rational_trader_agent(
    #         usd=w3 * t_basis / c,
    #         basis=w3 * t_basis / c,
    #         share=w3 * 100 / c))
    for i in range(c):
        agents.append(agent_creator.create_ideal_trader3(
            usd=w3 * t_basis / c,
            basis=w3 * t_basis / c,
            share=w3 * 100 / c,
            radii=random.uniform(0.1, 1)))
    for i in range(d):
        agents.append(agent_creator.create_random_agent(usd=w4 * t_basis / d,
                                                        basis=w4 * t_basis / d,
                                                        share=w4 * 100 / d))
    for i in range(e):
        agents.append(agent_creator.create_bond_lover(usd=w5 * t_basis / e,
                                                      basis=w5 * t_basis / e,
                                                      share=w5 * 100 / e))
    for i in range(f):
        agents.append(agent_creator.create_ma_trader(usd=w6 * t_basis / f,
                                                     basis=w6 * t_basis / f,
                                                     share=w6 * 100 / f))
    for _round in range(rounds):
        # print(protocol.treasury.treasury)
        # print(_round)
        for hour in range(24):
            # print(oracles.exchange.basis_demand_trajectory[-1], oracles.exchange.basis_supply_trajectory[-1])
            random.shuffle(agents)
            # running actions of agents here
            for agent in agents:
                agent.action()
            # print(time.time() - start)
            # start = time.time()
            protocol.action()

            if (hour + 1) % update_period == 0:
                # end of the day
                # run protocol actions here
                protocol.main_action()

            update_time()

    b_std, b_mean, bond_mean = plotter.analysis()
    # print(b_std, b_mean, bond_mean)
    if plot:
        plotter.plot_basis_price()
    return b_std, b_mean, bond_mean
