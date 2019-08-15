from nltk.corpus import wordnet
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import re
from builtins import any as b_any

#ignoredWords = ['the', 'a', 'at']

#define the noun that we have that already exists
meantWords = {}
partsOfInterest = ['VERB', 'NOUN']
#Define the input command
#inputCommand = "Find the objective at the point with the target"
#inputCommand = "There are no limits on airspeed or altitude"
#inputCommand = "Bring me six green peppers from Meijer"
#inputCommand = "The first place is LVN.  It is a target.  The airspeed constraint is 200 and the altitude limit is 1500.  The effective radius is 2.5"
#inputCommand = "The first waypoint is LVN.  It is a target.  The airspeed restriction is 200 and the altitude restriction is 1500.  The effective radius is 2.5"
#inputCommand = "What is our current airspeed?"
#inputCommand = "Go to the next location"
#inputCommand = "Go faster"
inputCommand = input("Please enter a command\n")
inputCommand = inputCommand.lower()
#Tokenize the input command
wordList = word_tokenize(inputCommand)
checkWordList = {}

#PoSTag word list and get anchor words and important words to check back
checkWordList, anchorWords, verbFound = PoSTag(partsOfInterest, wordList)

#if(verbFound == False):
for word in checkWordList:
    anchorsFound = findAnchors(word)
    for anchor in anchorsFound:
        #print(anchor)
        if anchor not in anchorWords:
            anchorWords[anchor] = []
'''else:
    nounAnchorNodeValues, verbAnchorNodeValues = findPoSAnchors(checkWordList)
    for anchor in nounAnchorNodeValues:
        if anchor not in anchorWords:
            anchorWords[anchor] = []
    for anchor, originalWord in verbAnchorNodeValues:
        if anchor not in anchorWords:
            anchorWords[anchor] = []
print (anchorWords)'''

#Get syno/hyper/hyponyms and derivationally related forms
synonyms, hypernyms, hyponyms, deriv = getNyms(anchorWords, checkWordList)

#Iterate through all targetWord key-value pairs
#for targetWord in anchorWords:
for anchorWord in anchorWords:
    endSearch = False
    #print(anchorWord)
    #print(anchorWords[anchorWord])
    for originalWord in anchorWords[anchorWord]:
        if(endSearch == False):
            #Ignore if the found word is the target word itself
            if(originalWord != anchorWord):
                answered = False
                #Check if one of the found words is correct
                answer = input("When you said " + originalWord + ", did you mean " + anchorWord + "?\n")
                while(answered == False):
                    if(answer == 'yes'):
                        answered = True
                        endSearch = True
                        meantWords[originalWord] = anchorWord
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

    
#ADDED
'''verbObjects = {}
if (verbFound == True):
    
    for word in meantWords:
        meantWord = meantWords[word]
        checkWordList, anchorWords, verbFound = PoSTag(partsOfInterest, word_tokenize(meantWord))
        if(checkWordList[meantWord] == 'VERB'):
             #Get list of nodes from graph
            nodeList =  testGraph.nodes.data()
            #iterate through nodes
            for node, values in nodeList:
                #Get the value of each node
                currentNodeValue = values['value']
                #If the word we are looking for is in a node's value
                if(meantWord in currentNodeValue):
                    #Get the node's neighbors
                    neighborNodes = list(networkx.all_neighbors(testGraph, node))
                    #for each neighbor, append its value to the anchor node values
                    for neighbor in neighborNodes:
                        neighborNodeValue = testGraph.node[neighbor]['value']
                        verbObjects.update({meantWord: neighborNodeValue.lower()})
print (verbObjects)'''

#Replace the initial words with the found words
for index, word in enumerate(meantInput):
    for meantWordKey, meantWordValue in meantWords.items():
        #print(word, meantWordKey, meantWordValue)
        if(word == meantWordKey):
            meantInput[index] = meantWordValue

#Put together a potential string that means the same and output it for confirmation
meantInputString = ' '.join(meantInput)
#if(verbFound == False):
print("You gave the following information: \n")
print(inputCommand)
print("Is this equivalent to the following?\n")
print(meantInputString)

'''
#VERY SHAKY WAY TO RECONSTRUCT SENTENCE
if(verbFound == True):
    print("You gave the following instruction: \n")
    print(inputCommand)
    verbAction, verbObject = verbObjects.popitem()
    print("Were you requesting for the " + verbObject + " to " + meantInputString + "?\n")
    print(meantInputString)
'''
    
#correctSolution = input("Please answer yes or no\n")