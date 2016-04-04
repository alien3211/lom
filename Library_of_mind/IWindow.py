#!/usr/bin/env python
#-*- coding: utf-8 -*-

import log
import pkgutil
import os

def getWindow(configData):
    log.LOG("IN GETWINDOW")
    if pkgutil.find_loader('gtk') is not None: 
        log.LOG("import GTK")
        import WindowGTK
        configData['user'] = os.environ['USER']
        configData['lomrc'] = os.environ['HOME'] + "/.lomrc"
        return WindowGTK.Window(configData)
    elif pkgutil.find_loader('PyQt') is not None: 
        log.LOG("import QT")
        import WindowQT
        return WindowQT.Window()

