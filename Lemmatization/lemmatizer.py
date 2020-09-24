from abc import ABC
from argparse import ArgumentParser

import tabulate

from Lemmatization.base import Lemmatizer
from Lemmatization.lib.trie import Trie
from Lemmatization.main import check_for_prefix_chop, chop_words
from Lemmatization.utility import stop_words
from Lemmatization.utility.helper import get_root_pos_rule_csv_path
from Lemmatization.utility.reader import read_csv


class TrieLoader(object):
    def __init__(self):
        self.root = self._make_dict_trie()

    @staticmethod
    def _make_dict_trie():
        trie = Trie()
        csv_path = get_root_pos_rule_csv_path()
        root_data = read_csv(csv_path)
        for d in root_data:
            word = d.get('word').strip()
            rules = list(filter(None, d.get('rules').strip().split(',')))
            trie.insert(word, rules)
        return trie


class NepaliLemmatizer(Lemmatizer, ABC):
    rule_not_used_in_my_dict = [50, 49, 48, 24, 20, 12, 10, 5, 4, 3, 2]
    rule_not_used_in_default_dict = [2, 4, 5, 12, 20, 24, 50]

    def __init__(self):
        super().__init__()
        self.trie = TrieLoader().root

    def lemmatize_word(self, word):
        is_root, matched_str, word_list = self.trie.get_suggestions(word)
        if is_root:
            return word, word
        lemma = self._handle_not_root(matched_str, word)
        return dict(word=word, lemma=lemma)

    def trie_based_method(self, text):
        tokenized_text = self.tokenize(text)
        lemmatized_text = list()
        # print(f'words\tlemma')
        for index, sentence in enumerate(tokenized_text):
            lemmatized_sentence = list()
            for word in sentence:
                lemmatized_sentence.append(self.lemmatize_word(word))
            lemmatized_text.append(lemmatized_sentence)
        return lemmatized_text

    def _handle_not_root(self, matched, word):
        def filter_words(key, length):
            if len(key) != length:
                return False
            return key.endswith('्') or key.endswith('उ')

        is_root, matched_str, word_list = self.trie.get_suggestions(matched, filter_more=True)
        if is_root:
            return matched
        else:
            if not word_list:
                return word
            word_list = sorted(word_list, key=lambda tup: len(tup[0]), reverse=True)
            word_list = list(filter(lambda w: filter_words(w[0], len(word_list[0][0])), word_list)) or word_list
            return word_list[0][0] if isinstance(word_list[0], tuple) else word_list[0]

    def hybrid_method(self, text):
        tokenized_text = self.tokenize(text)
        lemmatized_text = list()
        for sentence in tokenized_text:
            lemmatized_sentence = list()
            for word in sentence:
                status, _word, word_ = get_lemma(self.trie, word)
                # print(status, _word, word_)
                lemmatized_sentence.append(dict(word=str(word), lemma=str(word_)))
            lemmatized_text.append(lemmatized_sentence)
        return lemmatized_text


def get_lemma(trie, word: str, chopped: str = None):
    if word == chopped:
        return 1, word, word
    word = chopped if chopped else word

    is_root, matched_str, word_list = trie.get_suggestions(word)
    if is_root:
        return 2, word, word
    elif word_list:
        rules = set()
        for w, r in word_list:
            rules = rules.union(set(r))
        status, new_word = check_for_prefix_chop(word, word_list, rules)
        if status:
            return 3, word, new_word
    return get_lemma(trie, word, chop_words(word))


def filter_stop_words_digits(word):
    if word.isdigit():
        return False
    return word not in stop_words.get_from_nltk()


def tabulate_result(result):
    header = ['word', 'lemma']
    for sentence in result:
        rows = [x.values() for x in sentence]
        print(tabulate.tabulate(rows, header, tablefmt="grid"))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-m",
        "--method",
        default="trie",
        help="Name of the lemmatization methods API e.g. trie, hybrid [Default: trie]",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--text",
        help="Nepali text to lemmatize",
        required=True
    )
    args = parser.parse_args()
    lem = NepaliLemmatizer()
    if args.method == 'trie':
        results = lem.trie_based_method(args.text)
        tabulate_result(results)
    elif args.method == 'hybrid':
        results = lem.hybrid_method(args.text)
        tabulate_result(results)
    else:
        print('Invalid method given for Lemmatization')
        exit(0)
