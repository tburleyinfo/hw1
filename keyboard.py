import random
import tkinter as tk

class Uniform(object):
    """Barebones example of a language model class."""

    def __init__(self):
        self.vocab = set()

    def train(self, filename):
        """Train the model on a text file."""
        for line in open(filename):
            for w in line:
                self.vocab.add(w)

    # The following two methods make the model work like a finite
    # automaton.

    def start(self):
        """Resets the state."""
        pass

    def read(self, w):
        """Reads in character w, updating the state."""
        pass

    # The following two methods add probabilities to the finite automaton.

    def prob(self, w):
        """Returns the probability of the next character being w given the
        current state."""
        return 1/(len(self.vocab)+1) # +1 for <unk>

    def probs(self):
        """Returns a dict mapping from all characters in the vocabulary to the
probabilities of each character."""
        return {w: self.prob(w) for w in self.vocab}

class Application(tk.Frame):
    def __init__(self, model, master=None):
        self.model = model

        tk.Frame.__init__(self, master)
        self.pack()

        self.INPUT = tk.Text(self)
        self.INPUT.pack()

        self.chars = ['qwertyuiop',
                      'asdfghjkl',
                      'zxcvbnm,.',
                      ' ']

        self.KEYS = tk.Frame(self)
        for row in self.chars:
            r = tk.Frame(self.KEYS)
            for w in row:
                # trick to make button sized in pixels
                f = tk.Frame(r, height=32)
                b = tk.Button(f, text=w, command=lambda w=w: self.press(w))
                b.pack(fill=tk.BOTH, expand=1)
                f.pack(side=tk.LEFT)
                f.pack_propagate(False)
            r.pack()
        self.KEYS.pack()

        self.TOOLBAR = tk.Frame()

        self.BEST = tk.Button(self.TOOLBAR, text='Best', command=self.best, 
                              repeatdelay=500, repeatinterval=1)
        self.BEST.pack(side=tk.LEFT)

        self.WORST = tk.Button(self.TOOLBAR, text='Worst', command=self.worst, 
                               repeatdelay=500, repeatinterval=1)
        self.WORST.pack(side=tk.LEFT)

        self.RANDOM = tk.Button(self.TOOLBAR, text='Random', command=self.random, 
                                repeatdelay=500, repeatinterval=1)
        self.RANDOM.pack(side=tk.LEFT)

        self.QUIT = tk.Button(self.TOOLBAR, text='Quit', command=self.quit)
        self.QUIT.pack(side=tk.LEFT)

        self.TOOLBAR.pack()

        self.update()
        self.resize_keys()

    def resize_keys(self):
        for bs, ws in zip(self.KEYS.winfo_children(), self.chars):
            wds = [150*self.model.prob(w)+15 for w in ws]
            wds = [int(wd+0.5) for wd in wds]

            for b, wd in zip(bs.winfo_children(), wds):
                b.config(width=wd)

    def press(self, w):
        self.INPUT.insert(tk.END, w)
        self.INPUT.see(tk.END)
        self.model.read(w)
        self.resize_keys()

    def best(self):
        _, w = max((p, w) for (w, p) in self.model.probs().items())
        self.press(w)

    def worst(self):
        _, w = min((p, w) for (w, p) in self.model.probs().items())
        self.press(w)

    def random(self):
        s = 0.
        r = random.random()
        p = self.model.probs()
        for w in p:
            s += p[w]
            if s > r:
                break
        self.press(w)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(dest='train')
    args = parser.parse_args()

    ##### Replace this line with an instantiation of your model #####
    m = Uniform()
    m.train(args.train)
    m.start()

    root = tk.Tk()
    app = Application(m, master=root)
    app.mainloop()
    root.destroy()
