import pandas as pd
import numpy as np
import artm

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
        for i in [4, 4, 2, 2, 2]:
            logs = logs[::i]
        print(len(logs))
        return logs

    elif len(logs) > 20000000:
        for i in [4, 4, 3, 2, 2]:
            logs = logs[::i]
        print(len(logs))
        return logs

    else:
        for i in range(2, 4):
            logs = logs[::i]
        print(len(logs))
        return logs

def stage_split(data_time):
    text_begin = data_time[data_time['date'].isin(pd.date_range(start='2018-06-14', end='2018-06-20'))]['text'].values
    text_middle = data_time[data_time['date'].isin(pd.date_range(start='2018-06-21', end='2018-07-07'))]['text'].values
    text_final = data_time[data_time['date'].isin(pd.date_range(start='2018-07-08', end='2018-07-15'))]['text'].values

    text_begin = resize_logs(text_begin)
    text_middle = resize_logs(text_middle)
    text_final = resize_logs(text_final)

    return text_begin, text_middle, text_final

def save_new_stage(text_begin, text_middle, text_final):
    with open('begin_log.txt', 'w') as f_out:
        for i in (text_begin):
            f_out.write(i)

    with open('middle_log.txt', 'w') as f_out:
        for i in (text_middle):
            f_out.write(i)

    with open('final_log.txt', 'w') as f_out:
        for i in (text_final):
            f_out.write(i)


def cluster_artm(text):
    bach_vectorizer = artm.BatchVectorizer(data_path=text,
                                           data_format='vowpal_wabbit', target_folder='batch_small',
                                           batch_size=20)
    T = 10  # количество тем
    topic_names = ["sbj" + str(i) for i in range(T - 1)] + ["bcg"]

    model_artm = artm.ARTM(num_topics=T, topic_names=topic_names, reuse_theta=True,
                           num_document_passes=1)

    np.random.seed(1)
    dictionary = artm.Dictionary()
    dictionary.gather(data_path=bach_vectorizer.data_path)
    model_artm.initialize(dictionary)

    model_artm.scores.add(artm.TopTokensScore(name='metric1', num_tokens=15))

    model_artm.regularizers.add(artm.SmoothSparsePhiRegularizer(name='smoothing', dictionary=dictionary,
                                                                topic_names='bcg', tau=1e5))

    model_artm.fit_offline(batch_vectorizer=bach_vectorizer, num_collection_passes=6)
    model_artm.regularizers.add(artm.SmoothSparsePhiRegularizer(name='stimulates',
                                                                dictionary=dictionary,
                                                                topic_names=["sbj" + str(i) for i in range(0, 29)],
                                                                tau=-1e5))

    model_artm.fit_offline(batch_vectorizer=bach_vectorizer, num_collection_passes=6)

    for topic_name in model_artm.topic_names:
        with open('cluster_log_artm.txt', 'a') as f_in:
            f_in.write(topic_name + ':')
            for word in model_artm.score_tracker["metric1"].last_tokens[topic_name]:
                f_in.write(word + ' ')
            f_in.write('\n')

def get_cluster():
    cluster_artm('begin_log.txt')
    cluster_artm('middle_log.txt')
    cluster_artm('final_log.txt')


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
    print('wait...')
    save_new_stage(text_begin, text_middle, text_final)
    get_cluster()
    print('result save in cluster_log_artm.txt')
    print('done')



if __name__ == '__main__':
    main()