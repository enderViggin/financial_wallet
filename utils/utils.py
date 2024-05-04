from typing import TypedDict, Literal
from datetime import datetime


class IncomeData(TypedDict):
    """ Сущность "Доход" """

    date: datetime
    category: Literal['income', 'expense']
    amount: int
    description: str
