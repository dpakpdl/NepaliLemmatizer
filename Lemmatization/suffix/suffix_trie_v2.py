from Lemmatization.lib.trie_operations import add
from Lemmatization.lib.trie_v1 import TrieNode


class SuffixTree(object):
    def __init__(self, string):
        self.string = string
        self.root = TrieNode("*")
        self.root.is_root = False
        for i in range(len(string)):
            self._add_prefix(string[-i:])

    def _add_prefix(self, string):
        add(self.root, string)


SuffixTree("परपर").root.pprint()