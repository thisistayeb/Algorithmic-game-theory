from wallet.wallet import Wallet

wallets = []


def add_wallet(wallet: Wallet):
    if wallet in wallets:
        raise "Wallet is added before!"
    wallets.append(wallet)
