
# Пишем Telegram бота на Python + Загружаем Telegram бота на сервер(хостинг)
# https://www.youtube.com/watch?v=x-VB3b4pKcU

# https://habr.com/ru/post/442800/
#
# bot.register_next_step_handler(message, get_name)
#

# @AlexSpravbot
from auth_data import TOKEN

import requests
from datetime import datetime
import os
import telebot

import random
import pandas


MAX_NUMBER = 10000
number = 0
count = 1
secure_number = int(random.uniform(0, MAX_NUMBER))

FILENAME  = 'results.xlsx'
FILENAME2 = 'results2.xlsx'

NAME_FLAG = False
global BOT

def telegram_bot(token):
    bot = telebot.TeleBot(token)


    @bot.message_handler(commands=["start"])
    def start_message(message):
        init_params()
        bot.send_message(message.chat.id, f"Привет угадай загаданное число от 0 до {MAX_NUMBER} за меньшее количество попыток!")
        print(f"Привет угадай загаданное число от 0 до {MAX_NUMBER} за меньшее количество попыток!")
        # bot.send_sticker(message.chat.id, 'CAADAgADcwgAAhhC7ggBnQGJ6b93ggI')
        bot.send_message(message.chat.id, "Ввведите число:")


    @bot.message_handler(content_types=["text"])
    def get_number(message):
        global number
        global count
        try:
            print(message.text)
            number = int(message.text)
            if number < 0 or number > MAX_NUMBER:
                raise ValueError("Error")
        except Exception as ex:
            # print(ex)
            bot.send_message(
                message.chat.id,
                f'Неверное число. Введите целое число от 0 до {MAX_NUMBER}'
            )
        else:
            bot.send_message(
                message.chat.id,
                f'Вы ввели: {number}'
            )
            res = check_number(number, secure_number)
            if res == 0:
                ResultOutput(message, secure_number, count)
            elif res < 0:
                bot.send_message(
                    message.chat.id,
                    f'Загаданное число меньше.\nКоличество попыток: {count}'
                )
            else:
                bot.send_message(
                    message.chat.id,
                    f'Загаданное число больше.\nКоличество попыток: {count}'
                )

            # bot.send_message(
            #     message.chat.id,
            #     f'Загаданное число: {secure_number}'
            # )
        count += 1

    def check_number(number, secure_number):
        if number < secure_number:
            return 1
        elif number == secure_number:
            return 0
        else:
            return -1

    def init_params():
        global number
        global count
        global secure_number
        number = 0
        count = 1
        secure_number = int(random.uniform(0, MAX_NUMBER))


    def ResultOutput(message, secure_number, count):
        # bot.send_sticker(message.chat.id, 'CAADAgADcwgAAhhC7ggBnQGJ6b93ggI')
        bot.send_message(
            message.chat.id,
            f'***** БИНГО !!! *****\nЗагаданное число: {secure_number}\nВы угадали!!!\nКоличество попыток: {count}'
        )
        bot.send_message(
            message.chat.id,
            'Таблица победителей (ТОП 10):\n' + get_table_string()
        )
        GetUserName(message)


    def GetUserName(message):
        bot.send_message(
            message.chat.id,
            'Введите ваше имя:'
        )
        bot.register_next_step_handler(message, user_name)
        print("I am here!")


    def user_name(message):
        name = message.text
        print('user_name')
        print(name)
        insert_name_in_table(name, count, FILENAME)
        bot.send_message(
            message.chat.id,
            f'Ваше имя: {name}\nВы записаны в таблицу результатов!\n'
        )
        bot.send_message(
            message.chat.id,
            'Таблица победителей (ТОП 10):\n' + get_table_string()
        )
        bot.send_message(
            message.chat.id,
            f'\nХотите попробовать еще разок?:'
        )
        bot.register_next_step_handler(message, run_again_question)


    def insert_name_in_table(name, count, filename=FILENAME):
        df = read_results_table_form_file(filename)
        series_obj = pandas.Series([name, count], index=df.columns)
        df = df.append(series_obj, ignore_index=True)
        df = df.sort_values(by=['ПОПЫТКИ'])
        write_results_table_to_file(filename, df.head(10))



    def run_again_question(message):
        if message.text.lower() in ('yes', 'y', 'д', 'да'):
            bot.register_next_step_handler(message, start_message)
        else:
            print('Exit')
            bot.send_message(
                message.chat.id,
                f'Давайте поболтаем!'
            )
            bot.register_next_step_handler(message, start_message)


    def read_results_table_form_file(filename):
        excel_data_df = pandas.read_excel(filename)
        return excel_data_df.head(10)


    def write_results_table_to_file(filename, df):
        df.to_excel(filename, index=False, header=True)


    def get_table_string(filename=FILENAME):
        df = read_results_table_form_file(filename)
        df = df.sort_values(by=['ПОПЫТКИ'])
        products_list = df.values.tolist()
        new_string = ""
        for item in products_list:
            new_string += "{:>4}".format(str(item[1])) + '  ' + "{:<35}\n".format(item[0])
        print(new_string)
        return new_string


    bot.polling()

def insert(name, count, filename=FILENAME):
    df = read_results_table_form_file(filename)
    print(df)
    series_obj = pandas.Series([name, count], index=df.columns)
    df = df.append(series_obj,  ignore_index=True)
    df = df.sort_values(by=['ПОПЫТКИ'])
    print(df)
    print()
    print(df)
    write_results_table_to_file(FILENAME2, df)


def read_results_table_form_file(filename):
    excel_data_df = pandas.read_excel(filename)
    return excel_data_df.head(10)

def write_results_table_to_file(filename, df):
    df.to_excel(filename, index=False, header=True)


if __name__ == '__main__':
    # write_results_table_to_file(FILENAME2, df)
    telegram_bot(TOKEN)
    #insert('Вася', 100)

