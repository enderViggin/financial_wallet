from typing import TypedDict, Literal
from uuid import UUID


class IncomeData(TypedDict):
    """ Сущность "Доход" """

    id: UUID
    name: str
    date: str
    category: Literal['income']
    amount: int
    description: str

class ExpenseData(TypedDict):
    """ Сущность "Расход" """

    id: UUID
    name: str
    date: str
    category: Literal['expense']
    amount: int
    description: str
