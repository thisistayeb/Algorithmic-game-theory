from utils.sys_time import update_time
import protocol.main_protocol as protocol
import protocol.agent_handler as agent_creator
import random
import plotter
# from tqdm import tqdm


def start(rounds=100, update_period=24):
    # we make agents of different types here
    # create agents from agent_handler
    agents = []
    t_basis = protocol.treasury.treasury
    a = 1000
    c = 9000
    d = 0
    w1 = 0.3
    w2 = 0.7
    for i in range(a):
        agents.append(
            agent_creator.create_ideal_trader(usd=w1 * t_basis / a, basis=w1 * t_basis / a, share=w1 * 100 / a,
                                              radii=random.choice([0, 0.2, 1, 4, 6, 10, 12])))
    for i in range(c):
        agents.append(
            agent_creator.create_random_agent(usd=w2 * t_basis / c, basis=w2 * t_basis / c, share=w2 * 100 / c))

    for _round in range(rounds):
        # print(_round)
        for hour in range(24):
            random.shuffle(agents)
            # running actions of agents here
            for agent in agents:
                agent.action()
            protocol.action()

            if (hour + 1) % update_period == 0:
                # end of the day
                # run protocol actions here
                protocol.main_action()

            update_time()

    b_std, b_mean, bond_mean = plotter.analysis()
    # plotter.plot_basis_price()
    return b_std, b_mean, bond_mean
