from multiprocessing import Process
import logging, signal, queue


class Decide(Process):
    def __init__(self, inQueue, outQueue, params, tolerance, timeout):
        super(Decide, self).__init__()
        # params will be a namedtuple
        self.params = params
        self.inQueue = inQueue
        self.outQueue = outQueue
        self.__stopped = False
        self.previousChoice = 100
        self.previousStatus = 0
        self.tolerance = tolerance
        self.timeout = timeout
        signal.signal(signal.SIGTERM, self.handler)

    def handler(self, signum, frame):
        if signum == signal.SIGTERM:
            self.__stopped = True
            logging.info("received SIGTERM, will leave gracefully")

    def decide(self, status):
        pass

    def run(self):
        super().run()
        logging.info("Set params {}".format(self.params))
        while not self.__stopped:
            try:
                status = self.inQueue.get(timeout=self.timeout)
                choice = self.decide(status)
                self.previousStatus, self.previousChoice = status, choice

                logging.info('Received: {}, decided: {}'.format(status, choice))

                self.outQueue.put(choice)
            except queue.Empty:
                logging.info("queue is empty, will end")
                break

class BangBang(Decide):

    def __init__(self, inQueue, outQueue, params, tolerance, timeout):
        super().__init__(inQueue, outQueue, params, tolerance, timeout)
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
