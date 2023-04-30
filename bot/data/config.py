# # Токен бота
# # TOKEN_API = '6054834704:AAGNkwsgQtHs7paKKr-icNGfZxWDbjtbxNA'
# #
# # TOKEN_CHATGPT_API = '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'
# #
# # GEOCODER_TOKEN_API = '40d1649f-0493-4b70-98ba-98533de7710b'


import os

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

GPT_TOKEN = str(os.getenv('GPT_TOKEN'))

GEOCODER_TOKEN = str(os.getenv('GEOCODER_TOKEN'))
