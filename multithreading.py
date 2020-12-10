from PySide2.QtCore import QObject, QRunnable, Slot, Signal
import traceback, sys


class WorkerSignals(QObject):

    finished = Signal()
    error = Signal(tuple)
    progress = Signal(str)


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()  
        self.kwargs['progress_callback'] = self.signals.progress
   

    @Slot()
    def run(self):

        try:
            self.fn(*self.args, **self.kwargs)
        except:
            #traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.finished.emit() 
            