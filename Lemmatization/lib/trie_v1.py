# -*- coding: utf-8 -*-

import sys
from typing import Tuple, List, Callable


class TrieNode(object):
    """
    Our trie node implementation. Very basic. but does the job
    """

    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Is it the last character of the word.`
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1
        # added parent node
        self.parent = None
        self.pos = None
        self.rules = []

    def pprint(self, indent="", last=True, stack=""):
        if indent != "":
            stack = stack + self.char

        sys.stdout.write(indent)
        if last:
            sys.stdout.write("┗╾")
            indent += "  "
        else:
            sys.stdout.write("┣╾")
            indent += "┃ "

        sys.stdout.write("{} ({})".format(self.char, self.counter))
        if self.word_finished:
            print(" - {}".format(stack))
        else:
            print()

        for i, c in enumerate(self.children):
            c.pprint(indent, i == len(self.children) - 1, stack)


def add(root: TrieNode, word: str, rules: List[str] = None, pos: str = None) -> None:
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
            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    node.word_finished = True
    node.rules = rules or []
    node.pos = pos or ''


def find(root, prefix: str) -> Tuple[bool, int]:
    """
    Check and return
      1. If the prefix exists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0
    for idx, char in enumerate(prefix):
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Have we reached end of a word while our prefix string is not exhausted?
        # Meaning, let's say, we have 'hammer' as a word in trie and the prefix
        # we are searching for is 'hammeres'.
        if node.word_finished and idx < (len(prefix) - 1) and not node.children:
            # If so, return false. We are trying to search for a prefix longer than
            # the actual closest match.
            return False, 0
        # Return False anyway when we did not find a word.
        if char_not_found:
            return False, 0
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.counter
