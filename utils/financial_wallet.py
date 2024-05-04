from typing import NoReturn, Union, Optional, List, Tuple


POSSIBLE_INITIAL_ACTIONS: Tuple[str, str, str] = ('Посмотреть расходы/доходы', 'Добавить расходы/доходы', 'Изменить расходы/доходы')
NUMBER_OF_POSSIBLE_INITIAL_ACTIONS: int = len(POSSIBLE_INITIAL_ACTIONS)

class UtilsFinancialWallet:
    """ Класс отвечающий за инструменты связанные с FinancialWallet """

    def get_user_response(
        self,
        message: str,
        type_of_response: Optional[str] = None,
        possible_answers: Optional[List] = None,
        optional: Optional[bool] = None
    ) -> Union[str, int]:
        """ Получаем ответ от пользователя """

        while True:
            try:
                response: str = input(f' ## {message}\n >> ')
                if not response and not optional: continue

                if type_of_response == 'int':
                    response: int = int(response)

                if not possible_answers: return response
                if response in possible_answers: return response
                else: print('\n Неправильный ответ.\n')
            except UnicodeDecodeError:
                print('\n Не используйте специальные символы в своих ответах.\n')
            except ValueError:
                print('\n Неправильный ответ.\n')


class MessageToDisplayFinancialWallet:
    """ Класс отвечающий за отображение сообщений для пользователя """

    def show_welcome_message(self) -> None:
        """ Показываем приветственное сообщение пользователю """

        text: str = "\n ### Добро пожаловать в FinancialWallet ###\n # Здесь вы можете отслеживать свои доходы и расходы.\n"""
        print(text)
        self.show_options_for_initial_actions()


    def show_options_for_initial_actions(self) -> None:
        """ Показываем варианты начальных действий """

        text: str = ''
        for count, action in enumerate(POSSIBLE_INITIAL_ACTIONS):
            text += f' [{count:02d}] {action}\n'

        print(text)


class FinancialWallet(UtilsFinancialWallet, MessageToDisplayFinancialWallet):
    """ Класс отвечающий за взаимодействие пользователя с финансовым кошельком """

    def get_initial_action_selected_by_user(self) -> str:
        """ Получаем выбранное пользователем начальное действие """
        pass


    def start(self) -> None:
        """ Начинаем принимать ввод от пользователя и реагировать на него """

        self.show_welcome_message()
        self.get_user_response(
            message='Что будем делать дальше?',
            type_of_response='int',
            possible_answers=list(range(NUMBER_OF_POSSIBLE_INITIAL_ACTIONS))
        )
