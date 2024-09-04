from PyQt6.QtCore import QRunnable, pyqtSlot as Slot
import time

class ThreadWorker(QRunnable):
    """
    Threaded objects that run asynchronously inside of the QThreadPool managed by the FSM.
    The thread workers expect a function to execute, a ConsoleLogger instance to log messages,
    and any additional arguments.
    """
    def __init__(self, func, logger, *args):
        super(ThreadWorker, self).__init__()
        self.func = func
        self.args = args
        self.command = func.__name__
        self.logger = logger

    @Slot()
    def run(self):
        timeStart = time.perf_counter()
        self.func(*self.args)
        timeEnd = time.perf_counter()
        timeElapsed = timeEnd - timeStart
        self.logger.info(f"Command [{self.command.upper()}] thread took {float(timeElapsed)} seconds.")