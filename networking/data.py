import datetime

class Data():
    msg_seq = 0
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.id = Data.msg_seq
        Data.msg_seq += 1
        self.time = datetime.datetime.now()

    def toString(self):
        return "[" + str(self.id) + "]@" + str(self.time) + " - " + self.message

