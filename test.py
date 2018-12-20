import pymorphy2
import re


def same_form(word1, word2):
    morph = pymorphy2.MorphAnalyzer()
    form1 = morph.parse(word1)[0]
    forms2 = morph.parse(word2)
    max = 0
    for form in forms2:
        l_form1 = re.split(r',| ', str(form1.tag))
        for lex in form.lexeme:
            l_form = re.split(r',| ', str(lex.tag))
            k = 5
            cur = 0
            for i in range(min(len(l_form), len(l_form1))):
                if l_form[i] == l_form1[i]:
                    cur += k
                if k != 1:
                    k -= 1
            if cur > max:
                max = cur
                res = lex.word

    return res

morph = pymorphy2.MorphAnalyzer()
form2 = morph.parse('дочь')
for form in form2:
    for lex in form.lexeme:
        print(lex)
print(same_form("печатая", "плачущий"))



