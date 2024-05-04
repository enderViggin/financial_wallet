from typing import TypedDict, Literal
from datetime import datetime


class IncomeData(TypedDict):
    """ Сущность "Доход" """

    date: str
    category: Literal['income']
    amount: int
    description: str

class ExpenseData(TypedDict):
    """ Сущность "Расход" """

    date: str
    category: Literal['expense']
    amount: int
    description: str
