from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from random import shuffle
from functions import *

TOKEN = '6738768458:AAEl0eYCeWBbpOSPe3b8dHBRkhGiUamDTVQ'  # Токен для идентификации бота

bot = Bot(token=TOKEN)  # Создаем экземпляр бота
dp = Dispatcher(bot, storage=MemoryStorage())  # Создаем экземпляр диспетчера

"""Обработка команды /start"""
@dp.message_handler(text=['/start'])
async def StartFunction(message: types.Message):
    users[message.from_user.id] = ['', 0, ['', '']] # Анаграммы, Число для скрабла, города

    await message.answer(
        f'👋 Привет, {(message.from_user.first_name).upper()}!\n\nЭто <b>GameBot🤖</b>\n\n'
        f'<b>Я умею:</b>\n\n<i>1) Играть в скрабл🔢\n\n'
        f'2) Играть в анаграммы🎭\n\n'
        f'3) Играть в города🏙️</i>\n\n<b>'
        f'<i>Во что поиграем?</i></b>',
        parse_mode=ParseMode.HTML, reply_markup=markup)

"""Обработка команды /help"""
@dp.message_handler(text=['/help'])
async def StartFunction(message: types.Message):
    await message.answer(
        '<b>-----Правила игры----</b>\n\n'

        '<b>Анаграммы:</b>\n\n'
        '<i>1. Цель игры: Составить как можно больше слов из букв заданного слова. \n'
        '2. Правила:\n'
        '    Используются только буквы исходного слова.\n'
        '     Каждая буква может быть использована только один раз в каждом новом слове.\n'
        '     Слова должны быть существительными в именительном падеже единственного числа (если не оговорено иное).\n'
        '     Побеждает игрок, составивший больше всего слов.</i>\n\n'

        '<b>Скрабл:</b>\n\n'
        '<i>1. Цель игры: Набрать больше очков, чем соперник, составляя слова на предоставленную тему.\n'
        '2. Правила:\n'
        '    Игроку предоставлена тема: "Фрукты на английском языке".\n'
        '     Он должен писать названия знакомых его фруктов на английском языке.</i>\n\n'

        '<b>Города:</b>\n\n'

        '<i>1. Цель игры: Назвать город, название которого начинается с последней буквы предыдущего города.\n'
        '2. Правила:\n'
        '    Игра начинается с любого города.\n'
        '     Следующий игрок должен назвать город, название которого начинается с последней буквы предыдущего города.\n'
        '     Города не могут повторяться.\n'
        '     Если игрок не может назвать город, он выбывает.\n'
        '     Побеждает последний оставшийся игрок.</i>\n', parse_mode=ParseMode.HTML, reply_markup=markup)

"""Обработка коллбэков и вызов функций при нажатии на кнопки"""
@dp.callback_query_handler()
async def CheckMessage(message: types.CallbackQuery):
    callback = message.data
    await bot.delete_message(message.from_user.id, message.message.message_id)

    if callback == 'City':
        await bot.send_message(message.from_user.id,
           f"Добро пожаловать в игру:\n Города России\n"
           f"\nНачинайте первым... 💬✍")
        await Form.Cities.set()

    if callback == 'Anagramms':
        users[message.from_user.id][0] = ''

        await message.answer("Подожди немного, я придумываю слово! 🤖")
        await message.answer("⏳")

        word = choice(words)
        users[message.from_user.id][0] += word

        await bot.send_message(message.from_user.id,
           f"Всё, я Загадал слово ✍ \n\n"
           f"Посморишь ответ, когда сдашься 🫡 "
           f"\n<tg-spoiler>🫵👁\n{word}</tg-spoiler>",
           parse_mode=ParseMode.HTML)

        word_shuffled = list(word)
        shuffle(word_shuffled)
        shuffled_word = ''.join(word_shuffled)

        await bot.send_message(message.from_user.id,
           f"Вот Анаграмма: "
           f"\n\n\t{shuffled_word}\n\n"
           f"Угадай слово, которое я загадал 🤖"
           f"\n\nУдачи! 👀✊")

        await Form.Anagramms.set()

    if callback == 'Scrable':
        await bot.send_message(message.from_user.id,
            f"Добро пожаловать в игру Скрабл! 🔠\n\n"
            f"<b>Тема:</b> Фрукты на анг. яз 👨‍🍳\n"
            f"\n<i>Начнем ...</i> \n\nНапишите слово ✍️",
            parse_mode=ParseMode.HTML)
        await Form.Scrable.set()

"""Вызов анаграммы"""
@dp.message_handler(state=Form.Anagramms)
async def adc_function(message: types.Message, state: FSMContext):
    msg = message.text

    if msg.lower() == 'стоп':
        gif = open('GIF/Otmena.mp4', 'rb')
        await message.reply_animation(animation=gif, caption=
        f"Можете выбирать другую игру 🤖\n"
        f"\n1)  /help   -   Помощь 👨‍🏫\n",
        reply_markup=markup)

        await state.finish()

    if msg.lower() == users[message.from_user.id][0].lower(): # Сюда сохраняется слово, выведенное программой
        await message.answer("Верно! Угадал! 😄🎖")
        await message.answer("✅")

        users[message.from_user.id][0] = ''  # Перемешивание букв в слове
        word = choice(words)
        users[message.from_user.id][0] += word

        await message.answer(
            f"Всё, я Загадал слово ✍ \n\n"
            f"Посморишь ответ, когда сдашься 🫡 "
            f"\n<tg-spoiler>🫵👁\n{word}</tg-spoiler>",
            parse_mode=ParseMode.HTML
        )

        word_shuffled = list(word)
        shuffle(word_shuffled)
        shuffled_word = ''.join(word_shuffled)

        await message.answer(
            f"Вот Анаграмма: "
            f"\n\n\t{shuffled_word}\n\n"
            f"Угадай слово, которое я загадал 🤖"
            f"\n\nУдачи! 👀✊"
            f"\nНапишите   ==  ⭕️<b><u><code>Стоп</code></u></b>⭕️  ==   чтобы Выйти ",
            parse_mode = ParseMode.HTML
        )

    else:
        if msg.lower() != 'стоп':
            await message.answer(
                f"Неверно, я такого не загадывал! 😡\n"
                f"\nНапишите   ==  ⭕️<b><u><code>Стоп</code></u></b>⭕️  ==   чтобы Выйти ",
                parse_mode=ParseMode.HTML
            )

"""этот декоратор для скрабла"""
@dp.message_handler(state=Form.Scrable)
async def adc_function(message: types.Message, state: FSMContext):
    msg = message.text

    if msg.lower() == 'стоп':
        gif = open('GIF/Otmena.mp4', 'rb')
        await message.reply_animation(animation=gif, caption=
        f"Можете выбирать другую игру 🤖\n"
        f"\n1)/help   -   Помощь 👨‍🏫\n",
        reply_markup=markup)

        await state.finish()

    for fruit in fruits:
        if msg.lower() == fruit.lower():
            users[message.from_user.id][1] += 3

            await message.answer(
                f"Хорошо! Слово принято\n"
                f"\n<b><i>Ваше кол-во очков::</i></b>  <code>{users[message.from_user.id][1]}</code>   👍",
                parse_mode=ParseMode.HTML
            )
            break
    else:
        if msg.lower() != 'стоп':
            await message.answer(
                f"Неверно, я такого фрукта не знаю! 😡\n"
                f"\nНапишите   ==  ⭕️<b><u><code>Стоп</code></u></b>⭕️  ==   чтобы Выйти ",
                parse_mode=ParseMode.HTML
            )

"""Этот декоратор нужен для городов"""
@dp.message_handler(state=Form.Cities)
async def adc_function(message: types.Message, state: FSMContext):
    msg = message.text

    if msg.lower() == 'стоп':
        gif = open('GIF/Otmena.mp4', 'rb')
        await message.reply_animation(animation=gif, caption=
        f"Можете выбирать другую игру 🤖\n"
        f"\n1)  /help   -   Помощь 👨‍🏫\n",
        reply_markup=markup)

        await state.finish()

    try:
        word = Get_City(msg=msg, user_id=message.from_user.id)
        if word == 'error':
            await message.answer(
                f"Неверно, город уже использовался! 😡\n"
                f"Напишите   ==  ⭕️<b><u><code>Стоп</code></u></b>⭕️  ==   чтобы Выйти ",
                parse_mode=ParseMode.HTML
            )
        else:
            await message.answer(word)
    except:
        await message.answer(
            f"Неверно, я такого города не знаю! 😡\n"
            f"\nНапишите   ==  ⭕️<b><u><code>Стоп</code></u></b>⭕️  ==   чтобы Выйти ",
            parse_mode=ParseMode.HTML
        )

if __name__ == '__main__':
    executor.start_polling(dp)

