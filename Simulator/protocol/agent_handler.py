from agents import bond_lover, hungry_trader, naive_trader, random_agent
from protocol import agents_database
from wallet.wallet import Wallet


def create_bond_lover():
    wallet = Wallet()
    agents_database.add_wallet(wallet)
    return bond_lover.BondLover(wallet)


def create_hungry_trader():
    wallet = Wallet()
    agents_database.add_wallet(wallet)
    return hungry_trader.HungryTraderAgent(wallet)


def create_naive_trader():
    wallet = Wallet()
    agents_database.add_wallet(wallet)
    return naive_trader.NaiveTraderAgent(wallet)


def create_random_agent():
    wallet = Wallet()
    agents_database.add_wallet(wallet)
    return random_agent.RandomAgent(wallet)
