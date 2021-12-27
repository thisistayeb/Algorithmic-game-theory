from utils.sys_time import update_time
import protocol.protocol as protocol
ROUNDS = 50

# we make agents of different types here
# create agents from agent_handler
agents = []
# TODO

for _round in range(ROUNDS):
    for hour in range(24):
        # running actions of agents here
        for agent in agents:
            agent.action()
        update_time()

    # end of the day
    # run protocol actions here
    protocol.action()

