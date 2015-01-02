#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from parser import *
import readline

readline.parse_and_bind("tab: complete")
        

if __name__ == '__main__':
    
    import sys
    import os

    initialization()
    update_last_log()
    parser = Parser()

    while True:
        try:

            patern = raw_input(options.get('lom','prompt'))
            
            if patern.lower() in ('q', 'exit', 'quit'):
                print 'Thanks for used this aplication'
                exit(0)
            else:
                if patern != "":
                    print parser.checkPatern(patern)

        except (KeyboardInterrupt, EOFError):
            print '\nIf you want exit this program \nyou mast write \'quit\' or \'exit\' or \'q\''
