class SuffixTrie(object):

    def __init__(self, t):
        """ Make suffix trie from t """
        t += '$'  # special terminator symbol
        self.root = {}
        for i in range(len(t)):  # for each suffix
            cur = self.root
            for c in t[i:]:  # for each character in i'th suffix
                if c not in cur:
                    cur[c] = {}  # add outgoing edge if necessary
                cur = cur[c]

    def follow_path(self, s):
        """ Follow path given by characters of s.  Return node at
            end of path, or None if we fall off. """
        cur = self.root
        for c in s:
            if c not in cur:
                return None
            cur = cur[c]
        return cur

    def has_substring(self, s):
        """ Return true iff s appears as a substring of t """
        return self.follow_path(s) is not None

    def has_suffix(self, s):
        """ Return true iff s is a suffix of t """
        node = self.follow_path(s)
        return node is not None and '$' in node


# print(SuffixTrie("परपर").root)
from nltk import WordNetLemmatizer
from nltk import PorterStemmer

lem = WordNetLemmatizer()
print(lem.lemmatize(word="ate", pos="v"))
st = PorterStemmer()
print(st.stem(word="ate"))