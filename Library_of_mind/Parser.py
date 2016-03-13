#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re


def parserArgument(arg):

    rest = arg.split()[::-1]
    command = rest.pop()
