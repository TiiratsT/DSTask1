from threading import Thread
import time

class nodeThread(Thread):

    def __init__(self, nodeID):
        Thread.__init__(self)
        self.Daemon = True
        self.running = True

        # Initial values
        self.successor = None
        self.nextSuccessor = None
        self.shortcuts = []
        self.nodeID = nodeID

        self.start()

    # To exit thread
    def setRunning(self, bool):
        self.running = bool
        print("Thread starting exiting")

    # Node waiting for input
    def run(self):
        while self.running:
            pass