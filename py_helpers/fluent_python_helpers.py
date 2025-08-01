#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module of helpers for >>py to extend functionality beyond just stuffdb.py ...
"""


# ---- tof






# ---- imports


import collections

# ---- end imports
Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]
    def __len__(self):
        return len(self._cards)
    def __getitem__(self, position):
        return self._cards[position]

# ---- eof