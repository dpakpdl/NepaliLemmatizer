import os
import random
from typing import List, Tuple, Set

from Lemmatization.main import read_csv, get_suffix_rules_based_on_number, make_words, get_sorted_rules
from Lemmatization.utility import helper


def get_words_from_random_n_roots(number_of_roots: int = 1000):
    nepali_dictionary = read_csv(helper.get_root_pos_rule_csv_path())
    nepali_dictionary = random.sample(nepali_dictionary, number_of_roots)
    for d in nepali_dictionary:
        word = d.get('word').strip()
        rules = filter(None, d.get('rules').strip().split(','))
        if not rules:
            continue
        get_words(list(rules), [(word, list(rules))])


def get_words(rules: List, words: List[Tuple[str, List]]):
    data_path = helper.get_data_path()
    file_path = os.path.join(data_path, 'gold_data_test.txt')
    infile = open(file_path, 'a')
    rules = get_suffix_rules_based_on_number(rules, get_sorted_rules())
    words = filter_words(words, rules)
    # try:
    #     words = random.sample(words, 5)
    # except ValueError:
    #     pass
    for word, rule in words:
        new = make_words(word, rule)
        if not new:
            continue
        infile.writelines(f'{new},{word},{rule}\n')
    infile.close()


def filter_words(words: List[Tuple], rules: List[Tuple[str, ...]]) -> Set[Tuple[str, Tuple[str, ...]]]:
    """
    filters word whose rule matches with rules given
    """
    return {(word, r) for word, rule in words for r in rules if r[1] in rule}


if __name__ == '__main__':
    print(get_words_from_random_n_roots())
