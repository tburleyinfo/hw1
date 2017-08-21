import random
import tkinter as tk, tkinter.font as tkfont

class Application(tk.Frame):
    def __init__(self, model, master=None):
        self.model = model

        tk.Frame.__init__(self, master)
        self.pack(fill="both", expand=1)

        self.INPUT = tk.Text(self, height=1)
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
            for w in row:
                p[w] = self.model.prob(w)
        z = sum(p.values())

        for bs, ws in zip(self.KEYS.winfo_children(), self.chars):
            for b, w in zip(bs.winfo_children(), ws):
                wd = 500*p[w]/z+30
                wd = int(wd+0.5)
                b.config(width=wd)

    def press(self, w):
        self.INPUT.insert(tk.END, w)
        self.INPUT.see(tk.END)
        self.model.read(w)
        self.resize_keys()
        root.update()

    def best(self):
        _, w = max((self.model.prob(w), w) for row in self.chars for w in row)
        self.press(w)

    def worst(self):
        _, w = min((self.model.prob(w), w) for row in self.chars for w in row)
        self.press(w)

    def random(self):
        p = {}
        for row in self.chars:
            for w in row:
                p[w] = self.model.prob(w)
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

    parser = argparse.ArgumentParser()
    parser.add_argument(dest='train')
    args = parser.parse_args()

    ##### Replace this line with an instantiation of your model #####
    m = unigram.Unigram()
    
    m.train(args.train)
    m.start()

    root = tk.Tk()
    root.minsize(width=800, height=400)
    app = Application(m, master=root)
    app.mainloop()
    root.destroy()
