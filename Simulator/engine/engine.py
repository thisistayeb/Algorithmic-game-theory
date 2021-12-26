from utils.sys_time import update_time
ROUNDS = 50

# we make agents of different types here
# create agents from agent_handler

for _round in range(ROUNDS):
    for hour in range(24):
        # running actions of agents here

        update_time()

    # end of the day
    # run protocol actions here

