from threading import Thread
import queue as q
import logging


class Decide(Thread):
    def __init__(self, inQueue, outQueue, params, tolerance):
        super(Decide, self).__init__()
        # params will be a namedtuple
        self.params = params
        self.inQueue = inQueue  # type: q.Queue
        self.outQueue = outQueue  # type: q.Queue
        self.__stopped = False
        self.previousChoice = 100
        self.previousStatus = 0
        self.tolerance = tolerance

    def stop(self):
        self.__stopped=True;

    def decide(self, status):
        return 0

    def run(self):
        super().run()
        logging.info("Set params {}".format(self.params))
        while not self.__stopped:
            try:
                status = self.inQueue.get()
                choice = self.decide(status)
                self.previousStatus, self.previousChoice = status, choice

                logging.info('Received: {}, decided: {}'.format(status, choice))

                self.outQueue.put(choice)
            except q.Empty:
                break

class BangBang(Decide):

    def __init__(self, inQueue, outQueue, params, tolerance):
        super().__init__(inQueue, outQueue, params, tolerance)
        self.max = params.max
        self.min = params.min
        self.step = params.step
        self.substep = params.substep

    def decide(self, latency):
        if latency >= self.max:
            logging.info('over MAX')
            choice=100  # if system's latency greater than max allowed, give all the power
        elif self.max*(1-self.tolerance) <= latency < self.max:
            logging.info('near MAX latency, trying giving {}'.format(self.substep))
            choice=self.previousChoice+self.substep  # if latency near max try giving some more power
        elif self.min*(1+self.tolerance) <= latency < self.max*(1-self.tolerance):
            logging.info('trying to reduce power by substep {}'.format(self.substep))
            choice = self.previousChoice - self.substep  # if latency between toleranche from min  max, try powercapping
        else:  # if system's latency lower than lower bound try reducing the power step by step if possible
            logging.info('trying to reduce power by step {}'.format(self.step))
            choice = self.previousChoice - self.step
        return choice if 100 >= choice >= self.step else 100 if choice >= 100 else self.step


