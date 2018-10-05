import json
import pathlib
from functools import reduce

def setupTable(data):
        table = {}
        # Per user word and message counts
        counts = {'word': {}, 'message': {}}
        # Ignore messages from people we excommunicated
        currentParticipants = []
        table['totalmessages'], table['vocabularylen'] = 0, 0
        for participant in data['participants']:
            person = participant['name']
            currentParticipants.append(person)
            table[person] = {}
            counts['word'][person], counts['message'][person] = 0, 0
        for message in data['messages']:
            person = message['sender_name']
            if person in currentParticipants and 'content' in message:
                table['totalmessages'] += 1
                counts['message'][person] += 1
                content = message['content'].split(" ")
                for word in content:
                    counts['word'][person] += 1
                    if word in table[person]:
                        table[person][word] += 1
                    else:
                        table[person][word] = 1
                        table['vocabularylen'] += 1
        return table, counts, currentParticipants


def naiveBayes(table, counts, currentParticipants, text):
    words = text.split(" ")
    scores = {}
    for person in currentParticipants:
        scores[person] = []
    for word in words:
        temp = {}
        # laplace smoothing
        v = table['vocabularylen']
        for person in currentParticipants:
            if word in table[person]:
                occurrences = table[person][word] + 1
            else:
                occurrences = 1

            scores[person].append(occurrences / (counts['word'][person] + v))

    wtScores, unwtScores = {}, {}
    for person in currentParticipants:
        prior = counts['message'][person] / table['totalmessages']
        totalUnwtProb = reduce((lambda x, y: x * y), scores[person])
        scores[person].append(prior)
        totalWtProb = reduce((lambda x, y: x * y), scores[person])
        unwtScores[person] = totalUnwtProb
        wtScores[person] = totalWtProb


    print("Max unweighted:")
    print(max(unwtScores.items(), key=lambda item: item[1]))
    print("Max weighted:")
    print(max(wtScores.items(), key=lambda item: item[1]))

def main():
    with open('message.json') as messageJSON:
        data = json.loads(messageJSON.read())
    table, counts, currentParticipants = setupTable(data)
    while True:
        print("\nType QUIT to quit\n")
        text = input("Quote to classify:\n")
        if text == "QUIT":
            return 0
        else:
            naiveBayes(table, counts, currentParticipants, text)

main()