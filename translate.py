
# coding: utf-8

# In[1]:

from googletrans import Translator
translator = Translator()


# In[2]:

import codecs

fileObj = codecs.open( "c:\\temp\\bigram-word-korean.txt", "r", "utf-8" )
file_w_Obj = codecs.open("c:\\temp\\bigram-trans-word.txt", "a", "utf-8")

u = fileObj.readlines()

for i in u[:400]:
    translated_word = translator.translate(i)
    data = "%s -> %s\n" %(translated_word.origin, translated_word.text)
    file_w_Obj.write(data)

