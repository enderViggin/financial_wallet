from typing import Union, List, Tuple, Literal
import uuid
from uuid import UUID
from datetime import datetime

from .utils import (
    IncomeData,
    ExpenseData,
    UtilsFinancialWallet,
)
from .db_utils import DBUtils



class AddingIncomeExpensesFinancialWallet(UtilsFinancialWallet):
    """ Класс связанный с добавлением доходов/расходов """

    def __init__(self):
        self.possible_actions: Tuple[str, str] = ('Доходы', 'Расходы')
        self.number_of_possible_actions: int = len(self.possible_actions)


    def get_following_action_user(self) -> str:
        """ Получаем следующее действие пользователя """

        designation_back: str = 'b';
        designation_exit: str = 'e';
        possible_answers: List[Union[str, int]] = list(map(
            str,
            list(range(self.number_of_possible_actions))
        ))
        for designation in [designation_back, designation_exit]:
            possible_answers.append(designation)

        user_response: str = self.get_user_response(
            message='ВЫБЕРИТЕ что делать дальше (введите номер или действие):',
            possible_answers=possible_answers,
        )
        return user_response


    def get_information_about_income_expense(self, category: str) ->  Union[IncomeData, ExpenseData]:
        """ Получаем информацию о доходе/расходе для последующего добавления """

        def get_name() -> str:
            """ Получаем название """

            user_response: str = self.get_user_response(
                message='1/3 ВВЕДИТЕ название:',
            )
            match user_response:
                case 'b':
                    AddingIncomeExpensesFinancialWallet().start()
                case 'e':
                    exit()
                case _:
                    return user_response

        def get_amount() -> int:
            """ Получаем сумму продукта """

            user_response: Union[int, Literal['b', 'e']] = self.get_user_response(
                message='2/3 ВВЕДИТЕ соответствующую сумму:',
            )
            match user_response:
                case 'b':
                    AddingIncomeExpensesFinancialWallet().start()
                case 'e':
                    exit()
                case _:
                    return user_response


        def get_description() -> str:
            """ Получаем описание """

            user_response: str = self.get_user_response(
                    message='3/3 ВВЕДИТЕ необходимое описание:',
            )
            match user_response:
                case 'b':
                    AddingIncomeExpensesFinancialWallet().start()
                case 'e':
                    exit()
                case _:
                    return user_response


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        if not category in ['income', 'expense']:
            raise ValueError(f'Передана неверная категория - {category}')

        new_id: UUID = str(uuid.uuid4())
        name: str = get_name()
        amount: int = get_amount()
        description: str = get_description()
        date_of_addition: datetime = datetime.now().strftime('%H:%M:%S %d-%m-%Y')

        result: Union[IncomeData, ExpenseData] = {
            'id': new_id,
            'name': name,
            'date': date_of_addition,
            'category': category,
            'amount': amount,
            'description': description
        }
        return result


    def add_income(self) -> None:
        """ Добавляем доход указанный пользователем """

        information_about_income: IncomeData = self.get_information_about_income_expense('income')
        DBUtils().add_new_income(information_about_income)


    def add_expense(self) -> None:
        """ Добавляем расход указанный пользователем """

        information_about_expense: ExpenseData = self.get_information_about_income_expense('expense')
        DBUtils().add_new_expense(information_about_expense)


    def start(self) -> None:
        self.show_menu_for_adding_income_expenses(self.possible_actions)
        user_response: str = self.get_following_action_user()

        match user_response:
            case 'b':
                return
            case 'e':
                exit()
            case '0':
                self.add_income()
                self.show_message_of_successfully_added_income_expense('income')
            case '1':
                self.add_expense()
                self.show_message_of_successfully_added_income_expense('expense')

        AddingIncomeExpensesFinancialWallet().start()
