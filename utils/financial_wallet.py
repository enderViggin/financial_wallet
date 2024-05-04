from typing import NoReturn, Union, Optional, List, Tuple

from .utils import IncomeData
from .db_utils import DBUtils


POSSIBLE_INITIAL_ACTIONS: Tuple[str, str, str] = ('Посмотреть расходы/доходы', 'Добавить расходы/доходы', 'Изменить расходы/доходы')
NUMBER_OF_POSSIBLE_INITIAL_ACTIONS: int = len(POSSIBLE_INITIAL_ACTIONS)

class UtilsFinancialWallet:
    """ Класс отвечающий за инструменты связанные с FinancialWallet """

    def get_user_response(
        self,
        message: str,
        type_of_response: Optional[str] = None,
        possible_answers: Optional[List] = None,
        optional: Optional[bool] = None,
        add_additional_actions: Optional[bool] = None
    ) -> Union[str, int]:
        """ Получаем ответ от пользователя """

        if add_additional_actions:
            message: str = f'\n ## [b]ack [e]xit\n ## {message}\n >> '
        else:
            message: str = f' ## {message}\n >> '

        while True:
            try:
                response: str = input(message)
                if not response and not optional: continue

                if type_of_response == 'int':
                    response: int = int(response)

                if not possible_answers: return response
                if response in possible_answers: return response
                else: print('\n [*] Выберите вариант из указанных.\n')
            except UnicodeDecodeError:
                print('\n Не используйте специальные символы в своих ответах.\n')
            except ValueError:
                print('\n [*] Выберите вариант из указанных.\n')


class MessageToDisplayFinancialWallet:
    """ Класс отвечающий за отображение сообщений для пользователя """

    def show_welcome_message(self) -> None:
        """ Показываем приветственное сообщение пользователю """

        text: str = "\n ### ДОБРО ПОЖАЛОВАТЬ В FinancialWallet ###\n ## Здесь вы можете отслеживать свои доходы и расходы.\n"""
        print(text)
        self.show_options_for_initial_actions()


    def show_options_for_initial_actions(self) -> None:
        """ Показываем варианты начальных действий """

        text: str = ''
        for count, action in enumerate(POSSIBLE_INITIAL_ACTIONS):
            text += f' [{count:02d}] {action}\n'

        print(text)


    def show_menu_for_viewing_income_expenses(self, possible_actions: Tuple[str, str]) -> None:
        """ Показываем меню просмотра доходов/расходов """

        text: str = '\n\n ### МЕНЮ ДОХОДЫ/РАСХОДЫ ###\n ## Выберите дальнейшее действие\n\n'

        for count, action in enumerate(possible_actions):
            text += f' [{count:02d}] {action}\n'

        print(text)


class ViewingIncomeExpensesFinancialWallet(UtilsFinancialWallet, MessageToDisplayFinancialWallet):
    """ Класс связанный с просмотром доходов/расходов """

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
            message='Что теперь?',
            possible_answers=possible_answers,
            add_additional_actions=True
        )
        return user_response


    def start(self) -> None:

        self.show_menu_for_viewing_income_expenses(self.possible_actions)
        user_response: str = self.get_following_action_user()

        match user_response:
            case 'b':
                FinancialWallet().start()
            case 'e':
                exit()
            case '0':
                pass
            case '1':
                pass


class FinancialWallet(ViewingIncomeExpensesFinancialWallet):
    """ Класс отвечающий за взаимодействие пользователя с финансовым кошельком """

    def start(self) -> None:
        """ Начинаем принимать ввод от пользователя и реагировать на него """

        self.show_welcome_message()
        user_response: int = self.get_user_response(
            message='Итак, что делаем дальше?',
            type_of_response='int',
            possible_answers=list(range(NUMBER_OF_POSSIBLE_INITIAL_ACTIONS))
        )

        match user_response:
            case 0:
                ViewingIncomeExpensesFinancialWallet().start()
            case 1:
                pass
            case 2:
                pass
