import pymorphy2
import re




morph = pymorphy2.MorphAnalyzer()
form2 = morph.parse('дочь')
for form in form2:
    for lex in form.lexeme:
        print(lex)
print(same_form("печатая", "плачущий"))



