import pymorphy2
import re


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
            if cur >= max:
                max = cur
                res = lex.word
    return res

words = ['клинок', 'сабля', 'копье', 'кинжал', 'шпага']
morph = pymorphy2.MorphAnalyzer()
teg_words = []
for word in words:
    tg_w = morph.parse(word)
    teg_words.append(tg_w[0].word)
for word in teg_words:
    print(word)

eng = morph.parse("steel")
print(eng[0].normal_form, eng[0].tag.POS)
