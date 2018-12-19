import sys
import telebot
import gensim, logging
from telebot import types
import pymorphy2
import re
import json

model = gensim.models.Word2Vec.load('word2vec11.model')
model.init_sims(replace=True)

TOKEN = '782488600:AAGCguW2x4jfUE8wNiaxwKkQbWRbyAQ0PWs'

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(TOKEN)


markup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton('Режим ближайших соседей слова')
itembtn2 = types.KeyboardButton('Режим лишнего слова в списке')
itembtn3 = types.KeyboardButton('Режим схожести двух слов')
markup.add(itembtn1, itembtn2, itembtn3)

markup.one_time_keyboard = True

users = {}

def same_form(word1, word2):
    morph = pymorphy2.MorphAnalyzer()
    form1 = morph.parse(word1)[0]
    forms2 = morph.parse(word2)
    res = ''
    max = 0
    for form in forms2:
        l_form1 = re.split(r',| ', str(form1.tag))
        for lex in form.lexeme:
            l_form = re.split(r',| ', str(lex.tag))
            cur = 5 if (l_form[0] == l_form1[0]) else 0
            cur += len(set(l_form) & set(l_form1))
            if cur > max:
                max = cur
                res = lex.word
                print()
    return res

@bot.message_handler(func=lambda message: str(message.text).startswith('Режим'))
def answer(message):

    if message.text.lower() == 'режим ближайших соседей слова':
        users[str(message.chat.id)] = 1
        print(users[str(message.chat.id)])
        bot.send_message(message.chat.id, 'Режим ближайших соседей слова включен')
    elif message.text.lower() == 'режим лишнего слова в списке':
        users[str(message.chat.id)] = 2
        print(users[str(message.chat.id)])
        bot.send_message(message.chat.id, 'Режим лишнего слова в списке включен')
    elif message.text.lower() == 'режим схожести двух слов':
        users[str(message.chat.id)] = 3
        print(users[str(message.chat.id)])
        bot.send_message(message.chat.id, 'Режим схожести двух слов включен')

@bot.message_handler(commands=['start'])
def answer(message):
    users[str(message.chat.id)] = 0
    bot.send_message(message.chat.id, 'Задайте режим запросов.', reply_markup=markup)

@bot.message_handler(content_types=["text"])
def answer(message):
    words = re.split(r', |,| ', message.text.lower())
    tag_words = []
    morph = pymorphy2.MorphAnalyzer()
    for word in words:
        tg_w = morph.parse(word)[0]
        if not (None == tg_w.tag.POS):
            tag_words.append(tg_w.normal_form + '_' + tg_w.tag.POS)
        else:
            tag_words.append('')
    if not (str(message.chat.id) in users):
        bot.send_message(message.chat.id, 'Задайте режим запросов.', reply_markup= markup)
        # Если режим ближайших соседей слова
    elif users[str(message.chat.id)] == 1:
        msg = ''
        if len(words) != 1:
            bot.send_message(message.chat.id, 'Введите одно слово!')
        elif tag_words[0] not in model:
            bot.send_message(message.chat.id, 'Слово ' + str(words[0]) + ' отсутствует в модели :(')
        else:
            msg += words[0] + '\n'
            # выдаем 10 ближайших соседей слова:
            if (tag_words[0] != ''):
                for i in model.most_similar(positive=[tag_words[0]], topn=10):
                # слово + коэффициент косинусной близости
                    word2 = i[0][:i[0].find('_')]
                    print(tag_words[0],word2)
                    res_word = same_form(words[0], word2)
                    msg += str(res_word) + ' ' + str(i[1]) + '\n'
                bot.send_message(message.chat.id, msg)
            else:
                bot.send_message(message.chat.id, 'Слово ' + str(words[0]) + ' отсутствует в модели :(')
    # Если режим лишнего слова в списке
    elif users[str(message.chat.id)] == 2:
        if len(words) < 2:
            bot.send_message(message.chat.id, 'Введено слишком мало слов. Попробуйте снова.')
        else:
            doesnt_exist = -1
            for i in range(len(tag_words)):
                if tag_words[i] not in model:
                    doesnt_exist = i
                    break
            if doesnt_exist == -1:
                res = model.doesnt_match(tag_words)
                bot.send_message(message.chat.id, res[:res.find('_')])
            else:
                bot.send_message(message.chat.id, 'Слово ' + str(words[i]) + ' отсутствует в модели :(')
    # Если режим лишнего слова в списке
    elif users[str(message.chat.id)] == 3:
        if len(words) != 2:
             bot.send_message(message.chat.id, 'Ошибка! Введите два слова!')
        elif tag_words[0] not in model:
            bot.send_message(message.chat.id, 'Слово ' + str(words[0]) + ' отсутствует в модели :(')
        elif tag_words[1] not in model:
            bot.send_message(message.chat.id, 'Слово ' + str(words[1]) + ' отсутствует в модели :(')
        else:
            bot.send_message(message.chat.id, str(model.similarity(tag_words[0], tag_words[1])))

@bot.callback_query_handler(func=lambda call: True)
def  test_callback(call):
    logger.info(call)
if __name__ == '__main__':
    bot.polling(none_stop=True)
