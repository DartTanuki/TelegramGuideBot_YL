import aiogram.utils.exceptions
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.keybords import user_keybords
from .user_states import RouteMR, OneCity

from bot.utils.gpt_api import ask
from bot.utils.geocoder_api import get_city_cords
from bot.utils.wiki_translate import get_pictures

from create_bot import bot
from .constants_text import about_bot, create_route_message, bot_commands


# @dp.message_handler(state=OneCity.city)
async def adding_city(message: types.Message, state: FSMContext):
    if message.text == 'cancel':
        await state.finish()
        await main_menu_loader(message)
        return

    await state.update_data(city=message.text)
    await message.answer('Запрос выполняется❗️ Требуется подождать какое-то время.')
    photo = get_pictures(message.text)

    try:
        await bot.send_photo(chat_id=message.chat.id,
                            photo=photo,
                            caption=ask(f'Расскажи немного о городе {message.text}'),
                            reply_markup=user_keybords.one_city_keybord)

    except aiogram.utils.exceptions.InvalidHTTPUrlContent:
        await message.answer(ask(f'Расскажи немного о городе {message.text}'),
                             reply_markup=user_keybords.one_city_keybord)
    await OneCity.next()


# @dp.callback_query_handler(lambda query: query.data == 'attractions', state=OneCity.next_state)
async def next_state_state(callback: types.CallbackQuery, state: FSMContext):
    data_states = await state.get_data()
    await callback.message.answer('<b>ДОСТОПРИМЕЧАТЕЛЬНОСТИ</b>:\n' +
                                  ask(f'Выведи список достопримечательностей города {data_states["city"]}'),
                                  parse_mode='HTML')


# @dp.callback_query_handler(lambda query: query.data == 'return_to_main', state=OneCity.next_state)
async def return_to_main_menu_query(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.message.chat.id)
    await main_menu_loader(callback.message)
    await callback.answer()


# @dp.callback_query_handler(lambda query: query.data == 'city_history', state=OneCity.next_state)
async def write_city_history(callback: types.CallbackQuery, state: FSMContext):
    data_states = await state.get_data()
    await callback.message.answer(f'<b>История города {data_states["city"]}</b>\n' +
                                  ask(f'Расскажи о истории города {data_states["city"]}'),
                                  parse_mode='HTML')
    await callback.answer()


# @dp.callback_query_handler(lambda query: query.data == 'show_on_maps', state=OneCity.next_state)
async def show_city_on_maps(callback: types.CallbackQuery, state: FSMContext):
    data_states = await state.get_data()
    city_cords = await get_city_cords(data_states["city"])
    await bot.send_location(chat_id=callback.message.chat.id, longitude=city_cords[0], latitude=city_cords[1])
    await callback.answer()


# Обработка нажатия 'one_city'
# @dp.callback_query_handler(lambda query: query.data == 'one_city')
async def one_city_query(callback: types.CallbackQuery):
    await callback.message.answer("""📝Введите интересующий вас город ниже: 
    ❌Для отмены действия введите слово 'cancel'.""")
    await OneCity.city.set()
    await callback.answer()


# @dp.callback_query_handler(lambda query: query.data == 'create_route')
async def create_route_query(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(create_route_message)
    await RouteMR.adding_cities.set()
    await state.update_data(cities=[])
    await callback.answer()


# @dp.message_handler(state=RouteMR.adding_cities)
async def add_city_to_the_plan(message: types.Message, state: FSMContext):
    if message.text == 'cancel':
        await state.finish()
        await main_menu_loader(message=message)
        return

    state_data = await state.get_data()
    await state.update_data(cities=state_data['cities'] + [message.text])
    state_data = await state.get_data()
    await message.answer(f'Город успешно добавлен✅\nТекущий список городов🌃: '
                         f'{" ➡️ ".join([city for city in state_data["cities"]])}\n'
                         f'Для продолжения введите следующий город ниже👇',
                         reply_markup=user_keybords.adding_cities_keybord)


# @dp.callback_query_handler(lambda query: query.data == 'adding_cities_end', state=RouteMR.adding_cities)
async def add_transport_to_the_plan(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    if len(state_data['cities']) >= 2:
        await callback.message.answer('Отлично, теперь выберите транспорт для путешествия!',
                                      reply_markup=user_keybords.adding_aim_keybord)
        await RouteMR.transport.set()
    else:
        await callback.message.answer('🔒Недостаточное количество городов для путешествия!')
    await callback.answer()


# @dp.callback_query_handler(lambda query: query.data in ['transport_car', 'transport_train', 'transport_airplane'],state=RouteMR.transport)
async def add_aim_to_the_plan(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'transport_car':
        await state.update_data(transport='машина')
    elif callback.data == 'transport_train':
        await state.update_data(transport='поезд')
    elif callback.data == 'transport_airplane':
        await state.update_data(transport='самолёт')

    await callback.message.answer('Выберите приоритет путешествия. Для пропуска нажмите соответствующую кнопку!',
                                  reply_markup=user_keybords.adding_priority_keybord)
    await RouteMR.aim.set()
    await callback.answer()


# @dp.callback_query_handler(lambda query: query.data in ['travelling_food', 'travelling_attractions', 'travelling_skip'],state=RouteMR.aim)
async def creating_route_query(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'travelling_skip':
        await state.update_data(aim='')
    else:
        await state.update_data(aim=callback.data)
    await callback.message.answer('🔑Отлично! Начинаем формировать результат по вашим предпочтениям!')

    # Формирование запроса к ChatGPT.
    state_data = await state.get_data()
    user_transport = state_data["transport"]
    user_aim = f'Приоритет путешествия - {state_data["aim"]}' if state_data["aim"] else ''
    await callback.answer()
    await callback.message.answer('<b>План путешествия по вашему запросу</b>✅' +
                                  ask(f'Составь подробный план путешествия, состоящий из городов '
                                      f'{", ".join(state_data["cities"])}. '
                                      f'Транспорт для путешествия - {user_transport}, {user_aim}. Не забудь написать'
                                      f'как добраться из одного города в другой, учитывая вышесказанный транспорт.'),
                                  reply_markup=user_keybords.return_to_main_menu, parse_mode='HTML')
    await RouteMR.do_route.set()


# @dp.callback_query_handler(lambda query: query.data == 'mr_to_main', state=RouteMR.do_route)
async def return_to_main_menu_from_route(callback: types.CallbackQuery, state: FSMContext):
    await main_menu_loader(callback.message)
    await state.finish()
    await callback.answer()

# COMMANDS FUNCTIONS


async def main_menu_loader(message: types.Message):
    await message.answer('<b>Стартуем✅</b>!\nВыберите одну из функций ниже!',
                         parse_mode='HTML',
                         reply_markup=user_keybords.start_keybord)


# Команда '/commands'
# @dp.message_handler(commands=['commands'])
async def commands_command(message: types.Message):
    await message.reply('\n'.join([f'<b>{key}</b>: {bot_commands[key]}' for key in bot_commands]), parse_mode='HTML')


# Команда '/about'
# @dp.message_handler(commands=['about'])
async def about_command(message: types.Message):
    await message.reply(text=about_bot)


# @dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await main_menu_loader(message)



def register_user_handlers_main(dp: Dispatcher) -> None:

    # Standart commands
    dp.register_message_handler(commands_command, commands=['commands'])
    dp.register_message_handler(about_command, commands=['about'])
    dp.register_message_handler(start_command, commands=['start'])

    # Standart Callback Handlers
    dp.register_callback_query_handler(create_route_query, lambda query: query.data == 'create_route')
    dp.register_callback_query_handler(one_city_query, lambda query: query.data == 'one_city')

    # One City States Handlers
    dp.register_message_handler(adding_city, state=OneCity.city)
    dp.register_callback_query_handler(next_state_state, lambda query: query.data == 'attractions',
                                       state=OneCity.next_state)
    dp.register_callback_query_handler(return_to_main_menu_query, lambda query: query.data == 'return_to_main',
                                       state=OneCity.next_state)
    dp.register_callback_query_handler(write_city_history, lambda query: query.data == 'city_history',
                                       state=OneCity.next_state)
    dp.register_callback_query_handler(show_city_on_maps, lambda query: query.data == 'show_on_maps',
                                       state=OneCity.next_state)

    # RouteMR States Handlers
    dp.register_message_handler(add_city_to_the_plan, state=RouteMR.adding_cities)
    dp.register_callback_query_handler(add_transport_to_the_plan, lambda query: query.data == 'adding_cities_end',
                                       state=RouteMR.adding_cities)
    dp.register_callback_query_handler(add_aim_to_the_plan, lambda query: query.data in
                                                     ['transport_car', 'transport_train', 'transport_airplane'],
                                       state=RouteMR.transport)
    dp.register_callback_query_handler(creating_route_query, lambda query: query.data in
                                                     ['travelling_food', 'travelling_attractions', 'travelling_skip'],
                                       state=RouteMR.aim)
    dp.register_callback_query_handler(return_to_main_menu_from_route,
                                       lambda query: query.data == 'mr_to_main', state=RouteMR.do_route)