#excel 문서를 pandas를 통해 dataframe으로 읽어오기
import pandas as pd
import pprint
import glob
import nltk
import MeCab
from konlpy.tag import Mecab
from nltk.probability import FreqDist
from sklearn.manifold import TSNE
import re
import numpy

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

total_cells = []

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
                total_cells.append(fail_reasons_df.iloc[inx,jnx])
    # sentences = re.sub('([ㄱ-힣]+)(\s)',"\g<1>", sentences)
    print(sentences)
    values.append(sentences)



####################################################
### noun 만 식별하니까 문제가 발생
### 외국어가 이상하게 선별됨
### 명사값으로만 하는 것은 나중에 check 해볼것


def syntatic_values(phrase):
    """Noun extractor."""

    tagged = t.pos(phrase)
    return [s for s, t in tagged if t not in ['SY', 'JKS','SF','SN','SSO','SSC']]



# MeCab 형태소분석기로 단어만 식별함
doc_dict = dict(zip(keys,values))
#syntatic_values 으로만 이루어진 value 값만들기
noun_values = []
# for sentence in doc_dict.values():
for sentence in total_cells:
    noun_sentence=""
    print(t.pos(sentence))
    noun_sentence = " ".join(syntatic_values(sentence))
    noun_values.append(noun_sentence)

#명사값으로 구성된 dictionary 생성
noun_dict = dict(zip(keys, noun_values))


# ('.', 'SY')로 나오는 결과를 join을 활용해서 /로 묶어줌
# pos = lambda d: ['/'.join(p) for p in t.pos(d)]


# for inx in range(len(values)):
#     print(pos(values[inx]))

#####################################################################
##### CO-OCCURANCE MATRIX
#####


gen_docs = [[w.lower() for w in text.split()]
            for text in noun_values]

# co-occurrence matrix 만들기
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(min_df=5, ngram_range=(1, 1))

X = vectorizer.fit_transform(noun_values)
Xc = X.T * X  # co-occurrence matrix
Xc.setdiag(0)  # 대각성분을 0으로
result = Xc.toarray()  # array로 변환

# print(vectorizer.get_feature_names())

num_arr = numpy.asarray(result)
# numpy.savetxt("foo.csv", num_arr, delimiter=",")

for word, idx in vectorizer.vocabulary_.items():
    print("idx : %d [word : %s]" %(idx, word))


co_occur_df = pd.DataFrame(num_arr, columns=vectorizer.get_feature_names(), index=vectorizer.get_feature_names())

co_occur_df.to_excel('co_occurence.xlsx')


#####################################################################

texts_ko = [doc.split() for doc in noun_values]

#train
from gensim.models import word2vec
wv_model_ko = word2vec.Word2Vec(texts_ko)
wv_model_ko.init_sims(replace=True)
wv_model_ko.save('ko_word2vec_e.model')


#
# print(wv_model_ko.wv['양극'])




def tsne_plot(model):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []

    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()


tsne_plot(wv_model_ko)

