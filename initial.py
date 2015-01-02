#!/usr/bin/env python
#-*- coding: utf-8 -*-

from os import getenv
import ConfigParser
from Tcolors import replace_colour, re_replace_colour
from lomSQL import lomsql 

# Global Variable
options = ConfigParser.RawConfigParser()
options.read('/home/' + getenv('USER') + '/.lomrc')

databases = lomsql()

types        = []
access       = []
keys         = []
search       = []
news_waiting = []
news_added   = []
last_log     = []


def prompt():
    r_prompt = replace_colour(options.get('lom','prompt')).replace('\'','').replace('"', '')
    options.set( 'lom','prompt', r_prompt)

def initialization():
    init_text = "\nLibrary Of Mind v1.0"
    prompt()
    if databases.get('SELECT user from USERS where user="' + options.get('lom','user') + '";') == []:
        databases.add('INSERT INTO USERS(user, id_access) VALUES ("' + options.get('lom','user') + '", 3)')
        print "Current user are exist"
        
    last_log = databases.get('SELECT last_log FROM USERS WHERE user=\'' + options.get('lom','user') + '\';')[0][0]
    news_waiting = databases.get('select * from WAITING w where w.data_a > \'' + last_log + '\';')
    news_added = databases.get('select * from LIBRARY l where l.data_a > \'' + last_log + '\';')

    init_text += "\nLast logged (<blue>" + last_log + "<end>)\n"

    if len(news_waiting) != 0 or len(news_added) != 0:
        init_text += "Since last logged add <green>" + str(len(news_waiting)) + "<end> waiting and <green>" + str(len(news_added)) + "<end> verified record/s to library\n"
    else:
        init_text += "Since last logged not added anything\n"

    init_text += "For more information use command <lightgray>help <cyan><command><end> or <lightgray>h <cyan><command><end>\n"
    print replace_colour(init_text)


def update_last_log():

    databases.add('UPDATE USERS SET last_log = datetime(\'now\') where user = \'' +  options.get('lom','user') + '\';')
    


def between(s,left="'", right="'"):
    s = s.replace("\"","'")
    before,_,a = s.partition(left)
    a,_,after = a.partition(right)
    return before,a,after
