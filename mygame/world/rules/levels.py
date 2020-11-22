class XP:
    def  __init__(self,target, xp_val):
        self.xp_val = xp_val
        self.target = target
        self.add()

    def add(self):
        target = self.target
        target.db.xp += self.xp_val
        self.check_level(target.db.xp ,target.db.next_level_xp)

    def check_level(self, xp, next_level_xp):
        target = self.target
        if target.db.xp >= target.db.next_level_xp:
            self.level_up()
            remainder = round(target.db.xp - target.db.next_level_xp)
            target.db.xp = remainder
            target.db.next_level_xp *= 1.5
            self.check_level(target.db.xp, target.db.next_level_xp)

    def level_up(self):
       self.target.db.level += 1
       self.target.location.msg_contents(str(self.target) +' has gained a level!')
