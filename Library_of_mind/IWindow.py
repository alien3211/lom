import log
import pkgutil

def getWindow(a):
    log.LOG("IN GETWINDOW")
    if pkgutil.find_loader('gtk') is not None: 
        import WindowGTK
        return WindowGTK.Window()
    elif pkgutil.find_loader('PyQt') is not None: 
        import WindowQT
        return WindowQT.Window()

