from typing import Tuple, List, Union
from collections import namedtuple

from .utils import (
    IncomeData,
    ExpenseData,
    UtilsFinancialWallet,
)
from .db_utils import DBUtils


class EditingIncomeExpensesFinancialWallet(UtilsFinancialWallet):
    """ Класс связанный с изменением доходов/расходов """

    def get_entry_to_edit(
        self,
        split_list_of_entries: Tuple[List[List[Union[IncomeData, ExpenseData]]]],
        part_of_entries: int,
        entry_number: int
    ) -> None:
        """ Получаем запись для редактирования """

        return split_list_of_entries.final_list[part_of_entries - 1][entry_number - 1]


    def get_new_entry_data(self) -> None:
        """ Получаем новые данные для записи """

        def get_new_name() -> str:
            response: str = self.get_user_response(
                message='1/3 ВВЕДИТЕ новое название для записи:',
                add_additional_actions='[s]kip'
            )

            if response == 'q':
                exit()
            else:
                return response


        def get_new_amount() -> str:
            response: str = self.get_user_response(
                message='2/3 ВВЕДИТЕ новую цену для записи:',
                add_additional_actions='[s]kip'
            )

            if response == 'q':
                exit()
            else:
                return response

        def get_new_description() -> str:
            response: str = self.get_user_response(
                message='3/3 ВВЕДИТЕ новое описание для записи:',
                add_additional_actions='[s]kip'
            )

            if response == 'q':
                exit()
            else:
                return response

        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        new_name = get_new_name()
        if new_name == 'b': return

        new_amount = get_new_amount()
        if new_amount == 'b': return

        new_description = get_new_description()
        if new_description == 'b': return

        NewData = namedtuple('NewData', ['name', 'amount', 'description'])
        new_data: NewData = NewData(
            name=new_name,
            amount=new_amount,
            description=new_description
        )
        return new_data


    def edit_selected_entry(
        self,
        split_list_of_entries: Tuple[List[List[Union[IncomeData, ExpenseData]]]],
        part_of_entries: int,
        users_choice: str
    ) -> None:
        """ Редактируем выбранную запись пользователя """
        
        new_entry_data = self.get_new_entry_data()
        entry_to_edit: Union[IncomeData, ExpenseData] = self.get_entry_to_edit(
            split_list_of_entries,
            part_of_entries,
            int(users_choice)
        )
        if new_entry_data.name != 's':
            entry_to_edit['name'] = new_entry_data.name

        if new_entry_data.amount != 's':
            entry_to_edit['amount'] = new_entry_data.amount

        if new_entry_data.description != 's':
            entry_to_edit['description'] = new_entry_data.description
        DBUtils().save_edited_entry(entry_to_edit)


    def start(
        self,
        split_list_of_entries: Tuple[List[List[Union[IncomeData, ExpenseData]]]],
        part_of_entries: int
    ) -> None:

        def get_users_choice() -> str:

            nonlocal split_list_of_entries
            designation_back: str = 'b';
            designation_quit: str = 'q';
            designations: List[str] = [
                designation_back,
                designation_quit,
            ]
            possible_answers: List[Union[str, int]] = list(map(
                str,
                list(range(1, split_list_of_entries.total_number_of_parts + 1))
            ))
            _ = [possible_answers.append(designation) for designation in designations]

            return self.get_user_response(
                message='ВЫБЕРИТЕ номер записи для изменения (введите число или действие):',
                possible_answers=possible_answers,
            )


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        users_choice: str = get_users_choice()

        match users_choice:
            case 'b':
                return
            case 'q':
                exit()
            case _:
                self.edit_selected_entry(split_list_of_entries, part_of_entries, users_choice)
