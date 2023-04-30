from aiogram.dispatcher.filters.state import StatesGroup, State


class OneCity(StatesGroup):
    city = State()  # Стадия выбора города для просмотра информации
    next_state = State()  # Промежуточная стадия. Общая для всех доп.функций.


class RouteMR(StatesGroup):
    adding_cities = State()  # Стадия добавления городов
    aim = State()  # Стадия определения цели путешествия
    transport = State()  # Стадия выбора транспорта для совершения путешествия
    do_route = State()  # Стадия формирования окончательного запроса и получение ответа.