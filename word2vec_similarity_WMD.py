
#two sample sentences
s1 = 'grade 위해'
s2 = '치수 Wt'

# print(wv_model_ko.most_similar(positive=["ceramic"]))
#
# #calculate distance between two sentences using WMD algorithm
# distance = wv_model_ko.wmdistance('Ceramic'.split(), 'ceramic'.split())
#
# print('distance = %.4f' % distance)


###########################################################
# word2vec을 활용한 문장비교
###########################################################


wmd_corpus = ['Abbb cccc dddd', 'Abbb bbbb bbb']

# Initialize WmdSimilarity.
from gensim.similarities import WmdSimilarity
num_best = 10
instance = WmdSimilarity(wmd_corpus, wv_model_ko, num_best=10)
sent = 'Al tab'

sims = instance[sent]  # A query is simply a "look-up" in the similarity class.

sims
