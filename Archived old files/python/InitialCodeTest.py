from nltk.corpus import wordnet, verbnet
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import re
#ignoredWords = ['the', 'a', 'at']

#define the noun that we have that already exists
targetWords = {"target": [], "locate": [], "unrelated": []}
meantWords = {}
#targetWords = {"waypoint": 0, "restriction": 0}
partsOfInterest = ['VERB', 'NOUN', 'ADV']
#Define the input command
#inputCommand = "Find the objective at the point with the target"
#inputCommand = "Bring me six green peppers from Meijer"
#inputCommand = "The first place is LVN.  It is a target.  The airspeed constraint is 200 and the altitude limit is 1500.  The effective radius is 2.5"
#inputCommand = "The first waypoint is LVN.  It is a target.  The airspeed restriction is 200 and the altitude restriction is 1500.  The effective radius is 2.5"
#inputCommand = "What is our current airspeed?"
#inputCommand = "go faster"
inputCommand = input("Please enter a command\n")
inputCommand = inputCommand.lower()
#Tokenize the input command
wordList = word_tokenize(inputCommand)
checkWordList = {}

#Tag each word with a part of speech (using the universal tagging system for more general tags)
tagged = pos_tag(wordList, tagset='universal', lang='eng')
#tagged = pos_tag(wordList)
#Go through each word and find if it's a part of speech we are interested in
for tagPair in tagged:
    #get word and tag
    word = tagPair[0]
    tag = tagPair[1]
    #If interesting part of speech, then append to list of words to check
    if tag in set(partsOfInterest):
        checkWordList.update({word: tag})
    #print (word)
    #print(tag)


#Iterate through all words to check
for currentWord in checkWordList:
    synonyms = []
    hypernyms = []
    hyponyms = []
    pertainyms = []
    deriv = []
    print(currentWord)
    print(checkWordList[currentWord])
    #Get synsets of current word to check
    testWord = wordnet.synsets(currentWord)
    #for each synset (meaning)
    for syn in testWord:
        #Get Hypernyms
        if(len(syn.hypernyms()) > 0):
            currentHypernyms = syn.hypernyms()
            for hyperSyn in currentHypernyms:
                for lemma in hyperSyn.lemmas():
                    #if(lemma.name() != currentWord):
                    hypernyms.append(lemma.name())
                #hypernyms.append(hyperSyn.lemma_names())
        #Get Hyponyms
        if(len(syn.hyponyms()) > 0):
            currentHyponyms = syn.hyponyms()
            for hypoSyn in currentHyponyms:
                for lemma in hypoSyn.lemmas():
                    #if(lemma.name() != currentWord):
                    hyponyms.append(lemma.name())
                #hypernyms.append(hyperSyn.lemma_names())
        #Get direct synonyms
        for lemma in syn.lemmas():
            #if(lemma.name() != currentWord):
            synonyms.append(lemma.name())
            for derivForm in lemma.derivationally_related_forms():
                if(derivForm.name() not in deriv):
                    deriv.append(derivForm.name())
            for pertain in lemma.pertainyms():
                if(pertain not in pertainyms):
                    pertainyms.append(pertain)
    print("SYNONYMS: ")
    print(set(synonyms))
    print('\n HYPERNYMS:')
    print(set(hypernyms))
    print('\n HYPONYMS:')
    print(set(hyponyms))
    print('\n DERIV:')
    print(set(deriv))
    print('\n PERTAIN:')
    print(set(pertainyms))
    #Check if any target words found in syno/hyper/hypo lists
    #If target word is found, increase the number of times found in the dictionary.
    for targetWord in targetWords:
        if targetWord in set(synonyms):
            targetWords[targetWord].append(currentWord)
        elif targetWord in set(hypernyms):
            targetWords[targetWord].append(currentWord)
        elif targetWord in set(hyponyms):
            targetWords[targetWord].append(currentWord)
    print('\n')
print(targetWords.items())

#Iterate through all targetWord key-value pairs
for targetWord in targetWords:
    endSearch = False
    #Iterate through all syno/hyper/hyponyms found and stored
    for foundWord in targetWords[targetWord]:
        if(endSearch == False):
            #Ignore if the found word is the target word itself
            if(foundWord != targetWord):
                answered = False
                #Check if one of the found words is correct
                answer = input("When you said " + targetWord + ", did you mean " + foundWord + "?\n")
                while(answered == False):
                    if(answer == 'yes'):
                        answered = True
                        endSearch = True
                        meantWords[targetWord] = foundWord
                    elif(answer == 'no'):
                        answered = True
                    else:
                        answer = input("Please answer yes or no\n")
                        answered = False

#Set up a list for the words which were replaced                        
print(meantWords.items())
meantInput = []
for word in wordList:
    meantInput.append(word)

#Replace the initial words with the found words
for index, word in enumerate(meantInput):
    for meantWordKey, meantWordValue in meantWords.items():
        if(word == meantWordValue):
            meantInput[index] = meantWordKey

#Put together a potential string that means the same and output it for confirmation
meantInputString = ' '.join(meantInput)
print("You gave the following input: \n")
print(inputCommand)
print("Is this equivalent to the following?\n")
print(meantInputString)
correctSolution = input("Please answer yes or no\n")