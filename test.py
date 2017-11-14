from threading import Thread
import time
import decide_bangbang as d
import queue as q
from collections import namedtuple
import logging
import random

logging.basicConfig(level=logging.INFO,format='%(threadName)s : %(message)s')

class BangBangRandomTest(d.Decide):
    def decide(self, out):
        return out + random.randint(-1*self.mulstep*self.step
                             if out - self.mulstep*self.step >= 0
                             else 0,
                             2*self.mulstep*self.step
                             if out + 2*self.mulstep*self.step
                             else 150-out)

    def __init__(self, inQueue, outQueue , params):
        super().__init__(inQueue, outQueue, params, tolerance)
        self.mulstep = params.mulstep
        self.step = params.step

#Ottimo test e ottimo design del controller. Riusciamo a fare un test con dati presi da qualche dataseta di latenza?
# tipo da questo sito: https://www.caida.org/data/ 
# oppure dai benchmark usati da facebook qui: https://code.facebook.com/posts/321654407970003/real-world-web-application-benchmarking/

if __name__=='__main__':
    inQueue = q.Queue()
    outQueue = q.Queue()

    minimum = 80
    maximum = 100
    step = 10
    substep = 1
    tolerance = 0.05
    mulstep = 5
    initValue = 50

    BangBangParams = namedtuple('params', ['min', 'max', 'step', 'substep'])
    TestBangBangParams = namedtuple('params', ['mulstep','step'])

    bang_bang = d.BangBang(inQueue, outQueue, BangBangParams(minimum, maximum, step, substep), tolerance)
    test_bang_bang = BangBangRandomTest(outQueue,inQueue,TestBangBangParams(mulstep,step))
    bang_bang.name = 'Controller'
    test_bang_bang.name = 'Tester'

    inQueue.put(initValue)

    test_bang_bang.start()
    bang_bang.start()

    time.sleep(5)

    test_bang_bang.stop()
    bang_bang.stop()

    test_bang_bang.join()
    bang_bang.join()

    logging.info('stopped correctly')
