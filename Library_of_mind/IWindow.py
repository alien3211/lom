import log
import pkgutil

def getWindow(a):
    log.LOG("IN GETWINDOW")
    if pkgutil.find_loader('gtk') is not None: 
        log.LOG("import GTK")
        import WindowGTK
        return WindowGTK.Window()
    elif pkgutil.find_loader('PyQt') is not None: 
        log.LOG("import QT")
        import WindowQT
        return WindowQT.Window()

