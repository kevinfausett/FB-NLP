Features: 
* Random quote generator for FB messenger chats
* Variable-length n-grams for use in markov chains
* Separate markov chain for every participant
* Fast parsing and generation

To use: go to https://www.facebook.com/settings?tab=your_facebook_information and download your messages.
Take the messages.json file you want to generate quotes from and place it in this repo.
Run main.py

Output: A random quote of at least 102 words will be generated for each participant in the chat and output to console and written to text files named after the participant.

You can change the length of the n-grams used as keys in the transition table. Just change the n argument in ParseJsonToNGram and generateChain. I find 1 to be gibberish, 2-3 to be good, and 4 to be too much direct quoting.

To-do:
* Implement fallback where if a sequence of words matching the current n-gram key, match against an n-1-gram key. e.g., if "tip the iceberg" doesn't match any keys, try "the iceberg", then "iceberg", and only resort to randomly selecting a new key when the last word's only matches are end of message.
* Use Naive Bayes to take in a quote and message.json, output who is most likely to say that quote