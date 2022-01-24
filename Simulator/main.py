from utils.sys_time import update_time
import protocol.main_protocol as protocol
import protocol.agent_handler as agent_creator
import random
import plotter
from tqdm import tqdm
ROUNDS = 5

# we make agents of different types here
# create agents from agent_handler
agents = []
num = 200
num2 = 2 * num
for i in range(num):
    agents.append(agent_creator.create_ideal_trader(usd=1000, basis=15000 / num2, share=100 / num))
    # agents.append(agent_creator.create_ideal_trader2(usd=1000, basis=10000 / num2, share=100 / num2))
    agents.append(agent_creator.create_random_agent(usd=200, basis=200))
    agents.append(agent_creator.create_bond_lover(usd=10, basis=10000 / num2))
    # agents.append(agent_creator.create_bond_lover(usd=100000))
    # agents.append(agent_creator.create_naive_trader(usd=100, basis=10000 / num2, share=100 / num2))
    # agents.append(agent_creator.create_hungry_trader(usd=100, basis=10000 / num2, share=100 / num2))
# TODO

for _round in tqdm(range(ROUNDS)):
    print(_round)
    for hour in range(24):
        random.shuffle(agents)
        # running actions of agents here
        for agent in agents:
            agent.action()
        protocol.action()

        if hour == 23:
            # end of the day
            # run protocol actions here
            protocol.main_action()

        update_time()

plotter.plot_basis_price()
