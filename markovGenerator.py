import json
from random import choice
import pathlib

def parseJsonToNGram(data, n):
    transitionTables = {}
    currentParticipants = []
    for participant in data['participants']:
        person = participant['name']
        currentParticipants.append(person)
        transitionTables[person] = {}
    for message in data['messages']:
        person = message['sender_name']
        # Ignore message senders who aren't current participants
        if person in currentParticipants and 'content' in message and len(message['content']) > n:
            content = message['content'].split(" ")
            for i in range(n, len(content)):
                if n > 1:
                    key = tuple([content[i - k] for k in range(n, 0, -1)])
                else:
                    # Instead of a tuple of strings, casting a single tuple to string would yield a char tuple
                    key = content[i-1]
                if key in transitionTables[person]:
                    transitionTables[person][key].append(content[i])
                else:
                    transitionTables[person][key] = [content[i]]
    return transitionTables


def generateChain(transitionTables, data, n):
    for participant in data['participants']:
        person = participant['name']
        print(person)
        start = choice(list(transitionTables[person].keys()))
        words = [start[i] for i in range(0, n)]
        words.append(choice(transitionTables[person][start]))
        # For speed, build a list of strings and ' '.join them
        res = []
        res.extend(words)
        t = 0
        f = 0
        for count in range(0, 100):
            if n > 1:
                key = tuple(words[1:])
            else:
                key = words[1]
            if key in transitionTables[person]:
                for i in range(0, len(words) - 1):
                    words[i] = words[i+1]
                words[-1] = choice(transitionTables[person][key])
                res.append(words[-1])
            # If key not found, forget our context and start talking about something else.
            else:
                key = choice(list(transitionTables[person].keys()))
                if n > 1:
                    words = [key[i] for i in range(0, n)]
                else:
                    words = [key]
                words.append(choice(transitionTables[person][key]))
                res.extend(words)
            count += 1
        resStr = ' '.join(res)
        filename = participant['name'] + ".txt"
        pathlib.Path(filename).write_text(resStr, encoding="utf8")
        print(resStr)

def main():
    with open('message.json') as messageJSON:
        data = json.loads(messageJSON.read())
    tt = parseJsonToNGram(data, 2)
    generateChain(tt, data, 2)


main()
