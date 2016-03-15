#!/usr/bin/env python
#-*- coding: utf-8 -*-

__all__ = ['parserArgument']

import re
from MySQL import ConMySQL


def parserArgument(arg):

    rest = arg.split()
    command = rest.pop(-1)

    if command in ['help', 'h']:
        return getHelp(rest)
    elif command in ['set']:
        return setOption(rest)
    elif command in ['search', 's']:
        return search(rest)
    elif command in ['add','a']:
        return addRecord()
    elif command in ['update', 'u']:
        return updateRecord(rest)
    elif command in ['type', 't']:
        return getType(rest)
    elif command in ['key', 'k']:
        return getKey(rest)
    elif command in ['news', 'n']:
        return getNews(rest)
    elif command.isdigit():
        return getDigit(int(command))

def getHelp(com):
    
    return ConMySQL.getHelp(com)

def search(com):
    pass

def addRecord(com):
    pass

def getType(com):

    if com:
    	return ConMySQL.getType(com)
    else:
    	return ConMySQL,getType()

def getKey(com):
    
    if com:
    	return ConMySQL.getKey(com)
    else:
    	return ConMySQL,getKey()

def getNews(com):
    pass

def getDigit(com):
    pass
