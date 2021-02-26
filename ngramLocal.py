import collections
import math

class ngram:
    """A unigram language model.

    data: a list of lists of symbols. They should not contain `<EOS>`;
          the `<EOS>` symbol is automatically appended during
          training.
    """
    
    def __init__(self, data):
        self.count = collections.Counter()
        self.total = 0
        for line in data:
            line = ["<BOS>", "<BOS>", "<BOS>", "<BOS>"] + list(line) + ['<EOS>']

            #Example: line = ["<BOS>", "<BOS>", "<BOS>", "<BOS>"] + ["T", "h", "e"] + ['<EOS>']
            for i in range(len(line)): 
                if i+3 < len(line): 
                    fourGram= (line[i], line[i+1], line[i+2], line[i+3])
                    self.count[fourGram] += 1
                if i+4 < len(line):
                    fiveGram= (line[i], line[i+1], line[i+2], line[i+3], line[i+3])
                    self.count[fiveGram] += 1


    def start(self):
        """Return the language model's start state. (A unigram model doesn't
        have state, so it's just `None`."""
        
        #Should return the first n-1 BOS+FIRST STRING(S) symbols. 
        return ("<BOS>", "<BOS>", "<BOS>", "<BOS>")

    def read(self, q, a):
        """Return the state that the model would be in if it's in state `q`
        and reads symbol `a`. (Again, a unigram model doesn't have state, so
        this just returns `None`.)"""
        
        return (q[1], q[2], q[3], a)

    #def smoothing(): 

    def logprob(self, q, a):
        """Return the log-probability of `a` when the model is in state `q`."""
        
        #prob(q, a) = count(q + a)/count(q)
        vocab = len(set(line for line in self.count))

        delta = .01
        prob = self.count[(q[0], q[1], q[2], q[3], a)]+delta/(vocab*delta)+self.count[q]
        return math.log(prob)


    def best(self, q, a):
        """Return the symbol with highest probability when the model is in 
        state `q`."""
        return max(self.count, key=self.count.get)
