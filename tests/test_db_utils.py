import os
import sys
import re
from typing import KeysView, List

import pytest
from unittest.mock import MagicMock

from ..utils.db_utils import DBUtils



def test_get_path_to_db() -> None:
    path_to_db: str = DBUtils().get_path_to_db()
    assert re.findall( '.+?/db.json$', path_to_db)[0]


def test_get_db() -> None:
    db: Dict = DBUtils().get_db()
    keys: KeysView = db.keys()
    assert 'income' in keys and 'expenses' in keys


@pytest.mark.parametrize('some_list, number_of_parts, expected_result',
                         [
                              ([1, 2, 3, 4, 5], 2, [[1, 2,], [3, 4], [5]]),
                              ([1, 2, 3, 4, 5, 6, 7], 3, [[1, 2, 3], [4, 5, 6], [7]]),
                         ])
def test_split_list_into_parts(some_list: List, number_of_parts: int, expected_result: List[List]) -> None:
    splitted_list: Tuple = DBUtils().split_list_into_parts(some_list, number_of_parts)
    assert  splitted_list.final_list == expected_result


def test_get_current_balance() -> None:
    current_balance: int = DBUtils().get_current_balance()
    assert type(current_balance) == int
