from agents import bond_lover, hungry_trader, naive_trader, random_agent, ideal_agent
import protocol.agents_database as agents_database
from wallet.wallet import Wallet


def create_bond_lover(basis=0, share=0, usd=0):
    wallet = Wallet(basis=basis, share=share, usd=usd)
    agents_database.add_wallet(wallet)
    return bond_lover.BondLover(wallet)


def create_hungry_trader(basis=0, share=0, usd=0):
    wallet = Wallet(basis=basis, share=share, usd=usd)
    agents_database.add_wallet(wallet)
    return hungry_trader.HungryTraderAgent(wallet)


def create_naive_trader(basis=0, share=0, usd=0):
    wallet = Wallet(basis=basis, share=share, usd=usd)
    agents_database.add_wallet(wallet)
    return naive_trader.NaiveTraderAgent(wallet)


def create_ideal_trader(basis=0, share=0, usd=0):
    wallet = Wallet(basis=basis, share=share, usd=usd)
    agents_database.add_wallet(wallet)
    return ideal_agent.IdealAgent(wallet)


def create_random_agent(basis=0, share=0, usd=0):
    wallet = Wallet(basis=basis, share=share, usd=usd)
    agents_database.add_wallet(wallet)
    return random_agent.RandomAgent(wallet)


def create_hodler_agent(basis=0, share=0, usd=0):
    wallet = Wallet(basis=basis, share=share, usd=usd)
    agents_database.add_wallet(wallet)
    return random_agent.Hodler(wallet)
