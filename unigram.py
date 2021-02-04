import collections
import math

class Unigram:
    """A unigram language model.

    data: a list of lists of symbols. They should not contain `<EOS>`;
          the `<EOS>` symbol is automatically appended during
          training.
    """
    
    def __init__(self, data):
        self.count = collections.Counter()
        self.total = 0
        for line in data:
            for a in list(line) + ['<EOS>']:
                self.count[a] += 1
                self.total += 1

    def start(self):
        """Return the language model's start state. (A unigram model doesn't
        have state, so it's just `None`."""
        
        return None

    def read(self, q, a):
        """Return the state that the model would be in if it's in state `q`
        and reads symbol `a`. (Again, a unigram model doesn't have state, so
        this just returns `None`.)"""
        
        return None

    def logprob(self, q, a):
        """Return the log-probability of `a` when the model is in state `q`."""
        return math.log(self.count[a]/self.total)

    def best(self, q):
        """Return the symbol with highest probability when the model is in 
        state `q`."""
        return max(self.count, key=self.count.get)
