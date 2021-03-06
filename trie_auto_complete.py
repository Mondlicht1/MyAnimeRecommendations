"""CSC111 Final Project: My Anime Recommendations
===============================================================
The trie_auto_complete module.
This module contains functions to create an Trie data structure from the
datafiles as described in the report.
================================================================
@author: Raazia Hashim
"""
from __future__ import annotations
from typing import Optional, List, Dict


class TrieNode:
    """A TrieNode in the Trie data structure.
        Instance Attributes:
            - letter: The letter contained in this TrieNode, None if this is the root of the Trie.
            - is_word: True if this node indicates the end of a word, False otherwise.
            - children: The nodes that are adjacent to this node.
        Representation Invariants:
            - self not in self.children
    """
    letter: Optional[str]
    is_word: bool
    children: Dict[str, TrieNode]

    def __init__(self, letter: Optional[str], is_word: Optional[bool] = False) -> None:
        """Initializing a new TrieNode with the given letter and is_word value.
        By default, the is_word attribute is set to False.
        """
        self.letter = letter
        self.is_word = is_word
        self.children = {}

    def find_node_from_str_index(self, word: str, start: int) -> tuple[str, Optional[TrieNode]]:
        """Find a node that match the given string, starting from an index.
        Returns a tuple containing the correct part of word from `start` (because this search is
        case-insensitive) and the node that match the end of word.
        If no node that match the word is found, return a tuple of ('', None)
        """
        if start >= len(word):
            return ('', None)

        elif word[start] == self.letter or word[start].swapcase() == self.letter:
            if start == len(word) - 1:
                return (self.letter, self)
            for child in self.children:
                correct_substr, leaf = \
                    self.children[child].find_node_from_str_index(word, start + 1)
                if leaf is not None:
                    return (self.letter + correct_substr, leaf)

        return ('', None)


class Trie:
    """A Trie data structure used to implement an autocomplete algorithm.
    Instance Attributes:
            - root: The TrieNode stored at this Trie's root, or None if the Trie is empty. The
            root by default contains no letter value.
    """
    root: Optional[TrieNode]

    def __init__(self, all_words: Optional[List[str]]) -> None:
        """Initializing a new Trie data structure consisting of words in the list all_words.
        The root of the Trie has value equal to an empty string.
        The Trie is empty if and only if self.root.children == {}
        """
        self.root = TrieNode('', False)
        for word in all_words:
            self.insert_word(word)

    def insert_word(self, word: str) -> None:
        """Insert the given word into the Trie data structure.
        """
        curr_node = self.root

        for char in word:

            if char not in curr_node.children:
                curr_node.children[char] = TrieNode(char)

            curr_node = curr_node.children[char]

        curr_node.is_word = True

    def is_empty(self) -> bool:
        """Return whether this trie is empty.
        """
        return self.root.children == {}

    def __contains__(self, word: str) -> bool:
        """Returns whether the word is in the Trie.
        """
        curr_node = self.root
        for char in word:

            if char not in curr_node.children:
                return False

            curr_node = curr_node.children[char]

        return curr_node.is_word

    def find_node(self, word: str) -> tuple[Optional[str], Optional[TrieNode]]:
        """Find and return the node that has the given word.
        This method returns a tuple of the correct prefix (with correct letter cases) and the
        TrieNode that contains the last letter in the Trie.
        Return the root if the word is not found in the Trie.
        """
        for node in self.root.children:
            correct_word, leaf = self.root.children[node].find_node_from_str_index(word, 0)
            if leaf is not None:
                return (correct_word, leaf)

        return ('', None)

    def all_words(self) -> List[str]:
        """Return all possible words in the trie.
        """
        words_so_far = []

        start_node = self.root

        self._collect_words(start_node, '', words_so_far)

        return words_so_far

    def _collect_words(self, node: TrieNode, path: str, words_so_far: List[str]) -> None:
        """Collects all words continuing from the given node and path.
        """
        for child in node.children.values():
            if child.is_word:
                words_so_far.append(path + child.letter)

            self._collect_words(child, path + child.letter, words_so_far)

    def all_suffixes(self, prefix: str) -> List[str]:
        """Return all possible suffixes of the prefix found in the Trie.
        This method returns a list, where all elements are strings in the from prefix + suffix.
        Note that the empty string is a valid suffix.
        Return a list with just the prefix if prefix is not found in the Trie.
        """
        correct_prefix, start_node = self.find_node(prefix)
        words_so_far = []

        if start_node is not None and start_node.is_word:
            words_so_far.append(correct_prefix)

        if start_node is None:
            return words_so_far
        else:
            self._all_suffixes_(start_node, correct_prefix, words_so_far)

        return words_so_far

    def _all_suffixes_(self, node: TrieNode, prefix: str, words_so_far: List[str]) -> None:
        """Helper method for the all_suffixes method.
        """
        for child in node.children.values():
            if child.is_word:
                words_so_far.append(prefix + child.letter)

            self._all_suffixes_(child, prefix + child.letter, words_so_far)

    def longest_suffix(self, prefix: str) -> str:
        """Find and return the longest word that begins with prefix
        Note, the shorted suffix will always be the word itself.
        """
        all_words = self.all_suffixes(prefix)

        return max(all_words, key=len)
