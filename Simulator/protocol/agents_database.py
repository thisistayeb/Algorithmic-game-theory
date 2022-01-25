from wallet.wallet import Wallet

wallets = []
address_to_wallet = dict()


def add_wallet(wallet: Wallet):
    if wallet in wallets:
        raise "Wallet is added before!"
    address_to_wallet[wallet.address] = wallet
    wallets.append(wallet)


def launcher():
    global wallets, address_to_wallet
    del wallets, address_to_wallet
    wallets = []
    address_to_wallet = dict()
