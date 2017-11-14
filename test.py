import time, multiprocessing, logging, random
import decide_bangbang as d
from collections import namedtuple

logging.basicConfig(level=logging.NOTSET, format='%(processName)s : %(message)s')


class BangBangRandomTest(d.Decide):
    def decide(self, out):
        return out + random.randint(-1 * self.mulstep * self.step
                                    if out - self.mulstep * self.step >= 0
                                    else 0,
                                    2 * self.mulstep * self.step
                                    if out + 2 * self.mulstep * self.step
                                    else 150 - out)

    def __init__(self, inQueue, outQueue, params):
        super().__init__(inQueue, outQueue, params, 0, 1)
        self.mulstep = params.mulstep
        self.step = params.step


# Ottimo test e ottimo design del controller. Riusciamo a fare un test con dati presi da qualche dataseta di latenza?
# tipo da questo sito: https://www.caida.org/data/ 
# oppure dai benchmark usati da facebook qui: https://code.facebook.com/posts/321654407970003/real-world-web-application-benchmarking/

if __name__ == '__main__':
    inQueue = multiprocessing.Queue()
    outQueue = multiprocessing.Queue()

    minimum = 80
    maximum = 100
    step = 10
    substep = 1
    tolerance = 0.05
    mulstep = 5
    initValue = 50
    timeout = 1

    BangBangParams = namedtuple('params', ['min', 'max', 'step', 'substep'])
    TestBangBangParams = namedtuple('params', ['mulstep', 'step'])

    bang_bang = d.BangBang(inQueue, outQueue, BangBangParams(minimum, maximum, step, substep), tolerance, timeout)
    test_bang_bang = BangBangRandomTest(outQueue, inQueue, TestBangBangParams(mulstep, step))
    bang_bang.name = 'Controller'
    test_bang_bang.name = 'Tester'

    inQueue.put(initValue)

    test_bang_bang.start()
    bang_bang.start()

    time.sleep(5)

    test_bang_bang.terminate()
    bang_bang.terminate()

    test_bang_bang.join()
    bang_bang.join()
    logging.info('stopped correctly')
