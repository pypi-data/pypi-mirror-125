import os
import argparse
import textwrap
from datetime import timedelta
from time import time
import shutil

import dask.multiprocessing
import dask.dataframe as dd

from konlpy.tag import Komoran


# mart parquet field
DEFAULT_MART_FIELDS = [
        'uid','title','content', 'comment', 'source_text',
        'source_site','i_date', 'script', 'c_date', 'domain'
        ]


#uid,url,title,c_cnt,source_text,content,category,source_site,comment,r_cnt,i_date,bad,tag,script,c_date,domain
dtypes = {
    'uid': str,
    'url': str,
    'title': str,
    'c_cnt': str,
    'source_text': str,
    'content': str,
    'category': str,
    'source_site': str,
    'comment': str,
    'r_cnt': str,
    'i_date': str,
    'bad': str,
    'tag': str,
    'script': str,
    'c_date': str,
    'domain': str,
}


class TimeCheckDecorator:
    def __init__(self, f):
        self.func = f

    def __call__(self, *args, **kwargs):
        start = time()
        self.func(*args, **kwargs)
        duration = time() - start
        strDuration = str(timedelta(seconds=duration)).split('.')[0]
        print(f'[{self.func.__name__}] duration: {strDuration}')


def stop_word_update(file):
    with open(file, 'r', encoding='utf-8-sig') as f:
        lines = f.read()

    return lines.split('\n')


def dist_morpheme(txt: str, komo: Komoran, stop_words):
    tmp = []
    if txt == None or komo == None or txt.strip() == '':
        #print('text or komoran is None.')
        return None

    try:
        for i in komo.pos(txt):
            if len(i[0]) > 1 and i[0] not in stop_words:
                tmp.append('/'.join(i))
    except:
        #print(f'Morpheme parse fail. ({txt})')
        return None


    ret = ' '.join(tmp)
    #print(textwrap.shorten(ret, width=30, placeholder="..."))
    return ret


def dist_map_partition(df, stop_words, user_dic):
    komo = Komoran(userdic=user_dic)
    df[['title', 'content', 'comment', 'script']] = df[['title', 'content', 'comment', 'script']]\
        .applymap(lambda x: dist_morpheme(x, komo, stop_words))
    
    return df


@TimeCheckDecorator
def do_morph(input, stop_words, user_dic, output_mart):

    dask.config.set(scheduler='processes')

    ddf: dd.DataFrame = dd.read_parquet(input)

    df = ddf.map_partitions(lambda x: dist_map_partition(x, stop_words, user_dic), meta=dtypes)
    df = df[DEFAULT_MART_FIELDS]
    df.to_parquet(output_mart, write_metadata_file=False, compression='snappy')


_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data_path(path):
    return os.path.join(_ROOT, path)


def main():
    default_input = get_data_path('data/dask_apt_20.csv.parquet')
    default_stop_words = get_data_path('data/stop_words.csv')
    default_user_dictionary = get_data_path('data/apt.dic')

    parser = argparse.ArgumentParser(description="BBDR distributed morpheme")
    parser.add_argument('-i', '--input-parquet', default=default_input)
    parser.add_argument('-s', '--stop-words', default=default_stop_words)
    parser.add_argument('-u', '--user-dictionary', default=default_user_dictionary)

    args = parser.parse_args()

    # input parquet file
    input = args.input_parquet
    if not os.path.isfile(input):
        print(f'There is no input parquet file. {input}')
        exit(1)

    # stop words 
    stop_words_file = args.stop_words
    if not os.path.isfile(stop_words_file):
        print(f'There is no stop words file. {stop_words_file}')
        stop_words = []
    else:
        stop_words = stop_word_update(stop_words_file)

    # user dictionary
    user_dictionary= args.user_dictionary
    if not os.path.isfile(user_dictionary):
        print(f'There is no user dictionary file. {user_dictionary}')
        user_dictionary = None

    # output parquet file
    output_directory = f'{input}.out'
    if os.path.isdir(output_directory): 
        #print(f'delete output directory: {output_directory}')
        shutil.rmtree(output_directory)

    do_morph(input, stop_words, user_dictionary, output_directory)


if __name__ == '__main__':
    main()

