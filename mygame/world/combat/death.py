from evennia.utils import interactive
class Death:
    @interactive
    def __init__(self,target):
        self.target = target
        self.target.location.msg_contents(str(self.target)+ " has lost the will to live")
        yield 3
        self.target.msg("Re-Spawning you somewhere cozy")
        yield 2
        self.target.msg("Try to stay alive.")
        yield 2
        self.target.move_to(self.target.home, quiet = True)
        self.target.db.health = self.target.db.max_health
