import argparse
from ngramLocal import ngram

parser = argparse.ArgumentParser()
parser.add_argument(dest='train')
args = parser.parse_args()

train = []
dev= []


#Import Train
with open(args.train, "r") as f: 
    train = [list(line.rstrip()) for line in f]

#Import Dev
with open("data/dev", "r") as f: 
    dev = [list(line.rstrip("\n")) + ['<EOS>'] for line in f]

m = ngram(train)
q = m.start()

total = 0
correct = 0
i=0

#Read Dev Data into the model.
for line in dev:
    q = m.start()
    i = 0 
    for index, a in enumerate(line):  
        predicted_symbol = m.best(q)
        if index != len(line) - 1:
            gold_symbol = line[index + 1]
            if predicted_symbol == gold_symbol:
                correct += 1
            total+=1
        q = m.read(q, a)
        i+=1
        #print(i)
        print(q)

gold = a 
predicted = m.best(q)

acc = correct/total
print(acc*100, "%")