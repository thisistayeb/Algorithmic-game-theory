import oracles.exchange as exchange
import oracles.oracle as oracle
import oracles.token_stat as token_stat
import protocol.agents_database as agents_database
import protocol.treasury as main_treasury
import utils.sys_time as sys_time


def clean(_maximum_date=10, p_treasury=10 ** 5, p_shares=100):
    exchange.launcher()
    oracle.launcher(_maximum_date=10)
    token_stat.launcher()
    agents_database.launcher()
    main_treasury.launcher(
        _treasury=p_treasury, _shares=p_shares, _bond_expire=_maximum_date
    )
    sys_time.launcher()
