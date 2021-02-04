import tty, sys, termios

def getchar():
    """Read in one character from stdin.
    http://code.activestate.com/recipes/134892/"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def getline(prompt=''):
    """Reads a line from stdin with text prediction and returns it,
    without the trailing newline. If the user presses Ctrl-D at the
    beginning of the line, raises EOFError.
    """
    
    print(prompt, end='', flush=True)
    states = [lm.start()]
    chars = []
    prediction = ''

    def erase():
        if len(prediction) > 0:
            print(' '*len(prediction) + f'\x1b[{len(prediction)}D', end='', flush=True)
    
    while True:
        
        # Make prediction
        erase()
        prediction = []
        q = states[-1]
        for i in range(20):
            c = lm.best(q)
            if c == '<EOS>':
                break
            prediction.append(c)
            q = lm.read(q, c)
        prediction = ''.join(prediction)
        
        # Print prediction
        if len(prediction) > 0:
            print('\x1b[7m' + prediction + f'\x1b[0m\x1b[{len(prediction)}D', end='', flush=True)

        # Read and process character
        c = getchar()
        if c == '\x03': # Ctrl-C
            erase()
            raise KeyboardInterrupt()
        elif c == '\x04': # Ctrl-D
            if len(chars) == 0:
                erase()
                print('')
                raise EOFError()
            else:
                print('\a', end='')
        elif c in ['\r', '\n']: # Return
            erase()
            print('', flush=True)
            break
        elif c in ['\x7f', '\b']: # Backspace
            if len(chars) == 0:
                print('\a', end='')
            else:
                erase()
                print(f'\x1b[1D', end='', flush=True)
                chars.pop()
                states.pop()
        else:
            print(c, end='', flush=True)
            chars.append(c)
            states.append(lm.read(states[-1], c))
    return ''.join(chars)

if __name__ == "__main__":
    import argparse
    import unigram

    parser = argparse.ArgumentParser()
    parser.add_argument(dest='train')
    args = parser.parse_args()

    data = [list(line.rstrip('\n')) for line in open(args.train)]

    ##### Replace this line with an instantiation of your model #####
    lm = unigram.Unigram(data)

    while True:
        try:
            line = getline('> ')
        except EOFError:
            break
