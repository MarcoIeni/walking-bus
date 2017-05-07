from threading import Timer


class MyTimer:
    """
    It implements the concept of timer. It allows the expected operations like start, reset or know if it is expired.
    """
    def __init__(self, seconds, name):
        self.name = name
        self.seconds = seconds
        self.t = Timer(self.seconds, self.timeout)
        self.expired = False

    def reset(self):
        self.t.cancel()
        self.t = Timer(self.seconds, self.timeout)
        self.start()

    def timeout(self):
        self.expired = True
        self.t.cancel()
        print(self.name + " expired")

    def is_expired(self):
        return self.expired

    def start(self):
        self.t.start()

    def delete(self):
        self.t.cancel()
