from typing import List, Dict, Optional
import json
import os
import uuid

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


    def sort_list_of_income_by_date(self, list_of_all_income: List[IncomeData]) -> List[IncomeData]:
        """ Сортируем список доходов по дате """

        list_of_income_by_date: List[IncomeData] = sorted(
            list_of_all_income,
            key=lambda income: income['date']
        )
        return list_of_income_by_date


    def get_list_of_all_income(self, sort: Optional[str] = None) -> List:
        """ Получаем список всех доходов """

        db: Dict = self.get_db()
        list_of_all_income: List[IncomeData] = db['income']

        match sort:
            case 'date':
                sorted_list_of_income_by_date: List[IncomeData] = self.sort_list_of_income_by_date(
                    list_of_all_income
                )
                return sorted_list_of_income_by_date
            case _:
                return list_of_all_income


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
