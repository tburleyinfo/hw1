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

    def predict(self, q):
        """Return the probablity distribution over the next symbol, as a dict
        whose keys are symbols (as strs) and whose values are log-probabilities
        (as floats)."""
        
        return {a:math.log(self.count[a]/self.total) for a in self.count}
    
