from threading import Thread

import time

import decide_bangbang as d
import queue as q
from collections import namedtuple
import logging
import random

logging.basicConfig(level=logging.INFO)

class TestBench(Thread):
    def __init__(self, timeout, mulstep):
        super().__init__()
        inQueue.put(50)
        self.stopped=False
        self.timeout = timeout
        self.mulstep = mulstep

    def stop(self):
        self.stopped=True

    def run(self):
        super().run()
        while not self.stopped:
            try:
                out=outQueue.get(timeout=self.timeout)
                inQueue.put(out+random.randint(-1*self.mulstep*step if out-self.mulstep*step>=0 else 0, self.mulstep*step*2))
            except q.Empty:
                return

inQueue = q.Queue()
outQueue = q.Queue()

minimum = 80
maximum = 100
step = 10
substep = 1
tolerance = 0.05
BangBangParams = namedtuple('params', ['min', 'max', 'step', 'substep'])

bang_bang = d.BangBang(inQueue, outQueue, BangBangParams(minimum, maximum, step, substep), tolerance)
testBench=TestBench(timeout=5, mulstep=5)

testBench.start()
bang_bang.start()

time.sleep(5)

testBench.stop()
bang_bang.stop()

testBench.join()
bang_bang.join()

logging.info('stopped correctly')
