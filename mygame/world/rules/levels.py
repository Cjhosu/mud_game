

class XP:
    def  __init__(self,target, xp_val):
        self.xp_val = xp_val
        self.target = target
        self.add()
    def add(self):
        self.target.db.xp += self.xp_val
        pass
