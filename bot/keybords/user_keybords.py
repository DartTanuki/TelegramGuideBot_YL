from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_keybord = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Город', callback_data='one_city'),
     InlineKeyboardButton('Составить план путешествия!', callback_data='create_route')]
])

one_city_keybord = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Достопримечательности', callback_data='attractions'),
     InlineKeyboardButton('История города', callback_data='city_history'),
     InlineKeyboardButton('Показать на карте', callback_data='show_on_maps')],
    [InlineKeyboardButton('Вернуться в главное меню', callback_data='return_to_main')]
])

adding_cities_keybord = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Далее', callback_data='adding_cities_end')]
])

adding_aim_keybord = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Машина🚘', callback_data='transport_car'),
     InlineKeyboardButton('Поезд🚆', callback_data='transport_train'),
     InlineKeyboardButton('Самолет✈️', callback_data='transport_airplane')]
])

adding_priority_keybord = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Достопримечательности🌆', callback_data='travelling_attractions'),
     InlineKeyboardButton('Еда🍘', callback_data='travelling_food')],
    [InlineKeyboardButton('Пропустить', callback_data='travelling_skip')]
])

return_to_main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Вернуться в главное меню', callback_data='mr_to_main')]
])
