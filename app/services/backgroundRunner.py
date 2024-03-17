import datetime

class BackgroundRunner:
    def __init__(self):
        self.value = 0
        self.start = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.task = None

    def kill_task(self):
        self.task.cancel()
