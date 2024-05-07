from typing import NoReturn

from .utils import (
    NUMBER_OF_POSSIBLE_INITIAL_ACTIONS,
    UtilsFinancialWallet,
)
from .db_utils import DBUtils
from .viewing_fw_utils import MenuForViewingIncomeExpenseFinancialWallet
from .adding_fw_utils import AddingIncomeExpensesFinancialWallet


class FinancialWallet(UtilsFinancialWallet):
    """ Класс отвечающий за взаимодействие пользователя с финансовым кошельком """

    def start(self) -> NoReturn:
        """ Начинаем принимать ввод от пользователя и реагировать на него """

        while True: # Принимаем ввод от пользователя бесконечно
            current_balance: int = DBUtils().get_current_balance()
            self.show_welcome_message(current_balance)

            user_response: int = self.get_user_response(
                message='ВЫБЕРИТЕ необходимое действие (введите номер):',
                type_of_response='int',
                possible_answers=list(range(NUMBER_OF_POSSIBLE_INITIAL_ACTIONS)),
                add_additional_actions=False
            )

            match user_response:
                case 0:
                    MenuForViewingIncomeExpenseFinancialWallet().start()
                case 1:
                    AddingIncomeExpensesFinancialWallet().start()
