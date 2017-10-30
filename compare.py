from gensim import corpora, models, similarities
import pickle
from collections import defaultdict
from pprint import pprint
import string

tweet_list=pickle.load(open('all_tweets.txt', 'rb'))
test_list=pickle.load(open('testlist.txt','rb'))

stoplist = set('for a of the and to in'.split())
texts = [[word for word in tweets.lower().split() if word not in stoplist] for tweets in tweet_list]

frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]

dictionary = corpora.Dictionary(texts)
dictionary.save('saveddict.dict')

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('corpus.mm', corpus)  # store to disk, for later use
corpus = corpora.MmCorpus('corpus.mm')
print (corpus)

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=1000,decay=1)
print(lsi)

doc = test_list[0]
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]

index = similarities.MatrixSimilarity(lsi[corpus])
index.save('corpus.index')
index = similarities.MatrixSimilarity.load('corpus.index')

sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])

vid_list=pickle.load(open('tempvids.txt','rb'))

user_list=pickle.load(open('userlist.txt','rb'))

tester=pickle.load(open('queryname.txt','rb'))

print("Query Twitter Name: ", tester[0])
for comparison in sims:
    print(user_list[comparison[0]], "score: ", comparison[1])

for i in range (0,2):
    print(user_list[sims[i][0]],' videos:')
    print ('\n'.join(vid_list[sims[i][0]]))


