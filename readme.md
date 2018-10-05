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
* Returns result weighted by prior probability as well as unweighted

To use: same as above.

Output: The most likely speaker of a given quote based off the unweighted score, the most likely speaker based off the weighted score, and the corresponding scores printed to console.
The program will then prompt for another quote to classify until the user types "QUIT" or kills the process.
The inclusion of weighted and unweighted scores is because if you randomly select a facebook message from outside the training set, the prior probability of the 
likelihood of a particular person speaking should be factored in. However, there are circumstances where we may want to guess the speaker without factoring in
the amount of time someone spends speaking (seeing who would be most likely to say a quote that was not actually said, humans selecting their favorite quotes someone has said, etc)

To-do:
* Potentially add results from more classifiers.

