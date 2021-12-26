from agents.agent import Agent
from protocol import agents_database
from wallet.wallet import Wallet


def create_new_agent():
    wallet = Wallet()
    agents_database.add_wallet(wallet)
    return Agent(wallet)
