#!/usr/bin/python

import os

# Color Support
###############

class TermColors(dict):
    """Gives easy access to ANSI color codes. Attempts to fall back to no color
for certain TERM values. (Mostly stolen from IPython.)"""

    COLOR_TEMPLATES = (
        ("black" , "0;30"),
        ("red" , "0;31"),
        ("green" , "0;32"),
        ("brown" , "0;33"),
        ("blue" , "0;34"),
        ("purple" , "0;35"),
        ("cyan" , "0;36"),
        ("lightgray" , "0;37"),
        ("darkgray" , "1;30"),
        ("lightred" , "1;31"),
        ("lightgreen" , "1;32"),
        ("yellow" , "1;33"),
        ("lightblue" , "1;34"),
        ("lightpurple" , "1;35"),
        ("lightcyan" , "1;36"),
        ("white" , "1;37"),
        ("end" , "0"),
    )

    NoColor = ''
    _base = '\033[%sm'

    def __init__(self):
        self.update(dict([(k, self._base % v) for k,v in self.COLOR_TEMPLATES]))

_C = TermColors()



def replace_list(rep, rep_to, text):
    for i in range(len(rep)):
        text = text.replace(rep[i], rep_to[i])
    return text

def replace_colour(text):
    rep = ['<black>', '<red>', '<green>', '<brown>', '<blue>', '<purple>', '<cyan>', '<lightgray>', '<darkgray>', '<lightred>', '<lightgreen>', '<yellow>', '<lightblue>', '<lightpurple>', '<lightcyan>', '<white>', '<end>']
    rep_to = [_C['black'], _C['red'], _C['green'], _C['brown'], _C['blue'], _C['purple'], _C['cyan'], _C['lightgray'], _C['darkgray'], _C['lightred'], _C['lightgreen'], _C['yellow'], _C['lightblue'], _C['lightpurple'], _C['lightcyan'], _C['white'], _C['end']]
    return replace_list(rep, rep_to, text)


def re_replace_colour(text):
    rep = [_C['black'], _C['red'], _C['green'], _C['brown'], _C['blue'], _C['purple'], _C['cyan'], _C['lightgray'], _C['darkgray'], _C['lightred'], _C['lightgreen'], _C['yellow'], _C['lightblue'], _C['lightpurple'], _C['lightcyan'], _C['white'], _C['end']]
    rep_to = ['<black>', '<red>', '<green>', '<brown>', '<blue>', '<purple>', '<cyan>', '<lightgray>', '<darkgray>', '<lightred>', '<lightgreen>', '<yellow>', '<lightblue>', '<lightpurple>', '<lightcyan>', '<white>', '<end>']
    return replace_list(rep, rep_to, text)

