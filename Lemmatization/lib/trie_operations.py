# -*- coding: utf-8 -*-

import re
from typing import Tuple

from fuzzywuzzy import fuzz

from Lemmatization.lib.trie_v1 import TrieNode, find


def add(root, word: str, pos: str = None):
    """
    Adding a word in the trie structure
    """
    node = root
    for char in word:
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found it, increase the counter by 1 to keep track that another
                # word has it as well
                child.counter += 1
                # And point the node to the child that contains this char
                node = child
                found_in_child = True
                break
        # We did not find it so add a new child
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            new_node.parent = node
            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    node.word_finished = True
    node.pos = pos


def delete(root, prefix: str):
    """
        Delete Node at the last letter of prefix (if exists)
        To do this, we need to check first if prefix exists,
        then we need to determine the path to the end of the prefix
        and then pop the last char node
    """

    if find(root, prefix)[0]:
        node = root
        for char in prefix[:-1]:
            # Search through all the children of the present `node`
            for child in node.children:
                if child.char == char:
                    # We found the char existing in the child.
                    # Assign node as the child containing the char and break
                    node = child
                    break

        # Node at this point is the second to last character in trie, prune
        # via list revision
        node.children = [child for child in node.children if child.char != prefix[-1]]
        # Need to update the node.counter
        node.counter = len(node.children)


def find_prefix(root, prefix: str, pos: str) -> Tuple[bool, int, str, list]:
    """
    Check and return
      1. If the prefix exists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    matched = ''
    possibilities = []
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0, matched, possibilities
    for char in prefix:
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
                    possibilities.append(matched)
                break
        # Return False anyway when we did not find a char.
        if char_not_found:
            new_possibilities = []
            if node.word_finished:
                new_possibilities.append((matched, node.pos))
            for n in node.children:
                if n.word_finished:
                    new_possibilities.append((matched + n.char, n.pos))
            return False, 0, matched, get_most_matched(new_possibilities, prefix, pos)
            # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.counter, matched, possibilities


def get_node(node, level):
    while level:
        node = node.children
        level -= 1
    return node


def back_track(node, level=1):
    node = get_node(node, level=level)
    return [n for n in node if n.word_finished]


def build_all_children(node):
    possibilities = set()
    if not node.children:
        possibilities.add('')
        return possibilities

    for node in node.children:
        for s in build_all_children(node):
            if node.word_finished and s:
                possibilities.add(node.char)
            possibilities.add(str(node.char) + s)
    return possibilities


def scoring_function(string, matched, possibilities):
    highest_matched = matched
    values = [(highest_matched + str(x.char), x.pos)
              for x in possibilities if len(x.char) + len(highest_matched) < len(string)]

    # get_highest_character_matched(values, string)
    # get_most_matched(values, string)
    return values


def get_highest_character_matched(possibilities, string):
    regex = r"|".join(possibilities)
    print(re.findall(regex, string))


def get_most_matched(possibilities, string, pos):
    fuzz_ratio = {p[0]: (fuzz.ratio(p, (string, pos)), p[1]) for p in possibilities}
    data = sorted(fuzz_ratio.items(), key=lambda x: x[1], reverse=True)
    return data
