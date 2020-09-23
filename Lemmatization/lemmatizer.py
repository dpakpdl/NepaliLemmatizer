from abc import ABC

from Lemmatization.base import Lemmatizer
from Lemmatization.lib.trie import Trie
from Lemmatization.utility.reader import read_csv
from Lemmatization.main import check_for_prefix_chop, chop_words
from Lemmatization.utility import stop_words
from Lemmatization.utility.helper import get_root_pos_rule_csv_path


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
        return word, lemma

    def trie_based_method(self, text):
        tokenized_text = self.tokenize(text)
        lemmatized_text = list()
        # print(f'words\tlemma')
        for sentence in tokenized_text:
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
                lemmatized_sentence.append((word, word_))
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



if __name__ == "__main__":
    # paragraph = ' '.join(
    #     ["संवाददाता", "पहरेदार", "शासनप्रणाली", "स्वास्थ्यकर्मी", "बजारीकरण", "विरोधपत्र", "साहित्यकार",
    #      "कार्यपद्धति", "कानुनमन्त्री", "प्रयोगविधि", "काव्यशास्त्र", "कथाकारिता", "खच्चडवाला", "नैतिकता", "खुवाई",
    #      "कालिका", "सहसचिवहरु", "खाएन", "नखानु", "खाएनछ", "चुवावट"])
    # print(paragraph)
    # paragraph += " दोस्रो हुलाकी सडक अन्तर्गत लमही–कोइलाबास सडक विस्तार तथा कालोपत्रे भइरहेको छ । संरचना नभत्काएका कारण " \
    #              "सडक निर्माणमा ढिला भएको उनले बताए । ‘सडक निर्माणको काम रोकिन थाल्यो । आफैं भत्काउन धेरैपटक " \
    #              "अल्टिमेटम दिँदा पनि अटेर गरे,’ यादवले भने,‘अन्तमा बल प्रयोग गरेर सडक खाली गरियो ।’ २० जनाले " \
    #              "मुआब्जा पाएर आफै भत्काएको, तीन जनाले मुआब्जा नपाएर पनि भत्काएको र मुआब्जा पाएर पनि अटेर गरेका " \
    #              "एक दर्जन घरमा डोजर लगाउनु परेको उनले बताए । हेराइदिँदा"

    # lem = NepaliLemmatizer()
    # print(lem.lemmatize_word('निर्माणको'))
    # print(lem.hybrid_method('गुल्मेली'))
    # print(lem.lemmatize_word('गुल्मेली'))

    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument(
        "-m",
        "--method",
        default="trie",
        help="Name of the lemmatization methods API e.g. trie, hybrid [Default: trie]",
        # required=True
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
        print(lem.trie_based_method(args.text))
    elif args.method == 'hybrid':
        lem.hybrid_method(args.text)
    else:
        print('Invalid method given for Lemmatization')
        exit(0)

    # header = backup_list[0].keys()
    # rows = [x.values() for x in backup_list]
    # print(tabulate.tabulate(rows, header))
