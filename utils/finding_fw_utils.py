from typing import Tuple, List, Union, Dict
import re

from .utils import (
    IncomeData,
    ExpenseData,
    UtilsFinancialWallet,
)
from .db_utils import DBUtils


class FindingIncomeExpensesFinancialWallet(UtilsFinancialWallet):
    """ Класс связанный с поиском доходов/расходов по определенным критериям """

    def __init__(self):
        self.possible_criteria: Tuple[str, str, str, str] = ('Название', 'Описание', 'Сумма', 'Дата')
        self.number_of_possible_criteria: int = len(self.possible_criteria)


    def foo(self) -> None:
        db: Dict = DBUtils().get_db()

        if category == 'income':
            list_of_entries: List[IncomeData] = db['income']
        elif category == 'expense':
            list_of_entries: List[ExpenseData] = db['expenses']
        else:
            raise ValueError(f'Передана неверная категория - {edited_entry["category"]}')


    def get_value_of_selected_criterion(self, criteria: str) -> str:
        """ Получаем значение для выбранной критерии """

        def get_value_for_name() -> str:
            """ Получаем значение для имени """
            
            nonlocal criteria
            return self.get_user_response(
                message='1/1 ВВЕДИТЕ подстроку названия:',
            )

        def get_value_for_description() -> str:
            """ Получаем значение для описания """
            
            nonlocal criteria
            return self.get_user_response(
                message='1/1 ВВЕДИТЕ подстроку описания:',
            )

        def get_value_for_amount() -> str:
            """ Получаем значение для суммы """
            
            nonlocal criteria
            while True:
                value: str = self.get_user_response(
                    message='1/1 ВВЕДИТЕ сумму или диапазон (например, 350 или 2700-41500):',
                )
                first_option: List = re.findall('\d+', value)
                second_option: List = re.findall('\d+?-\d+', value)
                if second_option: return (2, second_option[0])
                if first_option: return (1, first_option[0])

        def get_value_for_date() -> str:
            """ Получаем значение для даты """
            
            nonlocal criteria
            while True:
                value: str = self.get_user_response(
                    message='1/1 ВВЕДИТЕ необходимую дату (формат: 21-03-2024):',
                )
                first_option: List = re.findall('\d{2,}-\d{2,}-\d{2,}', value)
                if first_option: return (1, first_option[0])


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        if criteria == 'Название':
            value: str = get_value_for_name()
            return value
        elif criteria == 'Описание':
            value: str = get_value_for_description()
            return value
        elif criteria == 'Сумма':
            value: str = get_value_for_amount()
            return value
        elif criteria == 'Дата':
            value: str = get_value_for_date()
            return value
        else:
            raise ValueError(f'criteria - {criteria}')


    def display_found_entries(self, entries_by_selected_criterion) -> None:
        """ Отображаем найденные записи """
        
        def get_total_amount() -> int:
            """ Получаем общую сумму найденных записей """

            total_amount: int = 0
            for entry in entries_by_selected_criterion:
                try:
                    amount: int = int(re.findall('\d+', entry['amount'])[0])
                    total_amount += amount
                except Exception:
                    continue

            return total_amount


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        total_amount: int = get_total_amount()
        text: str = f'\n ----- РЕЗУЛЬТАТЫ ПОИСКА НИЖЕ\n ----- Общая сумма: {total_amount} руб.'
        print(text)
        for count, entry in enumerate(entries_by_selected_criterion, 1):
            self.display_separate_entry(int(count), entry)

        input(' - НАЖМИТЕ Enter чтобы продолжить\n')


    def search_for_entries_by_to_selected_criterion(
        self,
        category: str,
        criteria_number: str
    ) -> None:
        """ Поиск записей по указанному критерию """

        def get_entries_by_selected_criterion() -> None:
            """ Получаем записи по указанной критерии """

            nonlocal category, criteria, value_of_selected_criterion
            return DBUtils().get_entries_by_selected_criterion(
                category,
                criteria,
                value_of_selected_criterion
            )


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        criteria: str = self.possible_criteria[int(criteria_number)]
        value_of_selected_criterion: str = self.get_value_of_selected_criterion(
            criteria
        )
        entries_by_selected_criterion = get_entries_by_selected_criterion()
        self.display_found_entries(entries_by_selected_criterion)


    def start(self, category: str) -> None:
        
        def get_users_choice() -> str:

            designation_back: str = 'b';
            designation_exit: str = 'e';
            designations: List[str] = [
                designation_back,
                designation_exit,
            ]
            possible_answers: List[Union[str, int]] = list(map(
                str,
                list(range(self.number_of_possible_criteria))
            ))
            _ = [possible_answers.append(designation) for designation in designations]

            return self.get_user_response(
                message='ВЫБЕРИТЕ критерий поиска (введите число или действие):',
                possible_answers=possible_answers,
            )

        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        self.show_entry_search_menu(category, self.possible_criteria)
        users_choice: str = get_users_choice()

        match users_choice:
            case 'b':
                return
            case 'e':
                exit()
            case _:
                self.search_for_entries_by_to_selected_criterion(category, users_choice)
