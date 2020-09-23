# encoding: utf8

from typing import Tuple, List, Set

from Lemmatization.lib.trie_v1 import TrieNode, add
from Lemmatization.utility import helper
from Lemmatization.utility.reader import read_csv
from Lemmatization.utility.reader import read_file


def stem_with_hunspell(word):
    import hunspell
    huns_obj = hunspell.HunSpell(helper.get_nepali_dict_path(), helper.get_nepali_rules_path())
    res = huns_obj.stem(word)
    for r in res:
        print(r.decode())


def get_suffix_rules(lines: List[str]) -> List[Tuple[str, ...]]:
    """
    filters the lines starts with SFX, split each line to tuple
    :param lines: lines read from rules file
    :return: list of tuples
    """
    return [tuple(line.strip().split(' ')) for line in lines if line.startswith('SFX')]


def get_suffix_rules_based_on_number(rule_number: List[str], rules: List[Tuple[str, ...]]) -> List[Tuple[str, ...]]:
    """
    filters the sorted rules based on rule number given
    :param rule_number: list: ['15', '22', '8', '43']
    :param rules: list of tuples of rules
    :return: list of tuples of filtered rules
    """
    return [rule for rule in rules if rule[1] in rule_number and rule[2] != "Y"]


def get_sorted_rules() -> List[Tuple]:
    """
    :return: list of sorted rules based on the length suffix or affix in descending order
    """
    lines = get_suffix_rules(read_file(helper.get_nepali_rules_path()))
    return sorted(lines, key=lambda tup: len(tup[3].split('/')[0]), reverse=True)


def make_dict_trie() -> TrieNode:
    root = TrieNode('*')
    csv_path = helper.get_root_pos_rule_csv_path()
    root_data = read_csv(csv_path)
    for d in root_data:
        word = d.get('word').strip()
        pos = d.get('pos').strip() or None
        rules = list(filter(None, d.get('rules').strip().split(',')))
        add(root, word, rules, pos)
    return root


def find_prefix(root, prefix: str) -> Tuple[bool, int, tuple, list]:
    """
    Check and return
      1. If the prefix exists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    # TODO check find prefix method / refactor
    node = root
    possibilities = []
    matched = ''
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 1, tuple(), []
    for idx, char in enumerate(prefix):
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                matched += char
                if node.word_finished:
                    possibilities.append((matched, node.rules))
                break
        # Have we reached end of a word while our prefix string is not exhausted?
        # Meaning, let's say, we have 'hammer' as a word in trie and the prefix
        # we are searching for is 'hammeres'.
        if node.word_finished and idx < (len(prefix) - 1) and not node.children:
            # If so, return false. We are trying to search for a prefix longer than
            # the actual closest match.
            if possibilities:
                possibilities = possibilities[-1]
            return False, 2, possibilities, []
        # Return False anyway when we did not find a word.
        if char_not_found:
            if possibilities:
                possibilities = possibilities[-1]
            return False, 3, possibilities, []
        if idx == len(prefix) - 1 and not node.word_finished:
            if possibilities:
                possibilities = possibilities[-1]
            return False, 4, possibilities, []
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    # print(possibilities)
    if possibilities:
        possibilities = possibilities[-1]
    return True, 5 + node.counter, possibilities, []


def get_rules_for_words_starting_with(starting: str, full_word: str) -> Tuple[Set, List[Tuple[str, List]]]:
    """
    get all words starting with a letter along with their rules for word formation
    :param starting: staring letter of word to be lemmatized, स
    :param full_word: word to be lemmatized; सम्बन्धमा
    :return: set of rules for all words founds, list of (word, rules)
    """
    rules_only = set()
    words = list()
    csv_path = helper.get_root_pos_rule_csv_path()
    root_data = read_csv(csv_path)
    for d in root_data:
        word = d.get('word').strip()
        rules = list(filter(None, d.get('rules').strip().split(',')))
        if rules and word.startswith(starting) and len(word) <= len(full_word):
            rules_only = rules_only.union(set(rules))
            words.append((word, rules))
    return rules_only, words


def get_matching_rules(rules: List[Tuple[str, ...]], word_to_lemmatize: str) -> List[Tuple[str, ...]]:
    """
    filter rules that do not have affix ending in given word to lemmatize
    :param rules: list of rules
    :param word_to_lemmatize: str
    :return: list of filtered rules
    """
    chopping_rules = list()
    for rule in rules:
        if word_to_lemmatize.endswith(rule[3].split('/')[0]):
            chopping_rules.append(rule)
    return chopping_rules


def filter_words(words: List[Tuple], rules: List[Tuple[str, ...]], full_word: str) -> Set[Tuple[str, Tuple[str, ...]]]:
    """
    filters word whose rule matches with rules given
    """
    return {(word, r) for word, rule in words for r in rules if len(full_word) >= len(word) and r[1] in rule}


def make_words(prefix_matched: str, rule: Tuple[str, ...]):
    """
    make word from prefix matched and rules
    :param prefix_matched: prefix matched
    :param rule: rule
    :return: word made using prefix and rules
    """
    if len(rule) == 5:
        _, rule_number, to_replace, replace_by, ending = rule
    else:
        _, rule_number, to_replace, replace_by, ending, _ = rule
    replace = replace_by.strip().split('/')
    replace_by = replace[0]

    def check_ending(token, end):
        if "." == end:
            return True
        end = end.replace('[', '')
        end = end.replace(']', '')
        end = list(end)
        if end[0] == '^':
            return all(not token.endswith(end) for end in end)
        return any(token.endswith(end) for end in end)

    def replace(token, to_replace, replace_by):
        if to_replace.isdigit() and int(to_replace) == 0:
            return token + replace_by
        return token[:-len(to_replace)] + replace_by

    if check_ending(prefix_matched, ending):
        return replace(prefix_matched, to_replace, replace_by)


def chop_words(full_word: str) -> str:
    """
    check all roots starting with characters less than the full word and make word using rules to find the correct root
    :param full_word: word to lemmatize
    :return: root or full word
    """
    for i in range(len(full_word) - 1, 0, -1):
        rules, words = get_rules_for_words_starting_with(full_word[:i], full_word)
        status, word = check_for_prefix_chop(full_word, words, rules)
        if status:
            return word

    return full_word


def check_for_prefix_chop(full_word: str, words: List[Tuple[str, List[str]]], rules: Set[str]) -> Tuple[bool, str]:
    """
    check if the rules of matched prefix forms the given word for lemmatization
    :param full_word: word to be lemmatized: हेराइदिँदा
    :param words: list of most matched prefix with the rules: [('हेराइ', ['15', '22', '8', '43'])]
    :param rules: list of rules of most matched prefix: ['15', '22', '8', '43']
    :return: either word or prefix
    """
    rules = get_suffix_rules_based_on_number(list(rules), get_sorted_rules())
    chopping_rules = get_matching_rules(rules, full_word)
    if not chopping_rules:
        return False, full_word
    words = filter_words(words, chopping_rules, full_word)
    for word, rule in words:
        built_word = make_words(word, rule)
        if full_word == built_word:
            return True, word
    return False, full_word


def get_lemma(trie, word: str, chopped: str = None) -> Tuple[int, str, str]:
    # TODO refactor/rethink of this algorithm
    if word == chopped:
        return 1, word, word
    word = chopped if chopped else word
    matched, num, prefix, _ = find_prefix(trie, word)
    if matched:
        return 0, word, word
    elif prefix:
        status, new_word = check_for_prefix_chop(word, [prefix], set(prefix[1]))
        if status:
            return 2, word, new_word
    return get_lemma(trie, word, chop_words(word))


if __name__ == '__main__':
    trie_node = make_dict_trie()
    t_word = 'हेराइदिँदा'
    print(get_lemma(trie_node, t_word))
