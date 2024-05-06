from typing import TypedDict, Literal, Tuple, Optional, List, Union
from uuid import UUID


POSSIBLE_INITIAL_ACTIONS: Tuple[str, str, str] = ('Посмотреть доходы/расходы', 'Добавить доходы/расходы', 'Изменить доходы/расходы')
NUMBER_OF_POSSIBLE_INITIAL_ACTIONS: int = len(POSSIBLE_INITIAL_ACTIONS)

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


class MessageToDisplayFinancialWallet:
    """ Класс отвечающий за отображение сообщений для пользователя """

    def show_welcome_message(self, current_balance: int) -> None:
        """ Показываем приветственное сообщение пользователю """

        text: str = f'\n ----- ДОБРО ПОЖАЛОВАТЬ В FinancialWallet\n ----- Здесь вы можете отслеживать свои доходы и расходы.\n ----- БАЛАНС: {current_balance} руб.\n'
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

        text: str = '\n\n ----- МЕНЮ ПРОСМОТРА ДОХОДЫ/РАСХОДЫ\n ----- Выберите дальнейшее действие\n\n'

        for count, action in enumerate(possible_actions):
            text += f' [{count:02d}] {action}\n'

        print(text)


    def show_menu_for_adding_income_expenses(self, possible_actions: Tuple[str, str]) -> None:
        """ Показываем меню добавления доходов/расходов """

        text: str = '\n\n ### МЕНЮ ДОБАВЛЕНИЯ ДОХОДОВ/РАСХОДОВ ###\n ### Выберите дальнейшее действие\n\n'

        for count, action in enumerate(possible_actions):
            text += f' [{count:02d}] {action}\n'

        print(text)


    def show_menu_for_editing_income_expenses(self, possible_actions: Tuple[str, str]) -> None:
        """ Показываем меню изменения доходов/расходов """

        text: str = '\n\n --- МЕНЮ ИЗМЕНЕНИЯ ДОХОДОВ/РАСХОДОВ \n --- Выберите дальнейшее действие\n\n'

        for count, action in enumerate(possible_actions):
            text += f' [{count:02d}] {action}\n'

        print(text)


    def show_message_of_successfully_added_income_expense(self, category: str) -> None:
        """ Показываем сообщение об успешно добавленном доходе/расходе """

        if category == 'income':
            message: str = 'УСПЕШНО добавлен указанный доход'
        elif category == 'expense':
            message: str = 'УСПЕШНО добавлен указанный расход'
        else:
            raise ValueError(f'Передана неверная категория - {category}')

        print(f'\n [*] {message}')


    def show_initial_message_for_list_of_income_expenses(self, category: str) -> None:
        """ Показываем начальное сообщение для списка доходов """

        if category == 'income':
            message: str = '\n\n ----- СПИСОК ДОБАВЛЕННЫХ ДОХОДОВ\n ----- Выберите дальнейшее действие'
        elif category == 'expense':
            message: str = '\n\n ----- СПИСОК ДОБАВЛЕННЫХ РАСХОДОВ\n ----- Выберите дальнейшее действие'
        else:
            raise ValueError(f'Передана неверная категория - {category}')
        print(message)


    def show_entry_search_menu(
        self,
        category: str,
        possible_criteria: Tuple[str, str, str, str]
    ) -> None:
        """ Показываем меню поиска записей """

        if category == 'income':
            text: str = '\n\n --- МЕНЮ ПОИСКА ЗАПИСЕЙ ДОХОДОВ\n --- Выберите дальнейшее действие\n\n'
        elif category == 'expense':
            text: str = '\n\n --- МЕНЮ ПОИСКА ЗАПИСЕЙ РАСХОДОВ\n --- Выберите дальнейшее действие\n\n'
        else:
            raise ValueError(f'Передана неверная категория - {category}')

        for count, criteria in enumerate(possible_criteria):
            text += f' [{count:02d}] {criteria}\n'

        print(text)



class UtilsFinancialWallet(MessageToDisplayFinancialWallet):
    """ Класс отвечающий за инструменты связанные с FinancialWallet """

    def get_user_response(
        self,
        message: str,
        type_of_response: Optional[str] = None,
        possible_answers: Optional[List] = None,
        optional: Optional[bool] = None,
        add_additional_actions: Optional[Union[bool, str]] = True
    ) -> Union[str, int]:
        """ Получаем ответ от пользователя """

        def get_text_of_message() -> str:
            """ Получаем текст для сообщения """
            
            if not add_additional_actions:
                text_of_message: str = f' - {message}\n > '
                return text_of_message

            text_of_message: str = f'\n - '
            if type(add_additional_actions) == str:
                text_of_message += f'{add_additional_actions} '
            text_of_message += f'[b]ack [e]xit\n - {message}\n > '

            return text_of_message


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        text_of_message: str = get_text_of_message()

        while True:
            try:
                response: str = input(text_of_message)
                if not response and not optional: continue

                if type_of_response == 'int':
                    response: int = int(response)

                if not possible_answers: return response
                if response in possible_answers: return response
                else: print('\n [*] НЕВЕРНО, выберите вариант из указанных.\n')
            except UnicodeDecodeError:
                print('\n Не используйте специальные символы в своих ответах.\n')
            except ValueError:
                print('\n [*] НЕВЕРНО, выберите вариант из указанных.\n')


    def display_separate_entry(
        self,
        count: int,
        entry: Union[IncomeData, ExpenseData]
    ) -> None:
        """ Отображаем отдельную запись """

        text: str = '\n'
        text += f' #{count} {entry["date"]} \n'
        text += f' | {entry["name"]} \n'
        text += f' | {entry["amount"]} \n'
        text += f' | {entry["description"]} \n'
        print(text)
