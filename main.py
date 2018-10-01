import json
from random import choice
import pathlib

def parseJsonToNGram(data, n):
    transitionTables = {}
    for participant in data['participants']:
        person = participant['name']
        transitionTables[person] = {}
        for message in data['messages']:
            if message['sender_name'] == person:
                if 'content' in message and len(message['content']) > n:
                    content = message['content'].split(" ")
                    for i in range(n, len(content)):
                        key = tuple([content[i - k] for k in range(n, 0, -1)])
                        # key = content[i - 2], content[i - 1]
                        if key in transitionTables[person]:
                            transitionTables[person][key].append(content[i])
                        else:
                            transitionTables[person][key] = [content[i]]
                # Avoid future participants checking if they sent a message we already know another sent
                data['messages'].remove(message)
        print(person + ' added!')
    return transitionTables


def generateChain(transitionTables, data):
    for participant in data['participants']:
        person = participant['name']
        print(person)
        start = choice(list(transitionTables[person].keys()))
        word1 = start[0]
        word2 = start[1]
        word3 = choice(transitionTables[person][start])
        res = []
        res.extend((word1, word2, word3))
        i = 0
        for i in range(0, 100):
            key = word2, word3
            if key in transitionTables[person]:
                word1 = word2
                word2 = word3
                word3 = choice(transitionTables[person][word1, word2])
                res.append(word3)
            else:
                key = choice(list(transitionTables[person].keys()))
                word1 = key[0]
                word2 = key[1]
                word3 = choice(transitionTables[person][key])
                res.extend((word1, word2, word3))
            i += 1
        resStr = ' '.join(res)
        filename = participant['name'] + ".txt"
        pathlib.Path(filename).write_text(resStr, encoding="utf8")
        print(resStr)

def main():
    with open('message.json') as messageJSON:
        data = json.loads(messageJSON.read())
    tt = parseJsonToNGram(data, 2)
    generateChain(tt, data)


main()
