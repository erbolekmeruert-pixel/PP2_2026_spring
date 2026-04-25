import datetime

class MickeyClockLogic:
    """
    Handles time-to-angle conversion for the clock hands.
    """
    def get_angles(self):
        now = datetime.datetime.now()
        
    
        sec_angle = now.second * 6
        
        min_angle = now.minute * 6 + now.second * 0.1
        
        return sec_angle, min_angle