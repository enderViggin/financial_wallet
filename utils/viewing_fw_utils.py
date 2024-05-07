from typing import Union, List, Tuple

from .utils import (
    IncomeData,
    ExpenseData,
    UtilsFinancialWallet,
)
from .editing_fw_utils import EditingIncomeExpensesFinancialWallet
from .finding_fw_utils import FindingIncomeExpensesFinancialWallet
from .db_utils import DBUtils



class DisplayListOfEntriesFinancialWallet(UtilsFinancialWallet):
    """ Отображаем конкретный список записей (доходов/расходов) для пользователя """

    def execute_following_action_user(
        self,
        category: str,
        split_list_of_entries: Tuple[List[List[Union[IncomeData, ExpenseData]]], int],
        part_of_entries: int
    ) -> str:
        """ Получаем следующее действие пользователя """

        def get_users_choice() -> str:
            
            nonlocal split_list_of_entries
            designation_find: str = 'f';
            designation_edit: str = 'e';
            designation_back: str = 'b';
            designation_exit: str = 'e';
            designations: List[str] = [
                designation_find,
                designation_edit,
                designation_back,
                designation_exit,
            ]
            possible_answers: List[Union[str, int]] = list(map(
                str,
                list(range(1, split_list_of_entries.total_number_of_parts + 1))
            ))
            _ = [possible_answers.append(designation) for designation in designations]

            return self.get_user_response(
                message='ВЫБЕРИТЕ что делать дальше (номер страницы или действие):',
                possible_answers=possible_answers,
                add_additional_actions='[f]ind [e]dit'
            )


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        users_choice: str = get_users_choice()

        match users_choice:
            case 'f':
                FindingIncomeExpensesFinancialWallet().start(category)
                DisplayListOfEntriesFinancialWallet().display_list_of_income_expense(
                    category=category,
                    part_of_entries=1
                )
            case 'e':
                EditingIncomeExpensesFinancialWallet().start(split_list_of_entries, part_of_entries)
                DisplayListOfEntriesFinancialWallet().display_list_of_income_expense(
                    category=category,
                    part_of_entries=1
                )
            case 'b':
                MenuForViewingIncomeExpenseFinancialWallet().start()
            case 'e':
                exit()
            case _:
                DisplayListOfEntriesFinancialWallet().display_list_of_income_expense(
                    category=category,
                    part_of_entries=int(users_choice)
                )


    def display_list_of_all_entries(
        self,
        split_list_of_entries: Union[List[IncomeData], List[ExpenseData]],
        part_of_entries: int
    ) -> None:
        """ Отображаем список всех записей """

        final_list: List[Union[IncomeData, ExpenseData]] = split_list_of_entries \
            .final_list[part_of_entries - 1]

        for count, entry in enumerate(final_list, 1):
            self.display_separate_entry(count, entry)

        pagination: str = '\n ВЫБРАНО: '
        for part in range(1, split_list_of_entries.total_number_of_parts + 1):
            if part == part_of_entries:
                pagination += f'[{part}] '
            else:
                pagination += f'{part} '

        print(pagination)


    def display_list_of_income_expense(
        self,
        category: str,
        part_of_entries: int = 1
    ) -> None:
        """ Отображаем список доходов/расходов """

        def get_split_list_of_entries() -> Tuple[List[List[IncomeData]], int]:
            """ Получаем разделенный список записей """
            
            if category == 'income':
                return DBUtils().get_list_of_all_income_expense(
                    category=category,
                    type_of_entries='splitted'
                )
            elif category == 'expense':
                return DBUtils().get_list_of_all_income_expense(
                    category=category,
                    type_of_entries='splitted'
                )
            else:
                raise ValueError(f'Передана неверная категория - {category}')


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        split_list_of_entries: Tuple[List[List[IncomeData]], int] = get_split_list_of_entries()
        self.show_initial_message_for_list_of_income_expenses(category)
        self.display_list_of_all_entries(split_list_of_entries, part_of_entries)
        self.execute_following_action_user(
            category,
            split_list_of_entries,
            part_of_entries
        )


class MenuForViewingIncomeExpenseFinancialWallet(UtilsFinancialWallet):
    """ Класс связанный с меню просмотра доходов/расходов """

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
            message='ВЫБЕРИТЕ что делать дальше (введите номер):',
            possible_answers=possible_answers,
        )
        return user_response


    def start(self) -> None:
        self.show_menu_for_viewing_income_expenses(self.possible_actions)
        user_response: str = self.get_following_action_user()

        match user_response:
            case 'b':
                return
            case 'e':
                exit()
            case '0':
                DisplayListOfEntriesFinancialWallet().display_list_of_income_expense('income')
            case '1':
                DisplayListOfEntriesFinancialWallet().display_list_of_income_expense('expense')

