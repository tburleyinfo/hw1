#DataLoader
import argparse
import unigram

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

#Train Model
m = unigram.Unigram(train)
q = m.start()

total = 0
correct = 0


#Read Dev Data into the model.
for line in dev:
    for index, a in enumerate(line):  
        predicted_symbol = m.best(q)
        if index != len(line) - 1:
            gold_symbol = line[index + 1]
            if predicted_symbol == gold_symbol:
                correct += 1
            total+=1
        q = m.read(q, a)

gold = a 
predicted = m.best(q)

acc = correct/total
print(acc*100, "%")
        

print("This is the most predicted character: ", m.best(q))








