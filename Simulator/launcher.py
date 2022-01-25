import history_eraser
import main


def launch(_maximum_date=10, p_treasury=10 ** 5, p_shares=100, _rounds=20):
    history_eraser.clean(_maximum_date, p_treasury, p_shares)
    main.start(rounds=_rounds, update_period=24)


launch()
