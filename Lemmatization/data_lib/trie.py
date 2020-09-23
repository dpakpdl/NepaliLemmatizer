from Lemmatization.main import read_csv, check_for_prefix_chop
from Lemmatization.utility.helper import get_root_pos_rule_csv_path


class TrieNode:
    def __init__(self):
        # Initialising one node for trie
        self.children = {}
        self.last = False
        self.word = None
        self.char = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, prefix, rules):
        # Inserts a key into trie if it does not exist already.
        # And if the key is a prefix of the trie node, just
        # marks it as leaf node.
        node = self.root

        for a in list(prefix):
            if not node.children.get(a):
                node.children[a] = TrieNode()

            node = node.children[a]
            node.char = a

        node.last = True
        node.word = prefix
        node.rules = rules

    def search(self, prefix):
        # Searches the given key in trie for a full match
        # and returns True on success else returns False.
        node = self.root
        found = True
        for a in list(prefix):
            if not node.children.get(a):
                found = False
                break
            node = node.children[a]

        return node and node.last and found

    def suggestions_rec(self, node, word, word_list):
        # Method to recursively traverse the trie
        # and return a whole word.
        if node.last:
            word_list.append((word, node.rules))

        for a, n in node.children.items():
            word_list = self.suggestions_rec(n, word + a, word_list)
        return word_list

    def get_suggestions(self, prefix, filter_more=False):
        # Returns all the words in the trie whose common
        # prefix is the given key thus listing out all
        # the suggestions for autocomplete.
        node = self.root
        not_found = False
        temp_word = ''
        word_list = list()
        for a in list(prefix):
            if not node.children.get(a):
                not_found = True
                break
            if node.last and node != self.root:
                word_list.append((node.word, node.rules))
            temp_word += a
            node = node.children[a]
        word_found = node and node.last and not not_found
        if word_found:
            return word_found, temp_word, []

        word_list = self.suggestions_rec(node, temp_word, word_list)

        def filter_words(possible_word):
            if filter_more:
                return len(prefix) + 1 >= len(possible_word[0])
            return len(prefix) >= len(possible_word[0])

        return word_found, temp_word, list(filter(filter_words, word_list))


if __name__ == "__main__":
    # creating trie object
    t = Trie()

    # creating the trie structure with the
    # given set of strings.
    for d in read_csv(get_root_pos_rule_csv_path()):
        rules = list(filter(None, d.get('rules').strip().split(',')))
        t.insert(d.get('word').strip(), rules)

    keys = ["संवाददाता", "पहरेदार", "शासनप्रणाली", "स्वास्थ्यकर्मी", "बजारीकरण", "विरोधपत्र", "साहित्यकार",
            "कार्यपद्धति", "कानुनमन्त्री", "प्रयोगविधि", "काव्यशास्त्र", "कथाकारिता", "खच्चडवाला", "नैतिकता", "खुवाई",
            "कालिका", "सहसचिवहरु", "खाएन", "नखानु", "खाएनछ", "चुवावट", "खाएको"]
    for key in keys:
        status, matched, word_lis = t.get_suggestions(key)
        if not status:
            rules = set()
            for w, r in word_lis:
                rules = rules.union(set(r))
            new_key = check_for_prefix_chop(key, word_lis, rules)
            print(matched, new_key, key, rules)
            print(t.get_suggestions(matched, filter_more=True))
        # print(status, word_lis)
