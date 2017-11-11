import decide_bangbang as d
import queue as q
from collections import namedtuple

inQueue = q.Queue()
outQueue = q.Queue()

min = 80
max = 100
step=10
Params = namedtuple('params', ['min', 'max', 'step'])

bang_Bang=d.BangBang(inQueue, outQueue, Params(min,max,step))


bang_Bang.start()


