import wikipedia
from translate import Translator
import random

# ---------------------------- WIKIPEDIA + TRANSLATOR CONFIG-------------------------------

#  Настройка результата API Wikipedia
wikipedia_lang = 'en'
wikipedia.set_lang(wikipedia_lang)

translator = Translator(from_lang='ru', to_lang='en')  # Создаем объект класса переводчика

#  Получение изображений по выбранному городу
def get_pictures(city: str) -> list:
    translated_city = translator.translate(city)
    need_name = wikipedia.search(translated_city)

    try:
        page = wikipedia.page(need_name[0])
    except wikipedia.exceptions.DisambiguationError:
        page = wikipedia.page(f'{need_name[0]} city')

    if len(translated_city.split(' ')) > 1:
        translated_city = '_'.join(translated_city.split(' '))

    return random.choice([photo for photo in page.images if translated_city.lower().rstrip() in photo.lower()
            and photo.split('.')[-1] in ['png', 'jpg']])
