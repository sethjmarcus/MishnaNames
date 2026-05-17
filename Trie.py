class TrieNode:
    def __init__(self):
        self.children = {}
        self.names = []   # terminal names


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()

            node = node.children[ch]

        node.names.append(word)