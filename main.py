from typing import NoReturn
from utils import financial_wallet


def main() -> NoReturn:
    """ Точка входа """
    financial_wallet.FinancialWallet().start()


if __name__ == '__main__':
    main()
