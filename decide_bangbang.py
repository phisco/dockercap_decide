from threading import Thread
import queue as q
import logging


class Decide(Thread):
    def __init__(self, inQueue, outQueue, func, params):
        # params will be a namedtuple
        self.params, self.func = params, func
        self.inQueue = inQueue  # type: q.Queue
        self.outQueue = outQueue  # type: q.Queue
        self.stopped = False
        self.previousChoice = 0
        self.previousStatus = 0

    def stop(self):
        self.stop = True

    def run(self):
        super().run()
        logging.info("Set params {}".format(self.params))
        while True:
            try:
                status = self.inQueue.get()
                choice = self.func(status, self.previousStatus, self.previousChoice)
                self.previousStatus, self.previousChoice = status, choice
                logging.info('Received: {}, decide: {}'.format(status, choice))
                self.outQueue.put(choice)
            except KeyboardInterrupt:
                break


class BangBang(Decide):
    def evaluate(self, latency, previousChoice, previousStatus):
        if latency >= self.max:
            return 100  # if system's latency greater than max allowed, give all the power
        elif latency >= self.min:
            return previousChoice  # if latency in allowed range, then continue like this
        else:  # if system's latency lower than lower bound try reducing the power step by step if possible
            choice = previousChoice - self.step
            return choice if choice >= self.step else self.step

    def __init__(self, inQueue, outQueue, params):
        super().__init__(inQueue, outQueue, self.evaluate, params)
        self.max = params.max
        self.min = params.min
        self.step = params.step
