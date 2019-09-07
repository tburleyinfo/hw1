import random
import tkinter as tk, tkinter.font as tkfont

class Application(tk.Frame):
    def __init__(self, model, master=None):
        self.model = model
        self.state = model.get_start()

        tk.Frame.__init__(self, master)
        self.pack(fill="both", expand=1)

        self.INPUT = tk.Text(self, height=1)
        self.INPUT.bind("<Key>", self.handle_key)
        self.INPUT.pack(fill="both", expand=1)

        self.chars = ['qwertyuiop',
                      'asdfghjkl',
                      'zxcvbnm,.',
                      ' ']

        self.KEYS = tk.Frame(self)
        for row in self.chars:
            r = tk.Frame(self.KEYS)
            for w in row:
                # trick to make button sized in pixels
                f = tk.Frame(r, height=30)
                b = tk.Button(f, text=w, command=lambda w=w: self.press(w))
                b.pack(fill=tk.BOTH, expand=1)
                b.pack()
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
        p = {}
        for row in self.chars:
            for a in row:
                ts = self.model.get_transitions(self.state, a)
                if len(ts) == 0:
                    pass
                elif len(ts) == 1:
                    [t] = ts
                    p[a] = self.model.get_prob(t)
                else:
                    raise ValueError("FST is not deterministic")
        z = sum(p.values())

        for bs, ws in zip(self.KEYS.winfo_children(), self.chars):
            for b, w in zip(bs.winfo_children(), ws):
                wd = 500*p.get(w,0)/z+30
                wd = int(wd+0.5)
                b.config(width=wd)
                
    def handle_key(self, event):
        self.press(event.char)
        return "break"

    def press(self, w):
        ts = self.model.get_transitions(self.state, w)
        if len(ts) == 0:
            # Automaton rejected keypress; do nothing
            pass
        elif len(ts) == 1:
            [t] = ts
            self.state = t.r
            self.INPUT.insert(tk.END, w)
            self.INPUT.see(tk.END)
            self.resize_keys()
            root.update()
        else:
            raise ValueError("FST is not deterministic")

    def probs(self):
        p = {}
        for row in self.chars:
            for w in row:
                ts = self.model.get_transitions(self.state, w)
                if len(ts) == 0:
                    p[w] = 0.
                elif len(ts) == 1:
                    [t] = ts
                    p[w] = self.model.get_prob(t)
                else:
                    raise ValueError("FST is not deterministic")
        return p
        
    def best(self):
        p = self.probs()
        w = max(p, key=p.get)
        self.press(w)

    def worst(self):
        p = self.probs()
        w = min(p, key=p.get)
        self.press(w)

    def random(self):
        p = self.probs()
        z = sum(p.values())

        s = 0.
        r = random.random()
        for w in p:
            s += p[w]/z
            if s > r:
                break
        self.press(w)

if __name__ == "__main__":
    import argparse
    import unigram
    #import ngram

    parser = argparse.ArgumentParser()
    parser.add_argument(dest='train')
    args = parser.parse_args()

    ##### Replace this line with an instantiation of your model #####
    m = unigram.Unigram(open(args.train))
    
    root = tk.Tk()
    root.minsize(width=800, height=400)
    app = Application(m, master=root)
    app.mainloop()
    root.destroy()
