import datetime

class Data():
    msg_seq = 0
    def __init__(self, player_no, bat_position, ball_position):
        super().__init__()
        self.player_no = player_no
        self.bat_position = bat_position
        self.ball_position = ball_position
        self.id = Data.msg_seq
        Data.msg_seq += 1
        self.time = datetime.datetime.now()

    def toString(self):
        try:
            return "[" + str(self.id) + "]@" + str(self.time) + " - " + str(self.player_no) + " : " + str(self.bat_position) + " : " + str(self.ball_position)
        except:
            return str(self.player_no)

    def isValid(self):
        return hasattr(self, "player_no")