
class Action:
    def __init__(self, **kwargs):
        self._properties = {
            "target": None,
            "steal": False,
            "kill": False, 
            "kill_card_id": None,
            "actor": None,  # what card we are claiming, e.g. Duke for Tax
            "cost": None,
            "blockable": False,
            "blockable_by": None
        }
        
        for arg in kwargs:
            self._properties[arg] = kwargs[arg]

    def get_property(self, prop : str):
        return self._properties[prop]

    def set_property(self, prop : str, value):
        self._properties[prop] = value

    def ready(self) -> bool:
        return True
