from Lemmatization.utility.helper import get_stop_word_path
from Lemmatization.utility.reader import read_file


def get_from_nltk():
    from nltk.corpus import stopwords
    return stopwords.words('nepali')


def get_from_collections():
    # Downloaded from: https://github.com/kushalzone/NepaliStopWords/
    stop_word_file = get_stop_word_path()
    return read_file(stop_word_file)
