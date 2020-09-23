#!/usr/bin/python
import time
import sys
from Lemmatization.utility.helper import get_root_pos_rule_csv_path
from Lemmatization.main import read_csv

TARGET = sys.argv[1]
MAX_COST = int(sys.argv[2])

# Keep some interesting statistics
NodeCount = 0
WordCount = 0


# The Trie data structure keeps a set of words, organized with one node for
# each letter. Each node has a branch for each letter that may follow it in the
# set of words.
class TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}

        global NodeCount
        NodeCount += 1

    def insert(self, word):
        node = self
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()

            node = node.children[letter]

        node.word = word


# read dictionary file into a trie
trie = TrieNode()

for d in read_csv(get_root_pos_rule_csv_path()):
    WordCount += 1
    trie.insert(d.get('word').strip())

print("Read %d words into %d nodes" % (WordCount, NodeCount))


# The search function returns a list of all words that are less than the given
# maximum distance from the target word
def search(word, max_cost):
    # build first row
    current_row = range(len(word) + 1)
    print(current_row)
    results = []

    # recursively search each branch of the trie
    for letter in trie.children:
        print(letter)
        search_recursive(trie.children[letter], letter, word, current_row, results, max_cost)

    return results


# This recursive helper is used by the search function above. It assumes that
# the previous_row has been filled in already.
def search_recursive(node, letter, word, previous_row, results, max_cost):
    columns = len(word) + 1
    current_row = [previous_row[0] + 1]
    # print(current_row)
    # Build one row for the letter, with a column for each letter in the target
    # word, plus one for the empty string at column 0
    for column in range(1, columns):

        insert_cost = current_row[column - 1] + 1
        delete_cost = previous_row[column] + 1

        if word[column - 1] != letter:
            replace_cost = previous_row[column - 1] + 1
        else:
            replace_cost = previous_row[column - 1]

        current_row.append(min(insert_cost, delete_cost, replace_cost))

    # if the last entry in the row indicates the optimal cost is less than the
    # maximum cost, and there is a word in this trie node, then add it.
    if current_row[-1] <= max_cost and node.word is not None:
        results.append((node.word, current_row[-1]))

    # if any entries in the row are less than the maximum cost, then
    # recursively search each branch of the trie
    if min(current_row) <= max_cost:
        for letter in node.children:
            search_recursive(node.children[letter], letter, word, current_row, results, max_cost)


start = time.time()
results = search(TARGET, MAX_COST)
end = time.time()

for result in results:
    print(result)

print("Search took %g s" % (end - start))
