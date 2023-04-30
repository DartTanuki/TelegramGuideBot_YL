import openai
from bot.data.config import GPT_TOKEN

# -----------------------CHATGPT CONFIG-------------------------------------
# Ключ доступа
openai.api_key = GPT_TOKEN

# Настройка запроса
ENGINE = 'text-davinci-003'
max_tokens = 3800
temperature = 0.5


# Генерация запроса к ChatGPT.
def ask(user_prompt):
    completion = openai.Completion.create(model=ENGINE,
                                          prompt=user_prompt,
                                          max_tokens=max_tokens,
                                          temperature=temperature)
    return completion["choices"][0].text