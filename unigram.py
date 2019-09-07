import fst

class Unigram(fst.FST):
    """A unigram language model.

    data: a list of lists of symbols. They should not contain `</s>`;
          the `</s>` symbol is automatically appended during
          training.
    """
    
    def __init__(self, data):
        super().__init__()
        
        # Our states are 0 and 1. In general, a state can be any hashable
        # object: for example, an int, a str, or a tuple.
        self.set_start(0)
        self.set_accept(1)

        # Create the transitions.
        for words in data:
            for a in words:
                self.add_transition(fst.Transition(0, a, a, 0))
        self.add_transition(fst.Transition(0, fst.STOP, fst.STOP, 1))

        # The FST automatically builds a dict of counts; convert them to
        # probabilities.
        self.probs = fst.estimate_joint(self.counts)

    def get_prob(self, t):
        return self.probs[t]
