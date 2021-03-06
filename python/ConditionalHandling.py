import re
from Constants import *


class Conditional:
    def __init__(self, firstLine):
        self.firstLine = firstLine
        self.anonFirstLine = ''
        self.ifLines = []
        self.anonIfLines = []
        self.thenLines = []
        self.anonThenLines = []
        self.processed = False

    def addIfLine(self, newIfLine):
        self.ifLines.append(newIfLine)

    def addThenLine(self, newThenLine):
        self.thenLines.append(newThenLine)

    def addAnonIfLine(self, newAnonIfLine):
        self.anonIfLines.append(newAnonIfLine)

    def addAnonThenLine(self, newAnonThenLine):
        self.anonThenLines.append(newAnonThenLine)

    def replaceIfLines(self, newIfLines):
        self.ifLines = newIfLines

    def replaceAnonIfLines(self, newAnonIfLines):
        self.anonIfLines = newAnonIfLines

    def replaceFirstLine(self, newFirstLine):
        self.firstLine = newFirstLine

    def replaceAnonFirstLine(self, newAnonFirstLine):
        self.anonFirstLine = newAnonFirstLine

    def markProcessed(self):
        self.processed = True

    def pprint(self):
        print("firstLine: " + self.firstLine)
        print("anonfirstLine: " + self.anonFirstLine)
        print("IF: ")
        print(self.ifLines)
        print("THEN: ")
        print(self.thenLines)
        print("ANON IF: ")
        print(self.anonIfLines)
        print("ANON THEN: ")
        print(self.anonThenLines)
        print("PROCESSED: ")
        print(self.processed)


# Iterate through all reference variable/replacement number pairs and perform the substitution,
# then return the anonymized if line
def replaceReferenceVariables(ifLine, referenceVariables):
    for originalVariable, replacementNumber in referenceVariables.items():
        ifLine = re.sub(originalVariable, str(replacementNumber), ifLine)
    return ifLine


# Make the predicate reference variables irrelevant so that checking if an incoming instruction is equivalent to
# a conditional if is easier
def anonymizeIfs(conditionalToAnonymize):
    # Get list of reference variables and assign a number to each to track order,
    # then replace the variable with the number
    referenceVariables = {}
    currentVarNumber = 0
    anonymizedIfLines = []
    # assign a number to each if line's reference var in each conditional
    for ifLine in conditionalToAnonymize.ifLines:
        predicateContents = ifLine.split('(', 1)[1]
        predicateReferenceVariable = predicateContents.split(',', 1)[0]
        # Make sure not to overwrite something already found (for instance, modifiers have the same ref var)
        if predicateReferenceVariable not in referenceVariables.keys():
            referenceVariables.update({predicateReferenceVariable: currentVarNumber})
        currentVarNumber = currentVarNumber + 1
    # Now iterate through ifline's and replace each instance of a reference var with the associated number
    for ifLine in conditionalToAnonymize.ifLines:
        anonIfLine = replaceReferenceVariables(ifLine, referenceVariables)
        anonymizedIfLines.append(anonIfLine)
    conditionalToAnonymize.replaceAnonIfLines(anonymizedIfLines)
    conditionalToAnonymize.replaceAnonFirstLine(anonymizedIfLines[0])
    return conditionalToAnonymize


def getConditionals(DRSLines, categorizedDRSLines):
    # Need to make groups of which parts are related
    conditionalLines = {}
    for currentLineNumber in categorizedDRSLines.keys():
        # reset conditional flag
        # conditional = ''
        # Find out if the current line is part of a conditional or not
        # conditional = isLineConditional(index, symbolLines)
        # if the current line is part of an IF in a conditional
        if categorizedDRSLines.get(currentLineNumber) == CONST_IF_TAG:
            conditionalLines.update({currentLineNumber: CONST_IF_TAG})

        # if the current line is part of a THEN in a conditional
        if categorizedDRSLines.get(currentLineNumber) == CONST_THEN_TAG:
            conditionalLines.update({currentLineNumber: CONST_THEN_TAG})

    # iterate through and group each line in the same if/then, then match them up
    # TODO: Make the string split to remove the numbers at the end of the DRS instruction happen when it's first read in
    # so that it doesn't have to be done every time the instruction is touched in this or the switcher.
    # Also this method is clunky and temporary.  WIll need cleaned up.
    conditionalList = []
    conditionalLineIndexes = list(conditionalLines.keys())
    for conditionalIndex, conditionalLineNumber in enumerate(conditionalLineIndexes):
        # print(conditionalIndex, conditionalLineNumber)
        # If item is an if
        if conditionalLines[conditionalLineNumber] == CONST_IF_TAG:
            # Get index for line
            ifLineIndex = conditionalLineNumber
            # If first conditional line overall, or first line since a then
            if (conditionalIndex - 1) < 0 or \
                    conditionalLines[conditionalLineIndexes[conditionalIndex - 1]] == CONST_THEN_TAG:
                # Create new Conditional with the current line as the first line in the conditional
                currentConditional = Conditional(DRSLines[ifLineIndex].split(')-')[0] + ')')
            # Otherwise, just an if line
            currentConditional.addIfLine(DRSLines[ifLineIndex].split(')-')[0] + ')')
        # If item is a then
        elif conditionalLines[conditionalLineNumber] == CONST_THEN_TAG:
            thenLineIndex = conditionalLineNumber
            currentConditional.addThenLine(DRSLines[thenLineIndex].split(')-')[0] + ')')
            # If last line overall or last then before an if
            if ((conditionalIndex + 1) >= (len(conditionalLineIndexes))) or\
                    conditionalLines[conditionalLineIndexes[conditionalIndex + 1]] == CONST_IF_TAG:
                currentConditional = anonymizeIfs(currentConditional)
                conditionalList.append(currentConditional)
    return conditionalList


def splitAndRun(currentInstruction, predSwitcher):
    predicateSplit = currentInstruction.split('(', 1)
    predicateType = predicateSplit[0]
    predicateContents = predicateSplit[1]
    # Call appropriate handling function based on predicate type
    DRSGraph = predSwitcher.callFunction(predicateType, predicateContents)
    return DRSGraph


def runFullConditional(conditional, predSwitcher, DRSGraph, conditionalSets):
    checkPreparedThenLines = []
    newIfNodes = []
    newThenNodes = []
    instructionCountInMatchingIfBlock = 0

    # HACKY WAY to avoid second parentheses being appended due to not having a -x/y at the end
    for thenLine in conditional.thenLines:
        checkPreparedThenLines.append(thenLine + '-0/0')
    # Run each line of the if part of the conditional
    for ifLine in conditional.ifLines:
        # Append newly created node to array - should probably make this a separate  function
        predicateSplit = ifLine.split('(', 1)
        predicateContents = predicateSplit[1]
        ifLineNodeReference = predicateContents.split(',')[0]
        newIfNodes.append(ifLineNodeReference)
        # Run the current line
        DRSGraph = splitAndRun(ifLine, predSwitcher)
    # Run each then line in the then part of the conditional
    for index, thenLine in enumerate(checkPreparedThenLines):
        # Run the current then line if it isn't in a matching if block
        if instructionCountInMatchingIfBlock == 0:
            instructionCountInMatchingIfBlock, conditionalWithMatchingIfBlock = checkCurrentInstructionIf(
                checkPreparedThenLines, index, thenLine, conditionalSets)
            if instructionCountInMatchingIfBlock == 0:
                # Append newly created node to array - should probably make this a separate  function
                predicateSplit = thenLine.split('(', 1)
                predicateContents = predicateSplit[1]
                thenLineNodeReference = predicateContents.split(',')[0]
                newThenNodes.append(thenLineNodeReference)
                # Run the current line
                DRSGraph = splitAndRun(thenLine, predSwitcher)
            else:
                # Get the if block that matches the then block and add it to newThenNodes, in order to still
                # be able to put in the conditional trigger edges
                conditional.pprint()
                for i in range(instructionCountInMatchingIfBlock):
                    currentIfLine = conditionalWithMatchingIfBlock.ifLines[i]
                    predicateSplit = currentIfLine.split('(', 1)
                    predicateContents = predicateSplit[1]
                    currentIfLineNodeReference = predicateContents.split(',')[0]
                    print("**************************************************", currentIfLineNodeReference)
                    newThenNodes.append(currentIfLineNodeReference)
        else:
            instructionCountInMatchingIfBlock = instructionCountInMatchingIfBlock - 1
    # make lists contain only distinct members
    newIfNodes = list(set(newIfNodes))
    newThenNodes = list(set(newThenNodes))
    # Add edges between if and then nodes to signify which nodes get triggered by conditional
    print("IF", newIfNodes)
    print("THEN", newThenNodes)
    for ifNode in newIfNodes:
        for thenNode in newThenNodes:
            if ifNode is not None and thenNode is not None:
                DRSGraph.addConditionalTriggerEdges(ifNode, thenNode)
    conditional.markProcessed()
    return DRSGraph


# Potentially unused parameters removed
# , predSwitcher, DRSGraph)
def checkCurrentInstructionIf(DRSLines, currentInstructionIndex, currentInstruction, conditionalSets):
    # Format instruction in the format of the conditionalSet
    currentInstruction = currentInstruction.split(')-')[0] + ')'
    # ASSUMPTION: Should not see a first line of an if that references another reference variable from the conditional
    # Hacky way to get current instruction anonymized - should rework this
    initialConditionalCheck = Conditional(currentInstruction)
    initialConditionalCheck.addIfLine(currentInstruction)
    initialConditionalCheck = anonymizeIfs(initialConditionalCheck)
    conditionalWithMatchingIfBlock = None

    instructionCountInMatchingIfBlock = 0
    for conditional in conditionalSets:
        # In the case that the current line matches a conditional found
        if conditional.anonFirstLine == initialConditionalCheck.anonFirstLine:
            # Build out a "potential conditional" to see if it matches the conditional we expect
            conditionalIfLength = len(conditional.ifLines)
            potentialConditional = Conditional(currentInstruction)
            for i in range(conditionalIfLength):
                # add n if lines, where n is the number of if lines in the conditional being checked against
                potentialIfLine = DRSLines[currentInstructionIndex + i].split(')-')[0] + ')'
                potentialConditional.addIfLine(potentialIfLine)
            # Anonymize the lines from the instructions to see if they match the anonymized if
            # lines from the conditional
            potentialConditional = anonymizeIfs(potentialConditional)
            # compare instructions and conditional
            # potentialConditional.pprint()
            matchingLines = 0
            # Iterate through all the if lines in the conditional - if they match, add to the counter
            for i in range(conditionalIfLength):
                if conditional.anonIfLines[i] == potentialConditional.anonIfLines[i]:
                    matchingLines = matchingLines + 1
            # If the number of matching lines is the number of lines in the conditional, the conditional triggers
            if matchingLines == conditionalIfLength:
                # Return how many lines match and which conditional matches
                instructionCountInMatchingIfBlock = conditionalIfLength
                conditionalWithMatchingIfBlock = conditional
    # return DRSGraph
    return instructionCountInMatchingIfBlock, conditionalWithMatchingIfBlock

