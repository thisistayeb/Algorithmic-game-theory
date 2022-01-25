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
    a = 5000
    c = 10000
    d = 0
    for i in range(a):
        agents.append(
            agent_creator.create_ideal_trader(usd=0.3 * t_basis / a, basis=0.3 * t_basis / a, share=0.3 * 100 / a))
    for i in range(c):
        agents.append(
            agent_creator.create_random_agent(usd=0.7 * t_basis / c, basis=0.7 * t_basis / c, share=0.7 * 100 / c))
    for i in range(d):
        agents.append(agent_creator.create_bond_lover(usd=1000, basis=0.1 * t_basis / d))
        # agents.append(agent_creator.create_naive_trader(usd=100, basis=10000 / num2, share=100 / num2))
        # agents.append(agent_creator.create_hungry_trader(usd=100, basis=10000 / num2, share=100 / num2))

    for _round in range(rounds):
        print(_round)
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

    plotter.plot_basis_price()
