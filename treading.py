import time
import datetime
from threading import Thread
from Queue import Queue

def log(message):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print "%s %s" % (now, message)

def oblicz(x):
    time.sleep(x)
    return x * x

class WatekOblicz(Thread):
    def __init__(self, id, kolejka_zadan):
        Thread.__init__(self, name="WatekOblicz-%d" % (id))
        self.kolejka_zadan = kolejka_zadan
    def run(self):
        while True:
            req = self.kolejka_zadan.get()
            if req is None:
                self.kolejka_zadan.task_done()
                break

            value, kolejka_rezultatow = req
            result = oblicz(value)
            log("%s %s -> %s" % (self.getName(), value, result))
            kolejka_rezultatow.put(result)
            self.kolejka_zadan.task_done()

kolejka_zadan = Queue()

def threaded_sum(values):
    nsum = 0.0
    kolejka_rezultatow = Queue()
    for value in values:
        kolejka_zadan.put((value,kolejka_rezultatow))

    for _ in values:
        nsum += kolejka_rezultatow.get()
    return nsum

def main():
    log("uruchamiamy watek")

    N_liczba_w = 3

    for i in range(N_liczba_w):
        w = WatekOblicz(i,kolejka_zadan).start()

    result = threaded_sum((4,5,3,1.5,2.2))
    log("suma wynosi: %f" % (result))

    for i in range(N_liczba_w):
        kolejka_zadan.put(None)
    log("koniec watku")

if __name__ == "__main__":
    main()


