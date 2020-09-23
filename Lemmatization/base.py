# -*- coding: utf-8 -*-
from Lemmatization.main import make_dict_trie, read_csv, get_sorted_rules, get_lemma, find_prefix
from Lemmatization.utility import helper
from Lemmatization.tokenization.tokenizer import NepaliTextTokenizer


class TrieLoader(object):
    def __init__(self):
        self.root = make_dict_trie()


class DictLoader(object):
    def __init__(self):
        csv_path = helper.get_root_pos_rule_csv_path()
        self.data = read_csv(csv_path)


class RuleLoader(object):
    def __init__(self):
        self.rules = get_sorted_rules()


class Lemmatizer(object):
    def __init__(self):
        self.trie = TrieLoader().root
        self.rules = RuleLoader().rules
        self.nepali_dict = DictLoader().data
        self.tokenizer = NepaliTextTokenizer()

    def tokenize(self, text):
        sentences = self.tokenizer.sentence_tokenize(text)
        tokenized_text = []
        for sentence in sentences:
            tokenized_text.append(self.tokenizer.word_tokenize(sentence))
        return tokenized_text

    def hybrid_method(self, text):
        tokenized_text = self.tokenize(text)
        lemmatized_text = list()
        print(f'words\tlemma')
        for sentence in tokenized_text:
            lemmatized_sentence = list()
            for word in sentence:
                _, _, lemma = get_lemma(self.trie, word, '')
                print(f"{word}\t{lemma}")
                lemmatized_sentence.append((word, lemma))
            lemmatized_text.append(lemmatized_sentence)
        return lemmatized_text

    def trie_based_method(self, text):
        tokenized_text = self.tokenize(text)
        lemmatized_text = list()
        # print(f'words\tlemma')
        for sentence in tokenized_text:
            lemmatized_sentence = list()
            for word in sentence:
                matched, _, lemma, _ = find_prefix(self.trie, word)
                lemma = lemma[0] if lemma else word
                # print(f"{word}\t{lemma}")
                lemmatized_sentence.append((word, lemma))
            lemmatized_text.append(lemmatized_sentence)
        return lemmatized_text

    def rule_based_approach(self):
        raise NotImplementedError


if __name__ == "__main__":
    lemmatizer = Lemmatizer()
    sent = "कोरोना संक्रमण नियन्त्रण गर्न भन्दै सरकारले घोषणा गरेको लकडाउनका कारण यातायातका साधन नचलेपछि काठमाडौंबाट " \
           "मानिसहरू बीपी राजमार्ग हुँदै पैदल नै तराईका जिल्ला गइरहेका छन् । लकडाउन लम्बिने संकेत देखिए पछि " \
           "काठमाडौंबाट बेखर्ची भएर हिँडेका उनीहरू भोक, प्यास नभन्दै ५-६ दिनसम्म लगाएर कम्तीमा ३ सय " \
           "किलोमिटर दूरी पार गर्दै आएका हुन् ।"
    print(lemmatizer.trie_based_method(sent))
