#!/usr/bin/env python
# -*- coding: utf-8 -*-
# "LibraryOfMind" is distributed under GNU GPLv3+, WITHOUT ANY WARRANTY.
# Copyright(c) 2015: Alan Tetich <alan.tetich@gmail.com>

import pkgutil


def req(query, *arg):

    if pkgutil.find_loader('_curlOpen') is not None:
        import _curlOpen
        _curlOpen.req(query, arg)
