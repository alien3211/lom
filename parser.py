#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
from initial import *


class Parser(object):
    
    def __init__(self):
        pass

    def checkPatern(self,patern):
        
        rest = patern.split()[::-1]
        command = rest.pop()

        if command in ['help', 'h']:
            return self.print_help(rest[::-1])
        elif command in ['set']:
            return self.set_option(rest[::-1])
        elif command in ['search', 's']:
            return self.search(rest[::-1])
        elif command in ['add','a']:
            return self.add_record(rest[::-1])
        elif command in ['update', 'u']:
            return self.update_record(rest[::-1])
        elif command in ['type']:
            return self.print_type(rest[::-1])
        elif command in ['access']:
            return self.print_access(rest[::-1])
        elif command in ['key']:
            return self.print_key(rest[::-1])
        elif command.isdigit():
            return self.digit(rest[::-1])
        elif command in ['news', 'n']:
            return self.news(rest[::-1])

    def print_help(self, option):
        return "TO JEST HELP",' '.join(option)

    def set_option(self, option):
        
        if len(option) >= 2:
            if option[0] in options.options('lom'):
                options.set('lom', option[0], replace_colour(between(' '.join(option))[1]))
                with open('/home/alan/.lomrc', 'wb') as configfile:
                    options.write(configfile)
            else:
                return replace_colour('')
        elif len(option) == 1:
            regex = re.compile(option[0])
            for row  in options.items('lom'):
                if regex.match(row[0]):
                    print "{:10} =  {} ".format(row[0],re_replace_colour(row[1]))
        else:
            for row  in options.items('lom'):
                    print "{:10} =  {} ".format(row[0],re_replace_colour(row[1]))
        return ""

    def search(self, option):
        return "search", ' '.join(option)

    def add_record(self, option):
        return "add record", ' '.join(option)

    def update_record(self, option):
        return "set record", ' '.join(option)

    def print_type(self, option):
        return "print type", ' '.join(option)

    def print_access(self, option):
        return "print access", ' '.join(option)

    def print_key(self, option):
        return "print key", ' '.join(option)

    def digit(self, option):
        return "is digit", ' '.join(option)

    def news(self, option):
        return "print news", ' '.join(option)

