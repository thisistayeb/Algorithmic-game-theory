from utils.sys_time import update_time
import protocol.protocol as protocol
import protocol.agent_handler as agent_creator
import random


ROUNDS = 50

# we make agents of different types here
# create agents from agent_handler
agents = []
for i in range(25):
    agents.append(agent_creator.create_random_agent())
    agents.append(agent_creator.create_bond_lover())
    agents.append(agent_creator.create_naive_trader())
    agents.append(agent_creator.create_hungry_trader())
# TODO

for _round in range(ROUNDS):
    for hour in range(24):
        random.shuffle(agents)
        # running actions of agents here
        for agent in agents:
            agent.action()
        protocol.action()
        update_time()

    # end of the day
    # run protocol actions here
    protocol.main_action()

