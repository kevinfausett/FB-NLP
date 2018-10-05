import json
import pathlib
from functools import reduce

def setupTable(data):
        table = {}
        # If we keep track of total message counts per user in the same dict we risk a collision
        counts = {}
        # Ignore messages from people we excommunicated
        currentParticipants = []
        table['totalcount'] = 0
        for participant in data['participants']:
            person = participant['name']
            currentParticipants.append(person)
            table[person] = {}
            counts[person] = 0
        for message in data['messages']:
            person = message['sender_name']
            if person in currentParticipants and 'content' in message:
                table['totalcount'] += 1
                counts[person] += 1
                content = message['content'].split(" ")
                for word in content:
                    if word in table[person]:
                        table[person][word] += 1
                    else:
                        table[person][word] = 1
        return table, counts, currentParticipants


def naiveBayes(table, counts, currentParticipants, text):
    words = text.split(" ")
    scores = {}
    participantCount = len(currentParticipants)
    for person in currentParticipants:
        scores[person] = []
    for word in words:
        temp = {}
        # laplace smoothing
        total = participantCount
        for person in currentParticipants:
            if word in table[person]:
                occurrences = table[person][word] + 1
            else:
                occurrences = 1
            temp[person] = occurrences
            total += occurrences
        for person in currentParticipants:
            probability = (temp[person] + 1) / total
            scores[person].append(probability)

    # We may or may not wan to weight prior probabilities. If one person posts more frequently in the groupchat,
    # a truly randomly selected message from the test set IS more likely to be them. But if we're just submitting quotes
    # that humans arbitrarily picked, we may want all prior probabilities to be weighed equally. We will output weighted
    # (including prior probability) and unweighted results.
    wtScores, unwtScores = {}, {}
    for person in currentParticipants:
        prior = counts[person] / table['totalcount']
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