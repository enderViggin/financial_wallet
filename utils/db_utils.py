from typing import List, Dict, Optional, Union, Tuple
import json
import os
from collections import namedtuple
import re

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


    def save_db_changes(self, db: Dict) -> None:
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

        split_list: SplitList = SplitList(
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


    def get_list_of_all_entries(
        self,
        category: str,
        sort: Optional[str] = 'date',
        number_of_parts: int = 5,
        type_of_entries: str = 'all'
    ) -> Union[Union[List[IncomeData], List[ExpenseData]], Tuple[List[List], int]]:
        """ Получаем список всех записей (доходов/расходов) """

        def get_list_of_all_entries() -> Union[List[IncomeData], List[ExpenseData]]:
            
            nonlocal category
            if category == 'income':
                list_of_all_entries: List[IncomeData] = db['income']
            elif category == 'expense':
                list_of_all_entries: List[IncomeData] = db['expenses']
            else:
                raise ValueError(f'Передана неверная категория - {category}')
            return list_of_all_entries



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

            if type_of_entries == 'all':
                return list_of_all_entries
            elif type_of_entries == 'splitted':
                return self.split_list_into_parts(
                    list_of_all_entries,
                    number_of_parts
                )
            else:
                message: str = 'Должен быть передан один из двух аргументов: number_of_parts, all_entries'
                raise ValueError(message)


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        db: Dict = self.get_db()
        list_of_all_entries: Union[List[IncomeData], List[ExpenseData]] = get_list_of_all_entries()
        list_of_all_entries: Union[List[IncomeData], List[ExpenseData]] = sort_list_of_entries()
        final_list: Union[Union[List[IncomeData], List[ExpenseData]], Tuple[List[List], int]] = get_required_type_of_entries()
        return final_list


    def add_new_entry(self, entry: Union[IncomeData, ExpenseData]) -> None:
        """ Добавляем запись в БД """

        db: Dict = self.get_db()

        if entry['category'] == 'income':
            db['income'].append(entry)
        elif entry['category'] == 'expense':
            db['expenses'].append(entry)

        self.save_db_changes(db)


    def save_edited_entry(self, edited_entry: Union[IncomeData, ExpenseData]) -> None:
        """ Сохраняем отредактированную запись """
        
        db: Dict = self.get_db()

        if edited_entry['category'] == 'income':
            list_of_entries: List[IncomeData] = db['income']
        elif edited_entry['category'] == 'expense':
            list_of_entries: List[ExpenseData] = db['expenses']
        else:
            raise ValueError(f'Передана неверная категория - {edited_entry["category"]}')

        for entry in list_of_entries:
            if entry['id'] == edited_entry['id']:
                list_of_entries.remove(entry)
                break

        list_of_entries.append(edited_entry)
        self.save_db_changes(db)


    def get_entries_by_selected_criterion(
        self,
        category: str,
        criteria: str,
        value: str
    ) -> None:
        """ Получаем записи по выбранному критерию """

        def add_entries_by_name_sorting() -> None:
            """ Добавляем записи по сортировке имени """
            
            nonlocal sorted_list, value, list_of_all_entries
            for entry in list_of_all_entries:
                if not value in entry['name']: continue
                entry['name'] = re.sub(value, f'[{value}]', entry['name'])
                sorted_list.append(entry)

        def add_entries_by_description_sorting() -> None:
            """ Добавляем записи по сортировке описания """
            
            nonlocal sorted_list, value, list_of_all_entries
            for entry in list_of_all_entries:
                if not value in entry['description']: continue
                entry['description'] = re.sub(
                    value,
                    f'[{value}]',
                    entry['description']
                )
                sorted_list.append(entry)


        def add_entries_by_amount_sorting_in_first_way() -> None:
            """ Добавляем записи по сортировке суммы первым способом """

            nonlocal sorted_list, value, list_of_all_entries

            for entry in list_of_all_entries:
                try:
                    entry_amount: str = re.findall('\d+', entry['amount'])[0]
                    if not value[1] == entry_amount : continue
                    sorted_list.append(entry)
                except Exception:
                    continue


        def add_entries_by_amount_sorting_in_second_way() -> None:
            """ Добавляем записи по сортировке суммы вторым способом """

            nonlocal sorted_list, value, list_of_all_entries

            for entry in list_of_all_entries:
                range: List[int] = list(map(int, value[1].split('-')))
                try:
                    amount_of_entry: int = int(
                        re.findall('\d+', entry['amount'])[0]
                    )
                except Exception:
                    continue

                if not range[0] <= amount_of_entry <= range[1]: continue
                sorted_list.append(entry)


        def add_entries_by_amount_sorting() -> None:
            """ Добавляем записи по сортировке суммы """
            
            nonlocal value

            if value[0] == 1:
                add_entries_by_amount_sorting_in_first_way()
            elif value[0] == 2:
                add_entries_by_amount_sorting_in_second_way()

        def add_entries_by_date_sorting() -> None:
            """ Добавляем записи по сортировке даты """
            
            nonlocal sorted_list, value, list_of_all_entries
            for entry in list_of_all_entries:
                if not value[1] in entry['date']: continue
                sorted_list.append(entry)


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        sorted_list: Union[List[IncomeData], List[ExpenseData]] = []
        list_of_all_entries = self.get_list_of_all_entries(category)

        if criteria == 'Название':
            add_entries_by_name_sorting()
        elif criteria == 'Описание':
            add_entries_by_description_sorting()
        elif criteria == 'Сумма':
            add_entries_by_amount_sorting()
        elif criteria == 'Дата':
            add_entries_by_date_sorting()

        return sorted_list


    def get_current_balance(self) -> int:
        """ Получаем текущий баланс """

        def add_all_income() -> None:
            """ Добавляем весь доход """

            nonlocal balance
            list_of_all_income: List[IncomeData] = self.get_list_of_all_entries(
                'income'
            )
            for income in list_of_all_income:
                try:
                    amount = int(re.findall('\d+', income['amount'])[0])
                    balance += amount
                except Exception:
                    continue

        def subtract_all_expense() -> None:
            """ Вычесть весь расход """

            nonlocal balance
            list_of_all_expense: List[IncomeData] = self.get_list_of_all_entries(
                'expense'
            )
            for income in list_of_all_expense:
                try:
                    amount = int(re.findall('\d+', income['amount'])[0])
                    balance -= amount
                except Exception:
                    continue


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        balance: int = 0
        add_all_income()
        subtract_all_expense()
        return balance
