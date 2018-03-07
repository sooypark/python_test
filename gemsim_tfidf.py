#excel 문서를 pandas를 통해 dataframe으로 읽어오기
import pandas as pd
import pprint
import glob
import nltk
import MeCab
from konlpy.tag import Mecab
from nltk.probability import FreqDist

import gensim
from nltk.tokenize import word_tokenize


t = Mecab()

#한글처리를 위해 font를 설정하는 방법
import matplotlib.pyplot as plt

#font_name = plt.font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
plt.rc('font', family='Malgun Gothic')

#file path를 읽어서 한꺼번에 file path를 file list를 만든다
#file list를 하나씩 읽어오면서 dataframe에 담는다
#data frame의 concat을 사용하여 한꺼번에 데이터 frame에 담는다
path = ""
allfiles = glob.glob(path + "\\*.xlsx")

frame = pd.DataFrame()
filelist = []

#file을 읽을때 index column을 넣지 않으려면 None으로 설정한다
for file_ in allfiles:
    data = pd.read_excel(file_, index_col=None)
    filelist.append(data)

frame = pd.concat(filelist)

# rownum을 구하기 위해서는 len(frame)을 사용하고, column의 길이를 구하기 위해서는 len(frame.columns)를 사용한다

sentences_capacity = ""

# 특정 df에서 특정값을 가져올때
failure_mode = set(frame["고장"])

# nan을 없애기 위해서 filter와 lamda 함수를 사용함
failure_mode = set(filter(lambda x: x == x , failure_mode))

# set을 list로 바꿈
keys = list(failure_mode)
values = []

for reason in keys:
    sentences = ""
    #df의 열에서 특정값을 가진 frame을 만들고 이를 dataframe으로 다시변경하기
    fail_reasons = frame[frame["고장"] == reason]
    fail_reasons_df = pd.DataFrame(fail_reasons)

    for inx in range(1, len(fail_reasons_df)):
        for jnx in range(1, len(fail_reasons_df.columns)):
            # reason과 동일한 sentence를 제거하여 plot을 그릴때 중복도를 업애려는 것
            if str(fail_reasons_df.iloc[inx,jnx]) != "nan" and str(fail_reasons_df.iloc[inx,jnx]) != reason:
                sentences += "." + str(fail_reasons_df.iloc[inx,jnx])
    values.append(sentences)


doc_dict = dict(zip(keys,values))

####################################################
### noun 만 식별하니까 문제가 발생
### 외국어가 이상하게 선별됨
### 명사값으로만 하는 것은 나중에 check 해볼것


def syntatic_values(phrase):
    """Noun extractor."""

    tagged = t.pos(phrase)
    return [s for s, t in tagged if t not in ['SY', 'JKS','SF','SN','SSO','SSC']]



# MeCab 형태소분석기로 단어만 식별함

#syntatic_values 으로만 이루어진 value 값만들기
noun_values = []
for sentence in doc_dict.values():
    noun_sentence=""
    # print(t.pos(sentence))
    noun_sentence = " ".join(syntatic_values(sentence))
    noun_values.append(noun_sentence)

#명사값으로 구성된 dictionary 생성
noun_dict = dict(zip(keys, noun_values))

### word bar chart
print(noun_dict.keys())

for key in noun_dict.keys():
    ko = nltk.Text(noun_dict[key].split())
    freq = FreqDist(noun_dict[key].split())
    x_axes = []
    y_axes = []
    for inx in range(20):
        top_50 = freq.most_common(20)
        x_axes.append(top_50[inx][0])
        y_axes.append(top_50[inx][1])
    print(type(ko))
    ko.vocab()
    print(x_axes)
    print(y_axes)
    plt.figure(figsize=(12, 4))
    plt.bar(x_axes, y_axes)
    plt.title(key)
    plt.show()
# ko.plot(50)

# print(noun_dict.items())


gen_docs = [[w.lower() for w in word_tokenize(text)]
            for text in noun_values]

# 1. dictionary 만들기
# print(gen_docs)
dictionary = gensim.corpora.Dictionary(gen_docs)
# print(dictionary[5])
# print(dictionary.token2id['바인더'])
# print("Number of words in dictionary:",len(dictionary))
# for i in range(len(dictionary)):
#     print(i, dictionary[i])

# 2. bag-of-words 만들기
corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
# print(corpus)

#3. tf-idf 만들기
tf_idf = gensim.models.TfidfModel(corpus)
# print(tf_idf)
s = 0
for i in corpus:
    s += len(i)
# print(s)

#4. create a similarity measure object
sims = gensim.similarities.Similarity("c:\\temp\\",tf_idf[corpus],
                                      num_features=len(dictionary))
# print(sims)
# print(type(sims))

# 5. similarity check
'''
query_doc = [w.lower() for w in word_tokenize("Socks are a force for good.")]
print(query_doc)
query_doc_bow = dictionary.doc2bow(query_doc)
print(query_doc_bow)
query_doc_tf_idf = tf_idf[query_doc_bow]
print(query_doc_tf_idf)

'''
number_cnt = 1
for key in noun_dict.keys():
    print("number:%d %s %s" %(number_cnt, key, noun_dict.keys()))
    query_doc = [w for w in noun_dict[key].split()]
    # print(query_doc)
    query_doc_bow = dictionary.doc2bow(query_doc)
    # print(query_doc_bow)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    # print(query_doc_tf_idf)
    print(sims[query_doc_tf_idf])
    number_cnt = number_cnt + 1
