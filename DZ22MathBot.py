import random
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = 'API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

correct_answers = 0
incorrect_answers = 0
max_incorrect_answers = 5 

def generate_task():
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operation = random.choice(['+', '-', '*', '/'])
    if operation == '+':
        result = num1 + num2
    elif operation == '-':
        result = num1 - num2
    elif operation == '*':
        result = num1 * num2
    elif operation == '/':
        result = num1 / num2
        result = round(result, 2)
    task_text = f"Выберай правильный ответ😊 {num1} {operation} {num2}?"
    return task_text, result

async def start_game(message):
    global correct_answers, incorrect_answers
    correct_answers = 0
    incorrect_answers = 0

    await message.answer("Эта математическая игра, если ты будешь отвечать не правильно, я позову твоего батю, и он тебя отпорет ремнем😈")

    while incorrect_answers < max_incorrect_answers:
        task_text, correct_result = generate_task()
        await message.answer(task_text)

        try:
            response = await bot.wait_for(types.Message, timeout=30)
            user_answer = response.text

            if user_answer.isdigit() or (user_answer.count('.') == 1 and user_answer.replace('.', '').isdigit()):
                user_answer = float(user_answer) if '.' in user_answer else int(user_answer)

                if user_answer == correct_result:
                    correct_answers += 1
                    await message.answer("А ты умный, молодец🙄")
                else:
                    incorrect_answers += 1
                    await message.answer(f"ХАХАХАХАХАХХ, ЛОХ😹, Правильный ответ: {correct_result}")
            else:
                await message.answer("Введи число уже наконец то!👺")

        except asyncio.TimeoutError:
            await message.answer("Не, мне надоело ждать, либо играешь, либо проваливаешь от сюда😾")
            break

    await message.answer(f"Ваше количество неправильных ответов{max_incorrect_answers},(1-2(Не плох)), (3(плох)), (4-5(ЛООООХХХ))")
    await message.answer(f"Твоя оценочка пупсик😽💋{correct_answers}<=Правильніе ответы, {incorrect_answers}<=Неправильные ответы👎🤮")
    await message.answer("Спасибо за игру), А ТЕПЕРЬ ВАЛИ ОТ СЮДА🤬")

if __name__ == '__main__':
    from aiogram import executor

    @dp.message_handler(commands=['start'])
    async def on_start(message: types.Message):
        await start_game(message)

    executor.start_polling(dp, skip_updates=True)