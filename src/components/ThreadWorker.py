from PyQt6.QtCore import QRunnable, pyqtSlot

class ThreadWorker(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super(ThreadWorker, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.func(*self.args, **self.kwargs)