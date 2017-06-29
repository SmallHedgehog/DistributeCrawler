# coding: utf-8

"""
管理线程状态的测试
"""

import Queue
import time
import threading

max_tasks = 10
Q = Queue.Queue()
Q.put_nowait("wait")

class Manager(object):
    """Manager thread's status test."""
    def __init__(self):
        super(Manager, self).__init__()
        self.threads = {}

    def Run(self):
        """Start several of threads"""
        def _run():
            while True:
                # print threading.currentThread()
                if self.threads[threading.currentThread().getName()][2] == 'stopping':
                    break
                time.sleep(2)

        def _print():
            # for key in self.threads.keys():
            #    print key, self.threads[key]
            for thread in threading.enumerate():
                print thread
            while True:
                command = raw_input('Command> ')
                if command == 'Thread-1':
                    self.threads[command][2] = 'stopping'
                    time.sleep(1)
                    # for key in self.threads.keys():
                    #    print key, self.threads[key]
                    for thread in threading.enumerate():
                        print thread
                    print "threading activeCount: ", threading.activeCount()
                elif command == 'add thread':
                    t = threading.Thread(target=_run)
                    self.threads[t.getName()] = [t.ident, t, 'running']
                    t.setDaemon(True)
                    t.start()
                    for thread in self.threads.keys():
                        print thread, self.threads[thread]

        for task in range(max_tasks):
            t = threading.Thread(target=_run)
            self.threads[t.getName()] = [t.ident, t, 'running']
            t.setDaemon(True)
            t.start()

        p = threading.Thread(target=_print)
        p.setDaemon(True)
        p.start()

        print "threading activeCount: ", threading.activeCount()

        Q.join()

if __name__ == '__main__':
    Manager().Run()
