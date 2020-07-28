"""An Agent that always takes Tax unless forced to Coup, and that never Blocks or Challenges."""

if __name__ == "__main__":
    from utils.game import *
    from utils.responses import *
    from utils.network import *
    from Agent import Agent
else:
    from .utils.game import *
    from .utils.responses import *
    from .utils.network import *
    from .Agent import Agent

class TaxAgent(Agent):
    def __init__(self, verbose=False):
        self.verbose = verbose
        pass

    def decide_action(self, options):
        if can_foreign_aid(options):
            return foreign_aid()
        else:
            targets = coup_targets(options)
            if targets:
                return coup(targets[0])
            # Should always be able to Tax unless we are forced to Coup
            assert False

    def decide_reaction(self, options):
        return decline()

    def decide_card(self, options):
        return options[0]


if __name__ == "__main__":
    start(TaxAgent())

