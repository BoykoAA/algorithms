import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans

def open_file():
    with open('football.txt') as f_in:
        football = f_in.readlines()

    return football

def get_datetime(football):
    data_time = []
    for i in football[1:]:
        data_time.append(i.split('\t')[1])

    data_time = [data_time[i][:10] for i in range(len(data_time))]
    data_time = pd.DataFrame(data_time, columns=['date'])

    return data_time

def get_text(data_time, football):
    text = []
    for i in football[1:]:
        text.append(i.split('\t')[0])

    data_time['text'] = text
    return data_time


def preproc_data(data_time):
    data_time['date'] = pd.to_datetime(data_time['date'])
    data_time = data_time.sort_values(by='date')

    return data_time


def resize_logs(logs):
    if len(logs) < 10000000:
        for i in [4, 2, 2]:
            logs = logs[::i]
        # print(len(logs))
        return logs

    elif len(logs) > 20000000:
        for i in [4, 2, 2, 2]:
            logs = logs[::i]
        # print(len(logs))
        return logs

    else:
        for i in range(2, 4):
            logs = logs[::i]
        # print(len(logs))
        return logs

def stage_split(data_time):
    text_begin = data_time[data_time['date'].isin(pd.date_range(start='2018-06-14', end='2018-06-20'))]['text'].values
    text_middle = data_time[data_time['date'].isin(pd.date_range(start='2018-06-21', end='2018-07-07'))]['text'].values
    text_final = data_time[data_time['date'].isin(pd.date_range(start='2018-07-08', end='2018-07-15'))]['text'].values

    text_begin = resize_logs(text_begin)
    text_middle = resize_logs(text_middle)
    text_final = resize_logs(text_final)

    return text_begin, text_middle, text_final


def cluster_logs(text, n_clusters=10):
    stopWords = stopwords.words('russian')
    vectorizer = TfidfVectorizer(stop_words=stopWords)
    X = vectorizer.fit_transform(text)
    true_k = n_clusters
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)
    # print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    cluster_words = []
    for i in range(true_k):
        with open('clusters.txt', 'a') as f_out:
            # print("Cluster %d:" % i),
            f_out.write(("Cluster %d:" % i))
            for ind in order_centroids[i, :10]:
                # print(' %s ' % terms[ind], end=' '),
                f_out.write((' %s ' % str(terms[ind])))
            f_out.write(('\n'))
            # print()
        with open('clusters.txt', 'a') as f_out:
            f_out.write('\n')
        print('clister %d:' % i ,'is done.')
    with open('clusters.txt', 'a') as f_out:
        f_out.write('---------------------------------------------')
        f_out.write('\n')


def get_cluster(text_begin, text_middle, text_final):
    cluster_logs(text_begin)
    cluster_logs(text_middle)
    cluster_logs(text_final)


def main():
    print('run.')
    football = open_file()
    print('open file done.')
    data_time = get_datetime(football)
    print('wait...')
    data_time = get_text(data_time, football)
    print('get data done')
    data_time = preproc_data(data_time)
    print('wait...')
    text_begin, text_middle, text_final = stage_split(data_time)
    print('stage split done')
    get_cluster(text_begin, text_middle, text_final)
    print('result save in cluster.txt')
    print('done')



if __name__ == '__main__':
    main()