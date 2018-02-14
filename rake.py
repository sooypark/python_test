#문서단위로 n-gram을 뽑아낼때 사용하는 것임

import RAKE.RAKE as rake
from konlpy.tag import Twitter
import nltk
import re


def count_n_gram(text,find_text):
    lst =[]
    sent = text.lower()
    #sent = re.sub("[A-z0-9\'\"`\|\/\+\#\,\)\(\?\!\b\-\:\=\;\.\«\»\—\@]", '', sent)
    sent = re.findall(find_text.lower(), sent)
    print(sent)
    for inx in sent:
        lst.append(inx)
    return lst


#하기는 참고 function
def tokenize(input_file, encoding):
    lst =[]
    with open(input_file, 'r', encoding=encoding) as f:
        for sent in f:
            sent = sent.lower()
            #sent = re.sub("[A-z0-9\'\"`\|\/\+\#\,\)\(\?\!\b\-\:\=\;\.\«\»\—\@]", '', sent)
            sent = re.findall('[a-z-]+', sent)
            for word in sent:
                lst.append(word)
    return lst

rake_object = rake.Rake("c:\\temp\\SmartStoplists.txt")

text = "Natural language processing (NLP) deals with the application of computational models to text or speech data. Application areas within NLP include automatic (machine) translation between languages; dialogue systems, which allow a human to interact with a machine using natural language; and information extraction, where the goal is to transform unstructured text into structured (database) representations that can be searched and browsed in flexible ways. NLP technologies are having a dramatic impact on the way people interact with computers, on the way people interact with each other through the use of language, and on the way people access the vast amount of linguistic data now in electronic form. From a scientific viewpoint, NLP involves fundamental questions of how to structure formal models (for example statistical models) of natural language phenomena, and of how to design algorithms that implement these models. In this course you will study mathematical and computational models of language, and the application of these models to key problems in natural language processing. The course has a focus on machine learning methods, which are widely used in modern NLP systems: we will cover formalisms such as hidden Markov models, probabilistic context-free grammars, log-linear models, and statistical models for machine translation. The curriculum closely follows a course currently taught by Professor Collins at Columbia University, and previously taught at MIT."
orgtext = text

keywords = rake_object.run(text)

print (keywords[0])
t = Twitter()

analysing_candidate_terms = []
index_num = 0

for inx, number in keywords:

    return_msg = ""
    text = t.morphs(inx)
    for i, tag in nltk.pos_tag(text):
        print(i, tag)
        if tag in ['VBZ', 'VBP']:
            return_msg = "VB"
    if return_msg == "" and number > 8:
        analysing_candidate_terms.append(keywords[index_num])
    else:
        return_msg = ""

    index_num = index_num + 1

print(analysing_candidate_terms)

list_n_gram =count_n_gram(orgtext, "probabilistic context-free grammars")
print(list_n_gram)


#1. file에서 문서를 읽는다.

#2. 읽은 문서를 stop-words 기준으로 문서를 자른다. stop-words-list는 따로 관리한다.

#3. stop-words 기준으로 잘라진 내용 중 명사구(NN, A N)와 같은 것들만 남기기 위해서 VBZ, VBP를 포함한 것을 제외한다.
# 제외된 List를 candidate term으로 남겨 놓는다

#4. candidate term의 TF를 얻어서 실제문서에서 TF을 통한 중요도를 판단한다
