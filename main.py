def parseJson():
    import json
    from random import choice
    import pathlib
    with open('message.json') as messageJSON:
        data = json.loads(messageJSON.read())
    transitionTables = {}
    for participant in data['participants']:
        person = participant['name']
        transitionTables[person] = {}
        for message in data['messages']:
            if message['sender_name'] == person:
                if 'content' in message and len(message['content']) > 2:
                    content = message['content'].split(" ")
                    for i in range(2, len(content)):
                        key = content[i-2], content[i-1]
                        if key in transitionTables[person]:
                            transitionTables[person][key].append(content[i])
                        else:
                            transitionTables[person][key] = [content[i]]
                # Avoid future participants checking if they sent a message we already know another sent
                data['messages'].remove(message)
        print(person)
        start = choice(list(transitionTables[person].keys()))
        word1 = start[0]
        word2 = start[1]
        word3 = choice(transitionTables[person][start])
        res = ""
        res += (word1 + " " + word2 + " " + word3 + " ")
        i = 0
        punctuation = ['.', '!', '?']
        while i < 50 and res[-1] not in punctuation:
        # for i in range(0, 100):
            key = word2, word3
            if key in transitionTables[person]:
                word1 = word2
                word2 = word3
                word3 = choice(transitionTables[person][word1, word2])
                res += (word3 + " ")
            else:
                key = choice(list(transitionTables[person].keys()))
                word1 = key[0]
                word2 = key[1]
                word3 = choice(transitionTables[person][key])
                res += (word1 + " " + word2 + " " + word3 + " ")
            i += 1
        filename = participant['name'] + ".txt"
        pathlib.Path(filename).write_text(res, encoding="utf8")
        print(res)
parseJson()