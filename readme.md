To use: go to https://www.facebook.com/settings?tab=your_facebook_information and download your messages.
Take the messages.json file you want to generate quotes from and place it in this repo.
Run main.py

Output: A random quote of at least 102 words will be generated for each participant in the chat and output to console and written to text files named after the participant.

You can change the length of the n-grams used as keys in the transition table. Just change the n argument in ParseJsonToNGram and generateChain. I find 1 to be gibberish, 2-3 to be good, and 4 to be too much direct quoting.