from typing import List, Dict, Optional, Union, Tuple
import json
import os
import uuid
from collections import namedtuple

from .utils import IncomeData, ExpenseData


class DBUtils:
    """ Инструменты связанные с БД """

    def get_path_to_db(self) -> str:
        """ Получаем путь к БД """

        path_to_db: str = os.path.abspath(
            os.path.join(os.path.dirname( __file__ ), '../db', 'db.json')
        )
        return path_to_db


    def get_db(self) -> Dict:
        """ Получаем базу данных пользователя """

        with open(self.get_path_to_db()) as file:
            file_content = file.read()
            database: Dict = json.loads(file_content)
            return database


    def save_db_changes(self,  db: Dict) -> None:
        """ Сохраняем проделанные изменения с БД """

        with open(self.get_path_to_db(), 'w') as file:
            json.dump(db, file)


    def split_list_into_parts(
        self,
        some_list: List,
        number_of_parts: int
    ) -> Tuple[List[List], int]:
        """ Разбиваем какой-то список на части """

        SplitList = namedtuple('SplitList', ['final_list', 'total_number_of_parts'])
        final_list: List[List] = []
        intermediate_list: List = []

        for count, item in enumerate(some_list, 1):
            intermediate_list.append(item)
            if count % number_of_parts == 0:
                final_list.append(intermediate_list)
                intermediate_list = []

        if intermediate_list: # Добавляем остатки
            final_list.append(intermediate_list)

        split_list = SplitList(
            final_list=final_list,
            total_number_of_parts=len(final_list)
        )
        return split_list


    def sort_list_of_entries_by_date(
        self,
        list_of_all_entries: Union[List[IncomeData], List[ExpenseData]]
    ) -> Union[List[IncomeData], List[ExpenseData]]:
        """ Сортируем список записей (доходов/расходов) по дате """

        list_of_entries_by_date: Union[List[IncomeData], List[ExpenseData]] = sorted(
            list_of_all_entries,
            key=lambda entry: entry['date'],
            reverse=True
        )
        return list_of_entries_by_date


    def get_list_of_all_income_expense(
        self,
        category: str,
        sort: Optional[str] = 'date',
        number_of_parts: int = 3,
        type_of_entries: str = 'all'
    ) -> Union[Union[List[IncomeData], List[ExpenseData]], Tuple[List[List], int]]:
        """ Получаем список всех доходов """

        def sort_list_of_entries() -> Union[List[IncomeData], List[ExpenseData]]:
            """ Сортируем список записей (доходов/расходов) """
            
            nonlocal sort

            if sort == 'date':
                return self.sort_list_of_entries_by_date(list_of_all_entries)
            else:
                return list_of_all_entries


        def get_required_type_of_entries() -> Union[Union[List[IncomeData], List[ExpenseData]], Tuple[List[List], int]]:
            """ Получаем необходимый вид записей """
            
            nonlocal type_of_entries, list_of_all_entries

            print('TOE', type_of_entries)
            if type_of_entries == 'all':
                return list_of_all_entries
            elif type_of_entries == 'splitted':
                print('YYYYYY')
                return self.split_list_into_parts(
                    list_of_all_entries,
                    number_of_parts
                )
            else:
                message: str = 'Должен быть передан один из двух аргументов: number_of_parts, all_entries'
                raise ValueError(message)


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        db: Dict = self.get_db()

        if category == 'income':
            list_of_all_entries: List[IncomeData] = db['income']
        elif category == 'expense':
            list_of_all_entries: List[IncomeData] = db['expenses']
        else:
            raise ValueError(f'Передана неверная категория - {category}')

        list_of_all_entries: Union[List[IncomeData], List[ExpenseData]] = sort_list_of_entries()

        final_list: Union[Union[List[IncomeData], List[ExpenseData]], Tuple[List[List], int]] = get_required_type_of_entries()
        return final_list


    def add_new_income(self, income: IncomeData) -> None:
        """ Добавляем новый доход в БД """

        db: Dict = self.get_db()
        db['income'].append(income)
        self.save_db_changes(db)


    def add_new_expense(self, expense: ExpenseData) -> None:
        """ Добавляем новый расход в БД """

        db: Dict = self.get_db()
        db['expenses'].append(expense)
        self.save_db_changes(db)
