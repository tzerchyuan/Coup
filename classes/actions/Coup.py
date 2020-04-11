from .Action import Action

class Coup(Action):
    def __init__(self, target : int = None, card_id : int = None):
        super().__init__(kill=True, target=target, kill_card_id=card_id, cost=7)

    def ready(self):
        return self.kill_card_id is not None and self.target is not None
