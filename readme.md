# Facebook Messenger Fake Quote Generator 

*markovGenerator.py*

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
* ~~Use Naive Bayes to take in a quote and message.json, output who is most likely to say that quote~~

# Facebook Messenger Classifier

*classifier.py*

Features:
* Predict most likely speaker of a message based off their previous messages 
* Naive Bayes implementation using FB messenger chats
* Laplace Smoothing to handle unseen words
* Returns result weighted by prior probability as well as unweighted (rationality explained below)

To use: same as above.

Output: The most likely speaker of a given quote based off the unweighted score, the most likely speaker based off the weighted score, and the corresponding scores printed to console.
The program will then prompt for another quote to classify until the user types "QUIT" or kills the process.

We may or may not want to weight prior probabilities (by number of messages a participant has sent divided by the total 
number of messages as opposed to saying prior probability is 1/number of participants) depending on the nature 
of the message. If one person posts more frequently in the groupchat,
a truly randomly selected message from the test set IS more likely to be them. But if we're just submitting quotes
that humans arbitrarily picked, we may want all prior probabilities to be weighted equally. However, if you do not
weight the result and the test set includes universally unseen words, it may be unfairly biased towards someone who has
spoken fewer words. After all, if you've never said a word and it has "one" occurrence (laplace smoothing) out of 100,000
words you've said compared to "one" occurrence out of 5,000 words someone else has said, it would rate the person
who has spoken less as more likely to say it. Thus, we will output weighted (including prior probability) and
unweighted results. Ideally, sending more messages means sending more words, and thus the higher count of words
in that class resulting in a lower probability for a given word will balance out the higher probability to be 
accurate but people have different tendencies in how they break up messages (breaking a paragraph into multiple vs
one for example) so someone who sends a higher than average number of messages but fewer than average words would 
likely be seen as the most likely speaker for any brand new words.

As a default, the weighted result should be the preferred, but in some contexts the unweighted may be taken into consideration.

To-do:
* Potentially add results from more classifiers.

