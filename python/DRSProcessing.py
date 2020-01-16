import networkx

from nltk.corpus import wordnet
import requests
import json

from GraphGeneration import *
from ConditionalHandling import *
from LineCategorization import *


class predicateSwitcher(object):

    def __init__(self):
        self.graphNumber = 0
        self.DRSGraph = ItemGraph(None)

    # Method to call the appropriate function based on the argument passed in
    def callFunction(self, predicateType, predicateContents):
        # Get the name of the method
        methodName = 'predicate_' + str(predicateType)
        # Get the method itself
        method = getattr(self, methodName, lambda: "Unknown predicate")
        # Call the method and return its output
        method(predicateContents)
        return self.DRSGraph

    def updateDRSGraph(self, newDRSGraph):
        self.DRSGraph = newDRSGraph

    # For object() predicates SHOULD CHECK IF OBJECT WITH GIVEN NAME ALREADY EXISTS!!!  IF SO, FIGURE OUT WHAT ARE
    # THE CONDITIONS FOR THAT TO OCCUR
    def predicate_object(self, predicateContents):
        # print(predicateContents)
        # Break up elements of object line into variables
        predicateComponents = predicateContents.split(',')
        objReferenceVariable = predicateComponents[0]
        objName = predicateComponents[1]
        # FOLLOWING ONES PROBABLY UNUSED BUT LEAVING COMMENTED OUT SO I HAVE ACCESS EASILY
        # objClass = predicateComponents[2]
        # objUnit = predicateComponents[3]
        # objOperator = predicateComponents[4]
        # objCount = predicateComponents[5].split(')')[0]
        if self.DRSGraph.FindItemWithValue(objReferenceVariable) is None:
            # Apply appropriate variables to ItemGraph
            objectGraph = ItemGraph(self.graphNumber)
            objectGraph.appendItemValue(objReferenceVariable)
            objectGraph.appendItemRole(objName)
            # Increase the graph number for auto-generation of names
            self.graphNumber = self.graphNumber + 1
            # If a main graph already exists, then add the new graph in to it
            if self.DRSGraph.graph is not None:
                # DRSGraph.graph = networkx.algorithms.operators.binary.union(DRSGraph.graph, objectGraph.graph)
                self.DRSGraph.graph = networkx.algorithms.operators.binary.compose(self.DRSGraph.graph,
                                                                                   objectGraph.graph)
            # if no main graph exists, this is the main graph
            else:
                self.DRSGraph.graph = objectGraph.graph
            return True
        else:
            return False

    # For predicate() predicates
    # HOW TO HANDLE SENTENCE SUB-ORDINATION?
    def predicate_predicate(self, predicateContents):
        # Intransitive verbs: (predName, verb, subjectRef)
        # - The SubjectRef Verbed (the man laughed, the target appears)
        # Transitive verbs: (predName, verb, subjectRef, dirObjRef)
        # - The Subjectref Verbed the dirObjRef (the task A has a group of objects H,
        # the subject L remembers the letter I)
        # Ditransitive verbs: (predName, verb, subjRef, dirObjRef, indirObjRef)
        # - The SubjectRef verbed the DirObjRef to the indirObjRef (The professor (S) gave
        # the paper (D) to the student (I))
        # Break up the predicate
        predicateComponents = predicateContents.split(',')
        numberOfComponents = len(predicateComponents)
        # Always have first three components, so only special cases are transitive/ditransitive
        predReferenceVariable = predicateComponents[0]
        predVerb = predicateComponents[1]
        predSubjRef = predicateComponents[2]
        # Different cases (differing number of components)
        if numberOfComponents == 3:
            # intransitive
            predSubjRef = predSubjRef.split(')')[0]
        elif numberOfComponents == 4:
            # Transitive
            predDirObjRef = predicateComponents[3].split(')')[0]
        elif numberOfComponents == 5:
            # Ditransitive - NOT YET IMPLEMENTED
            # predIndirObjRef = predicateComponents[4].split(')')[0]
            pass
        else:
            # invalid
            raise ValueError('Too many components ?')
        # Hardcode be case for specific scenarios

        if predVerb == 'be':
            # Check if naming or setting an equivalency
            if 'named' in predSubjRef:
                # If so call naming method
                self.DRSGraph = self.nameItem(predSubjRef, predDirObjRef, self.DRSGraph)
            # If not named(XYZ) but still has 4 components
            elif numberOfComponents == 4:
                # Get nodes for both subject and direct object
                subjRefNode = self.DRSGraph.FindItemWithValue(predSubjRef)
                dirObjRefNode = self.DRSGraph.FindItemWithValue(predDirObjRef)
                # If both are ITEM nodes in the graph, then the "Be" is setting an equivalency
                if subjRefNode is not None and dirObjRefNode is not None and 'Item' in dirObjRefNode:
                    self.DRSGraph.addNodeEquivalencyEdges(subjRefNode, dirObjRefNode)
                # If the target node is a PROPERTY node, then the 'BE' is setting an "is" property relationship
                elif subjRefNode is not None and dirObjRefNode is not None and 'Property' in dirObjRefNode:
                    self.DRSGraph.addPropertyEdge(subjRefNode, dirObjRefNode)
            # HANDLE ANY OTHER CASES????

        # Hardcode "have" case for composition
        elif predVerb == 'have':
            if numberOfComponents == 4:
                # Get nodes for both subject and direct object
                subjRefNode = self.DRSGraph.FindItemWithValue(predSubjRef)
                dirObjRefNode = self.DRSGraph.FindItemWithValue(predDirObjRef)
                # If both are nodes in the graph, then the "have" is setting a composition
                if subjRefNode is not None and dirObjRefNode is not None:
                    self.DRSGraph.addCompositionEdges(subjRefNode, dirObjRefNode)
        else:
            # Create Action Node
            self.DRSGraph.AppendItemAffordanceAtSpecificNode(predSubjRef, predVerb)
            actionGraph = ActionGraph(self.graphNumber)
            actionGraph.appendActionValue(predReferenceVariable)
            actionGraph.appendActionVerb(predVerb)
            # Increase the graph number for auto-generation of names
            self.graphNumber = self.graphNumber + 1
            # If a main graph already exists, then add the new graph in to it
            if self.DRSGraph.graph is not None:
                self.DRSGraph.graph = networkx.algorithms.operators.binary.compose(self.DRSGraph.graph,
                                                                                   actionGraph.graph)
            # if no main graph exists, this is the main graph
            else:
                self.DRSGraph.graph = actionGraph.graph

            # Get subject reference node
            subjRefNode = self.DRSGraph.FindItemWithValue(predSubjRef)
            actionNode = self.DRSGraph.FindItemWithValue(predReferenceVariable)

            # If just one subject "The target appears"
            if numberOfComponents == 3:
                # self.DRSGraph.AppendItemAffordanceAtSpecificNode(predSubjRef, predVerb)
                self.DRSGraph.addActionPerformerEdges(subjRefNode, actionNode)
            # If subject and direct object (e.g. "The subject remembers the letter")
            # predSubjRef = "Subject", predDirObjRef = "letter"
            elif numberOfComponents == 4:
                dirObjRefNode = self.DRSGraph.FindItemWithValue(predDirObjRef)
                self.DRSGraph.addActionPerformerEdges(subjRefNode, actionNode)
                self.DRSGraph.addActionTargetEdges(actionNode, dirObjRefNode)

            # TODO TODO TODO TODO
            elif numberOfComponents == 5:
                pass

    # For has_part() predicates
    def predicate_has_part(self, predicateContents):
        # Get predicate items
        predicateComponents = predicateContents.split(',')
        predGroupRef = predicateComponents[0]
        predGroupMember = predicateComponents[1].split(')')[0]
        # Hardcode the new object as being a group
        predGroupDescription = 'GROUP'
        # if Group reference doesn't exist
        groupNode = self.DRSGraph.FindItemWithValue(predGroupRef)
        memberNode = self.DRSGraph.FindItemWithValue(predGroupMember)
        if groupNode is None:
            # Then create that item
            # Apply appropriate variables to ItemGraph
            groupGraph = ItemGraph(self.graphNumber)
            groupGraph.appendItemValue(predGroupRef)
            groupGraph.appendItemRole(predGroupDescription)
            # Get the node for the group
            groupNode = groupGraph.FindItemWithValue(predGroupRef)
            # Increase the graph number for auto-name generation
            self.graphNumber = self.graphNumber + 1
            # Compose the new graph with the existing graph
            # (no scenario of no existing graph because can't start with has_part())
            self.DRSGraph.graph = networkx.algorithms.operators.binary.compose(self.DRSGraph.graph, groupGraph.graph)
        # Add membership edges
        self.DRSGraph.addGroupMembershipEdges(groupNode, memberNode)

    # HANDLE MODIFIERS - PREPOSITION
    # TODO TODO TODO TODO
    def predicate_modifier_pp(self, predicateContents):
        # Find action node of predicate
        # Get predicate items
        predicateComponents = predicateContents.split(',')
        modPPRefID = predicateComponents[0] + 'mod'
        modPPPrep = predicateComponents[1]
        modPPModifiedVerb = predicateComponents[0]
        modPPTargetObj = predicateComponents[2].split(')')[0]

        # Create Modifier Node
        modGraph = ModifierPPGraph(self.graphNumber)
        modGraph.appendModPPValue(modPPRefID)
        modGraph.appendModPPPrep(modPPPrep)

        # Increase the graph number for auto-generation of names
        self.graphNumber = self.graphNumber + 1

        # If a main graph already exists, then add the new graph in to it
        if self.DRSGraph.graph is not None:
            self.DRSGraph.graph = networkx.algorithms.operators.binary.compose(self.DRSGraph.graph, modGraph.graph)
        # if no main graph exists, this is the main graph
        else:
            self.DRSGraph.graph = modGraph.graph

        # Add verb and object modifier edges
        modNode = self.DRSGraph.FindItemWithValue(modPPRefID)
        verbNode = self.DRSGraph.FindItemWithValue(modPPModifiedVerb)
        objectNode = self.DRSGraph.FindItemWithValue(modPPTargetObj)
        self.DRSGraph.addModifierVerbEdges(modNode, verbNode)
        self.DRSGraph.addModifierObjectEdges(modNode, objectNode)

    # HANDLE MODIFIERS - ADVERB
    def predicate_modifier_adv(self, predicateContents):
        pass

    # HANDLE PROPERTIES
    # TODO: Handle 4/6 component properties
    # TODO: Handle degrees besides "pos"
    def predicate_property(self, predicateContents):
        # Break up the predicate
        predicateComponents = predicateContents.split(',')
        numberOfComponents = len(predicateComponents)
        # Always have first two components, others distributed based on number of components
        propRefId = predicateComponents[0]
        propAdjective = predicateComponents[1]
        # Different cases (differing number of components)
        if numberOfComponents == 3:
            # Only a primary object
            propDegree = predicateComponents[2].split(')')[0]
        elif numberOfComponents == 4:
            # Primary and secondary object
            propDegree = predicateComponents[2]
            # propSecObj = predicateComponents[3].split(')')[0]
        elif numberOfComponents == 6:
            # Primary, secondary, and tertiary objects
            # propSecObj = predicateComponents[2]
            propDegree = predicateComponents[3]
            # propCompTarget = predicateComponents[4]
            # propTertObj = predicateComponents[5].split(')')[0]
        else:
            # invalid
            raise ValueError('Too many components ?')

        existingNodeWithRefId = self.DRSGraph.FindItemWithValue(propRefId)
        if existingNodeWithRefId is None:
            # Apply appropriate variables to PropertyGraph (operating off same graph number
            # because the number in the name is irrelevant)
            propGraph = PropertyGraph(self.graphNumber)
            propGraph.appendPropValue(propRefId)
            propGraph.appendPropAdj(propAdjective)
            propGraph.appendPropDegree(propDegree)
            # Increase the graph number for auto-generation of names
            self.graphNumber = self.graphNumber + 1
            # If a main graph already exists, then add the new graph in to it
            if self.DRSGraph.graph is not None:
                self.DRSGraph.graph = networkx.algorithms.operators.binary.compose(self.DRSGraph.graph, propGraph.graph)
            # if no main graph exists, this is the main graph
            else:
                self.DRSGraph.graph = propGraph.graph
            return True
        else:
            outEdgesFromNode = self.DRSGraph.graph.out_edges(existingNodeWithRefId, data=True)
            adjectiveNode = None
            for startNode, endNode, edgeValues in outEdgesFromNode:
                # If an edge has the value ItemHasName, then we want to modify the end node
                if edgeValues['value'] == 'PropertyHasAdjective':
                    # Update graph with name
                    adjectiveNode = endNode
            if adjectiveNode is not None:
                self.DRSGraph.AppendValueAtSpecificNode(adjectiveNode, propAdjective)
            else:
                print(
                    "Error - Encountered duplicate reference for property but did not find adjective node to append to")
            return True

    # CAN PROBABLY MAKE THE NAME CHANGE A CLASS FUNCTION ????  MAKE APPEND/REPLACE BE ABLE TO TAKE IN SPECIFIC TARGETS?
    def nameItem(self, predSubjRef, predDirObjRef, DRSGraph):
        # Get item name out of "named(XYZ)"
        itemName = predSubjRef[predSubjRef.find("(") + 1:predSubjRef.find(")")]
        # Replace the name
        DRSGraph.ReplaceItemNameAtSpecificNode(predDirObjRef, itemName)
        # Return graph
        return DRSGraph


# VERY INITIAL VERSION, MOST CODE COPIED FROM PREDICATESWITCHER
# Proof of concept class to test with single case: "Is Psychomotor-Vigilance active?"

# CURRENTLY OPERATING UNDER ASSUMPTION THAT questions ALWAYS end with the predicate as the final piece.
# This will 100% need revised (probably just check if
# the current line is the final question line and then process the complete question at that point).
class questionSwitcher(object):

    def __init__(self):
        self.graphNumber = 0
        self.DRSGraph = None
        self.nodesWithGivenProperty = []
        self.nodesWithGivenPropertyAntonym = []
        # self.subjectNodeByReferenceVariable = None
        # self.objectNodeByReferenceVariable = None
        # self.subjectNodeByName = None
        # self.nodesWithGivenReferenceVariable = []
        # self.nodesWithGivenName = []
        self.subjectNode = None
        self.objectNode = None
        self.itemCount = 0
        self.propertyCount = 0
        # self.predicateTerm = ''
        self.newToOldRefIDMapping = {}

    # Method to clear the variables that get set by each question asked
    def clearVariables(self):
        self.nodesWithGivenProperty = []
        self.nodesWithGivenPropertyAntonym = []
        self.subjectNode = None
        self.objectNode = None
        self.itemCount = 0
        self.propertyCount = 0

    # Method to call the appropriate function based on the argument passed in
    def callFunction(self, predicateType, predicateContents, DRSGraph):
        # Get the name of the method
        methodName = 'question_' + str(predicateType)
        # Get the method itself
        method = getattr(self, methodName, lambda: "Unknown predicate")
        # Call the method and return its output
        self.DRSGraph = DRSGraph
        print(predicateContents)
        method(predicateContents)

    def returnDRSGraph(self):
        return self.DRSGraph

    def question_object(self, predicateContents):
        print("STILL NEED TO IMPLEMENT OBJECT IN QUESTION HANDLING")
        # Get object information
        predicateComponents = predicateContents.split(',')
        objRefId = predicateComponents[0]
        objRole = predicateComponents[1]
        # objClass = predicateComponents[2]
        # objUnit = predicateComponents[3]
        # objOperator = predicateComponents[4]
        # objCount = predicateComponents[5].split(')')[0]
        # Get the item node in the original instruction which this SHOULD correspond to
        DRSEquivalentNode = self.findItemNodeWithRole(objRole)
        print(DRSEquivalentNode)
        if self.DRSGraph.graph.has_node(DRSEquivalentNode):
            DRSNodeRefID = self.DRSGraph.graph.node[DRSEquivalentNode]['value']
            self.newToOldRefIDMapping.update({objRefId: DRSNodeRefID})
            print("NEW TO OLD OBJECT REF ID MAPPING", objRefId, DRSNodeRefID)
        else:
            self.newToOldRefIDMapping.update({objRefId: None})
            print("NEW TO OLD OBJECT REF ID NULL MAPPING", objRefId)
        # WILL NEED TO FIND A WAY TO HANDLE NAME AND ROLE TO GET MORE ACCURATE PICTURE?

        # findItemNodeWithNameAndRole(self, objName):

    # HANDLE PROPERTIES
    # TODO: Handle 4/6 component properties
    # TODO: Handle degrees besides "pos"
    def question_property(self, predicateContents):
        # INCREMENTING PROPERTY COUNT HERE UNDER ASSUMPTION THAT ANY PROPERTY MENTIONED IN THE
        # QUESTION WOULD BE IN THE PREDICATE
        # MAY BE INCORRECT
        # self.propertyCount = self.propertyCount + 1
        # Break up the predicate
        predicateComponents = predicateContents.split(',')
        numberOfComponents = len(predicateComponents)
        # Always have first two components, others distributed based on number of components
        propRefId = predicateComponents[0]
        propAdjective = predicateComponents[1]
        # Different cases (differing number of components) - completely unused right now, but leaving commented out
        # in case of implementation
        if numberOfComponents == 3:
            # Only a primary object
            # propDegree = predicateComponents[2].split(')')[0]
            pass
        elif numberOfComponents == 4:
            # Primary and secondary object
            # propDegree = predicateComponents[2]
            # propSecObj = predicateComponents[3].split(')')[0]
            pass
        elif numberOfComponents == 6:
            # Primary, secondary, and tertiary objects
            # propSecObj = predicateComponents[2]
            # propDegree = predicateComponents[3]
            # propCompTarget = predicateComponents[4]
            # propTertObj = predicateComponents[5].split(')')[0]
            pass
        else:
            # invalid
            raise ValueError('Too many components ?')

        # INITIAL NYM TESTING - will need to extend to other predicates as well of course
        adjectiveNymList, antonymList = getNyms(propAdjective)
        # print("ADJECTIVES", adjectiveNymList)
        adjectiveNodes = self.ListOfNodesWithValueFromList(adjectiveNymList)
        antonymNodes = self.ListOfNodesWithValueFromList(antonymList)

        print("ADJECTIVE NODES", adjectiveNodes)
        newNymCount = 0
        while len(adjectiveNodes) < 1 and len(antonymNodes) < 1 and newNymCount < 3:
            # No nodes "active"
            newAdjective = requestNewTermToNymCheck(propAdjective)
            newNymCount = newNymCount + 1
            adjectiveNymList, newAntonymList = getNyms(newAdjective)
            # antonymList.extend(newAntonymList)
            antonymNodes = self.ListOfNodesWithValueFromList(antonymList)
            adjectiveNodes = self.ListOfNodesWithValueFromList(adjectiveNymList)
            # Add new term into adjective node in order to grow our vocabulary
            # for node in adjectiveNodes:
            #    print("FOUND ONE" + node)
            #    #Add original term
            #    if(propAdjective not in self.DRSGraph.graph.node[node]['value']):
            #        self.DRSGraph.AppendValueAtSpecificNode(node, propAdjective)
            #    #Add new term if it was a synonym and not a term already found
            #    if(newAdjective not in self.DRSGraph.graph.node[node]['value']):
            #        self.DRSGraph.AppendValueAtSpecificNode(node, newAdjective)

        if len(adjectiveNodes) > 0:
            # propertyNodesWithAdjective = []
            for node in adjectiveNodes:
                print("AdjectiveNode", node)
                # Add new term into adjective node in order to grow our vocabulary
                if propAdjective not in self.DRSGraph.graph.node[node]['value']:
                    self.DRSGraph.AppendValueAtSpecificNode(node, propAdjective)
                propertyNode = self.getPropertyNodeFromAdjective(node)
                # print("propertyNode", propertyNode)
                self.nodesWithGivenProperty.append(propertyNode)
                # MAP FOUND PROPERTY NODE'S REF ID TO THE INCOMING REF ID
                if self.DRSGraph.graph.has_node(propertyNode):
                    DRSNodeRefID = self.DRSGraph.graph.node[propertyNode]['value']
                    self.newToOldRefIDMapping.update({propRefId: DRSNodeRefID})
                    print("NEW TO OLD PROPERTY REF ID MAPPING", propRefId, DRSNodeRefID)
                else:
                    self.newToOldRefIDMapping.update({propRefId: None})
                    print("NEW TO OLD PROPERTY REF ID NULL MAPPING", propRefId)

        if len(antonymNodes) > 0:
            # propertyNodesWithAdjective = []
            for node in antonymNodes:
                print("AntonymNode", node)
                # if(propAdjective not in self.DRSGraph.graph.node[node]['value']):
                #    self.DRSGraph.AppendValueAtSpecificNode(node, propAdjective)
                propertyNode = self.getPropertyNodeFromAdjective(node)
                # print("propertyNode", propertyNode)
                self.nodesWithGivenPropertyAntonym.append(propertyNode)
                # MAP FOUND ANTONYM NODE'S REF ID TO THE INCOMING REF ID
                if self.DRSGraph.graph.has_node(propertyNode):
                    DRSNodeRefID = self.DRSGraph.graph.node[propertyNode]['value']
                    self.newToOldRefIDMapping.update({propRefId: DRSNodeRefID})
                    print("NEW TO OLD PROPERTY REF ID MAPPING", propRefId, DRSNodeRefID)
                else:
                    self.newToOldRefIDMapping.update({propRefId: None})
                    print("NEW TO OLD PROPERTY REF ID NULL MAPPING", propRefId)

        # ***********************************************************************************************************************************
        # If no adjective nodes are found, then we look for antonyms
        # Because of this, we are positive-biased, as if we find adjective nodes, we don't look for antonyms
        # May be a better approach to look for both and, if both are found, declare a conflict rather than assume
        # one way or the other?
        # Slower processing time though
        # ***********************************************************************************************************************************
        # else:
        # antonymNodes = self.ListOfNodesWithValueFromList(antonymList)
        # We don't want to grow the vocabulary here directly, so we skip the adding new terms
        # if (len(antonymNodes) > 0):
        #    propertyNodesWithAdjective = []
        #    for node in antonymNodes:
        #        print("AntonymNode", node)
        #        if(propAdjective not in self.DRSGraph.graph.node[node]['value']):
        #            self.DRSGraph.AppendValueAtSpecificNode(node, propAdjective)
        #        propertyNode = self.getPropertyNodeFromAdjective(node)
        #        #print("propertyNode", propertyNode)
        #        self.nodesWithGivenPropertyAntonym.append(propertyNode)

    # For predicate() predicates
    # HOW TO HANDLE SENTENCE SUB-ORDINATION?
    def question_predicate(self, predicateContents):
        # Intransitive verbs: (predName, verb, subjectRef)
        # - The SubjectRef Verbed (the man laughed, the target appears)
        # Transitive verbs: (predName, verb, subjectRef, dirObjRef)
        # - The Subjectref Verbed the dirObjRef (the task A has a group of objects H,
        # the subject L remembers the letter I)
        # Ditransitive verbs: (predName, verb, subjRef, dirObjRef, indirObjRef)
        # - The SubjectRef verbed the DirObjRef to the indirObjRef (The professor (S) gave
        # the paper (D) to the student (I))
        # Break up the predicate
        predicateComponents = predicateContents.split(',')
        numberOfComponents = len(predicateComponents)
        # Always have first three components, so only special cases are transitive/ditransitive
        # predReferenceVariable = predicateComponents[0]
        predVerb = predicateComponents[1]
        predSubjRef = predicateComponents[2]
        # Set dir/indir object references to none so we can check them for substitution
        predDirObjRef = None
        predIndirObjRef = None
        # Different cases (differing number of components)
        if numberOfComponents == 3:
            # intransitive
            predSubjRef = predSubjRef.split(')')[0]
        elif numberOfComponents == 4:
            # Transitive
            predDirObjRef = predicateComponents[3].split(')')[0]
        elif numberOfComponents == 5:
            # Ditransitive
            predIndirObjRef = predicateComponents[4].split(')')[0]
        else:
            # invalid
            raise ValueError('Too many components ?')
        # Hardcode be case for specific scenarios

        # Substitute in DRS equivalents for dereferenced ref IDs
        if predSubjRef in self.newToOldRefIDMapping:
            predSubjRef = self.newToOldRefIDMapping.get(predSubjRef)
            if predSubjRef is None:
                # TODO: Better define this error case
                print("SOMETHING WENT WRONG - BETTER ERROR CASE TO COME; A MAPPING WAS NULL ")
                return None
        if predDirObjRef is not None and predDirObjRef in self.newToOldRefIDMapping:
            predDirObjRef = self.newToOldRefIDMapping.get(predDirObjRef)
            if predDirObjRef is None:
                # TODO: Better define this error case
                print("SOMETHING WENT WRONG - BETTER ERROR CASE TO COME; A MAPPING WAS NULL ")
                return None
        if predIndirObjRef is not None and predIndirObjRef in self.newToOldRefIDMapping:
            predIndirObjRef = self.newToOldRefIDMapping.get(predIndirObjRef)
            if predIndirObjRef is None:
                # TODO: Better define this error case
                print("SOMETHING WENT WRONG - BETTER ERROR CASE TO COME; A MAPPING WAS NULL ")
                return None

        if predVerb == 'be':
            # If the SUBJECT reference is a proper name
            # Check if we find a node containing said name
            if 'named' in predSubjRef:
                # self.predicateTerm = 'named'
                # Get item name out of "named(XYZ)"
                # itemNodeList = []
                itemName = predSubjRef[predSubjRef.find("(") + 1:predSubjRef.find(")")]
                # print(itemName)
                # self.nodesWithGivenName = self.ListOfNodesWithValue(itemName)
                nodesWithGivenName = self.ListOfNodesWithValue(itemName)
                if len(nodesWithGivenName) > 0:
                    print("NODES WITH GIVEN NAME", nodesWithGivenName)
                    self.subjectNode = nodesWithGivenName[0]
            # If the subject reference is another variable, not a proper name
            else:
                # self.predicateTerm = 'be'
                subjectRefVar = predSubjRef
                # self.nodesWithGivenReferenceVariable = self.ListOfNodesWithValue(itemRefVar)
                subjectNodes = self.ListOfNodesWithValue(subjectRefVar)
                if len(subjectNodes) > 0:
                    print("SUBJECT NODES", subjectNodes)
                    self.subjectNode = subjectNodes[0]
            # print("REFVARNODES", self.nodesWithGivenReferenceVariable, "********************")

            # Same as above for OBJECT reference
            if 'named' in predDirObjRef:
                # self.predicateTerm = 'named'
                # Get item name out of "named(XYZ)"
                # itemNodeList = []
                itemName = predDirObjRef[predDirObjRef.find("(") + 1:predDirObjRef.find(")")]
                # print(itemName)
                # self.nodesWithGivenName = self.ListOfNodesWithValue(itemName)
                nodesWithGivenName = self.ListOfNodesWithValue(itemName)
                if len(nodesWithGivenName) > 0:
                    print("NODES WITH GIVEN NAME", nodesWithGivenName)
                    self.objectNode = self.nodesWithGivenName[0]
            # If the subject reference is another variable, not a proper name
            else:
                # self.predicateTerm = 'be'
                objectRefVar = predDirObjRef
                # self.nodesWithGivenReferenceVariable = self.ListOfNodesWithValue(itemRefVar)
                objectNodes = self.ListOfNodesWithValue(objectRefVar)
                if len(objectNodes) > 0:
                    print("OBJECT NODES", objectNodes)
                    self.objectNode = objectNodes[0]
                # print("REFVARNODES", self.nodesWithGivenReferenceVariable, "********************")

            # Track how many items and properties, as item-item and item-property have different edges connecting them
            print("SELF.ITEMCOUNT PRIORITY", self.itemCount)
            print("SELF.PROPCOUNT PRIORITY", self.propertyCount)
            print("SELF.SUBJECTNODE", self.subjectNode)
            print("SELF.OBJECTNODE", self.objectNode)
            if self.subjectNode is not None:
                if 'Item' in self.subjectNode:
                    self.itemCount = self.itemCount + 1
                elif 'Property' in self.subjectNode:
                    self.propertyCount = self.propertyCount + 1
            if self.objectNode is not None:
                if 'Item' in self.objectNode:
                    self.itemCount = self.itemCount + 1
                elif 'Property' in self.objectNode:
                    self.propertyCount = self.propertyCount + 1

    def resolveQuestion(self):
        # if self.predicateTerm == 'named':
        # for node in self.nodesWithGivenName:
        #    outEdgesFromNode = (self.DRSGraph.graph.out_edges(node, data=True))
        #    inEdgesFromNode = (self.DRSGraph.graph.in_edges(node, data=True))
        #    edgesFromNode = list(outEdgesFromNode) + list(inEdgesFromNode)
        #    #print(edgesFromNode)
        #    for startNode, endNode, edgeValues in edgesFromNode:
        #        print(startNode, endNode, edgeValues)
        #        if(edgeValues['value'] == 'ItemHasName'):
        #            if(startNode != node):
        #                nodeToConnect = startNode
        #                #print(nodeToConnect)
        #            elif(endNode != node):
        #                nodeToConnect = endNode
        #                #print(nodeToConnect)
        print("NAMED SUBJECT NODE", self.subjectNode)
        print("NAMED OBJECT NODE", self.objectNode)
        if self.subjectNode is not None:
            subjectNode = self.subjectNode
            # outEdgesFromSubjectNode = (self.DRSGraph.graph.out_edges(subjectNode, data=True))
            # inEdgesFromSubjectNode = (self.DRSGraph.graph.in_edges(subjectNode, data=True))
            # print("OUT EDGES FROM SUBJECT NODE: ", outEdgesFromSubjectNode)
            # print("IN EDGES FROM SUBJECT NODE: ", inEdgesFromSubjectNode)
            # edgesFromSubjectNode = list(outEdgesFromSubjectNode) + list(inEdgesFromSubjectNode)
            # for startNode, endNode, edgeValues in outEdgesFromSubjectNode:
            #    if(edgeValues['value'] == 'ItemHasName'):
            #        print("START NODE", startNode)
            #        print("END NODE", endNode)
            #        if(startNode != subjectNode):
            #            subjectNodeToConnect = startNode
            #        elif(endNode != subjectNode):
            #            subjectNodeToConnect = endNode
        if self.objectNode is not None:
            pass
            # COMMENTED OUT BECAUSE I DON'T THINK IT DOES ANYTHING
            # objectNode = self.objectNode
            # outEdgesFromObjectNode = (self.DRSGraph.graph.out_edges(objectNode, data=True))
            # inEdgesFromObjectNode = (self.DRSGraph.graph.in_edges(objectNode, data=True))
            # edgesFromObjectNode = list(outEdgesFromObjectNode) + list(inEdgesFromObjectNode)
            # for startNode, endNode, edgeValues in edgesFromObjectNode:
            #    if(edgeValues['value'] == 'ItemHasName'):
            #        if(startNode != objectNode):
            #            objectNodeToConnect = startNode
            #        elif(endNode != objectNode):
            #            objectNodeToConnect = endNode

        # if self.predicateTerm == 'be':
        # for node in self.nodesWithGivenReferenceVariable:
        #    nodeToConnect = node
        # subjectNodeToConnect = self.subjectNode
        # objectNodeToConnect = self.objectNode
        # print("SUBJECT NODE", subjectNodeToConnect)
        # print("OBJECT NODE", objectNodeToConnect)

        # Assuming that if there is one item and one property, the item is the subject node, so the "Is" edge will be
        # in the outEdges
        # This may be an incorrect assumption, will need to test and check
        # Checking if there is an edge with name "Is", since "Is" is the name given to item->property edges.
        # THIS SHOULD BE ABSTRACTED, THERE SHOULD BE A VARIABLE SOMEWHERE THAT HOLDS IMPORTANT EDGE NAMES
        print("ITEM COUNT", self.itemCount)
        print("PROP  COUNT", self.propertyCount)
        if self.itemCount == 1 and self.propertyCount == 1:
            for node in self.nodesWithGivenProperty:
                # print(node)
                print("OUT FROM CONNECT", self.DRSGraph.graph.out_edges(subjectNode))
                outEdgesFromSubjectNode = self.DRSGraph.graph.out_edges(subjectNode, data=True)
                for startNode, endNode, edgeValues in outEdgesFromSubjectNode:
                    if edgeValues['value'] == 'Is':
                        return True
                # print("IN FROM CONNECT", self.DRSGraph.graph.in_edges(subjectNode))
                # if(self.DRSGraph.graph.has_edge(node, subjectNode, key="Is")):
                #    return True
                # if(self.DRSGraph.graph.has_edge(subjectNode, node, key="Is")):
                #    return True
            for antonymNode in self.nodesWithGivenPropertyAntonym:
                print("OUT FROM CONNECT", self.DRSGraph.graph.out_edges(subjectNode))
                outEdgesFromSubjectNode = self.DRSGraph.graph.out_edges(subjectNode, data=True)
                for startNode, endNode, edgeValues in outEdgesFromSubjectNode:
                    if edgeValues['value'] == 'Is':
                        return False
                # if(self.DRSGraph.graph.has_edge(antonymNode, subjectNode, key="Is")):
                #    #print("AHA IT IS THE SECOND THAT MUST COUNT")
                #    return False
                # if(self.DRSGraph.graph.has_edge(subjectNode, antonymNode, key="Is")):
                #    #print("")
                #    return False
            return None

        # Assuming if there are two items, there are no properties in the predicate (again, may need corrections)
        if self.itemCount == 2:
            print("OUT FROM CONNECT", self.DRSGraph.graph.out_edges(subjectNode))
            # Since "IsEquivalentTo" is a bi-directional edge, it doesn't matter which node we look from, but
            # it makes sense to look from the subject node for consistency's sake
            outEdgesFromSubjectNode = self.DRSGraph.graph.out_edges(subjectNode, data=True)
            for startNode, endNode, edgeValues in outEdgesFromSubjectNode:
                if edgeValues['value'] == 'IsEquivalentTo':
                    # If IsEquivalentTo edge is found connecting the subject node and the object node
                    return True
            # If IsEquivalentTo edge is not found connecting the subject node and the object node
            return False
            # If neither of the above scenarios has occurred, then unknown
        return None

    def ListOfNodesWithValueFromList(self, listOfNyms):
        nodeList = []
        for valueToFind in listOfNyms:
            # print(valueToFind)
            if self.DRSGraph is not None:
                # iterate through all graph nodes
                for node, values in self.DRSGraph.graph.nodes.data():
                    listOfValuesToCheck = values['value'].split('|')
                    # print("VALUES CHECKING LIST ", listOfValuesToCheck)

                    if valueToFind in listOfValuesToCheck:
                        # print("FOUND", valueToFind)
                        nodeList.append(node)
                    # If the current Node's value = the value passed in
                    # Changed from valueToFind in values to valueToFind == values as "active" was triggering
                    # found in "inactive" due to being substr
                    # if(valueToFind == values['value']):
                    #    print("FOUND", valueToFind)
                    #    nodeList.append(node)
        # print(nodeList)
        return nodeList

    def ListOfNodesWithValue(self, valueToFind):
        nodeList = []
        if self.DRSGraph is not None:
            # iterate through all graph nodes
            for node, values in self.DRSGraph.graph.nodes.data():
                # If the current Node's value = the value passed in
                # Changed from valueToFind in values to valueToFind == values as "active" was
                # triggering found in "inactive" due to being substr
                if valueToFind == values['value']:
                    nodeList.append(node)
        return nodeList

    def getPropertyNodeFromAdjective(self, adjectiveNode):
        # Get list of edges from the node
        inEdgesFromNode = self.DRSGraph.graph.in_edges(adjectiveNode, data=True)
        outEdgesFromNode = self.DRSGraph.graph.out_edges(adjectiveNode, data=True)
        edgesFromNode = list(inEdgesFromNode) + list(outEdgesFromNode)
        for startNode, endNode, edgeValues in edgesFromNode:
            # If an edge has the value ItemHasName, then we want to modify the end node
            if edgeValues['value'] == 'PropertyHasAdjective':
                # Update graph with name
                return startNode

    # TEMP UNTIL FIGURE OUT NAME HANDLING
    def findItemNodeWithRole(self, strRole):
        # Get list of nodes with the given role
        roleNodes = self.ListOfNodesWithValue(strRole)
        # Handle role nodes
        # roleItemNodes = []
        # Get list of item nodes associated with the role nodes
        for roleNode in roleNodes:
            print("ROLE NODE", roleNode)
            roleItemNode = self.findItemNodeConnectedToRoleNode(roleNode)
            print("ROLE ITEM NODE", roleItemNode)
            return roleItemNode

    def findItemNodeWithNameAndRole(self, strName, strRole):
        # Get list of nodes with the given name
        nameNodes = self.ListOfNodesWithValue(strName)
        # Get list of nodes with the given role
        roleNodes = self.ListOfNodesWithValue(strRole)
        # Handle name nodes
        nameItemNodes = []
        # Get list of item nodes associated with the name nodes
        for nameNode in nameNodes:
            nameItemNode = self.findItemNodeWithName(nameNode)
            nameItemNodes.append(nameItemNode)
        # Handle role nodes
        roleItemNodes = []
        # Get list of item nodes associated with the role nodes
        for roleNode in roleNodes:
            roleItemNode = self.findItemNodeConnectedToRoleNode(roleNode)
            roleItemNodes.append(roleItemNode)
        # Find item node which has both the name and role
        # Iterate through role nodes for arbitrary reason
        for potentialItemNode in roleItemNodes:
            if potentialItemNode in nameItemNodes:
                return potentialItemNode

    def findItemNodeConnectedToNameNode(self, nameNode):
        # Edges seem to be a little weird, so getting
        # outEdgesFromNode = self.DRSGraph.graph.out_edges(roleNode, data=True)
        inEdgesFromNode = self.DRSGraph.graph.in_edges(nameNode, data=True)
        # edgesFromNode = inEdgesFromNode
        # edgesFromNode = self.DRSGraph.graph.edges(nameNode, data=True)
        for startNode, endNode, edgeValues in inEdgesFromNode:
            # If an edge has the value ItemHasName, then we want to return the start node (the item node itself)
            if edgeValues['value'] == 'ItemHasName':
                # print(startNode, endNode, edgeValues)
                print("FOUND NODE WITH NAME:", startNode)
                return startNode

    def findItemNodeConnectedToRoleNode(self, roleNode):
        # outEdgesFromNode = self.DRSGraph.graph.out_edges(roleNode, data=True)
        inEdgesFromNode = self.DRSGraph.graph.in_edges(roleNode, data=True)
        # edgesFromNode = outEdgesFromNode + inEdgesFromNode
        for startNode, endNode, edgeValues in inEdgesFromNode:
            # If an edge has the value ItemHasName, then we want to return the start node (the item node itself)
            if edgeValues['value'] == 'ItemHasRole':
                # print(startNode, endNode, edgeValues)
                print("FOUND NODE WITH ROLE:", startNode)
                return startNode


def requestNewTermToNymCheck(originalTerm):
    newTerm = input(
        "Sorry, I don't understand \"" + originalTerm + "\".  Please give me an alternate word and "
                                                        "I'll make the connection.")
    return newTerm


def APEWebserviceCall(phraseToDRS):
    print(phraseToDRS)
    # Make APE Webservice call with given ACE phrase
    urlToRequest = "http://attempto.ifi.uzh.ch/ws/ape/apews.perl?text=" + phraseToDRS + "&solo=drspp"
    # Get the DRS that is sent back
    r = requests.get(urlToRequest)
    returnedDRS = r.text.splitlines()
    # enteredQuestion = False
    DRSLines = []
    error = False
    for line in returnedDRS:
        line = line.strip()
        # Exclude first, useless line
        # Also skip empty lines (if line.strip() returns true if line is non-empty.)
        if line != '[]' and line.strip():
            if line == "importance=\"error\"":
                error = True
            # print("SPACE ONLY")
            print(line)
            DRSLines.append(line)
    # Technically it's a little silly to categorize the DRS for a question since it's obviously all
    # a question, but this gets around having to do questionable and inconsistent parsing to deal with
    # the header lines
    # This way, we can just get the question lines, which are what we actually use to process questions
    if error:
        return None
    else:
        symbolLines = getSymbolLines(DRSLines)
        print("SYMBOLS - ", symbolLines)
        categorizedQuestionDRS = categorizeDRSLines(DRSLines, symbolLines)
        print(categorizedQuestionDRS)

        questionLines = []
        # Iterate through DRS lines and get only the actual question lines, none of the headers
        for index, line in enumerate(DRSLines):
            if categorizedQuestionDRS.get(index) == 'question':
                questionLines.append(line)
        print(questionLines)
        # Return just the lines that are the actual DRS for the question, no headers
        return questionLines


def getNyms(wordToCheck):
    # Iterate through all words to check
    synonyms = []
    hypernyms = []
    hyponyms = []
    deriv = []
    # uniqueNymList = []
    uniqueAntonymList = []
    # for currentWord in checkWordList:
    synonyms.clear()
    hypernyms.clear()
    hyponyms.clear()
    deriv.clear()
    print(wordToCheck)
    # print(currentWord)
    # print(checkWordList[currentWord])
    # Get synsets of current word to check
    testWord = wordnet.synsets(wordToCheck)
    # for each synset (meaning)
    for syn in testWord:
        # Get Hypernyms
        if len(syn.hypernyms()) > 0:
            currentHypernyms = syn.hypernyms()
            for hyperSyn in currentHypernyms:
                for lemma in hyperSyn.lemmas():
                    # if(lemma.name() != currentWord):
                    hypernyms.append(lemma.name())
                # hypernyms.append(hyperSyn.lemma_names())
        # Get Hyponyms
        if len(syn.hyponyms()) > 0:
            currentHyponyms = syn.hyponyms()
            for hypoSyn in currentHyponyms:
                for lemma in hypoSyn.lemmas():
                    # if(lemma.name() != currentWord):
                    hyponyms.append(lemma.name())
                # hypernyms.append(hyperSyn.lemma_names())
        # Get direct synonyms
        for lemma in syn.lemmas():
            # if(lemma.name() != currentWord):
            synonyms.append(lemma.name())
            # Get derivationally related forms
            for derivForm in lemma.derivationally_related_forms():
                if derivForm.name() not in deriv:
                    deriv.append(derivForm.name())
            # Get antonyms
            if lemma.antonyms():
                # print(lemma.antonyms()[0].name())
                if lemma.antonyms()[0].name() not in uniqueAntonymList:
                    uniqueAntonymList.append(lemma.antonyms()[0].name())
    # print("SYNONYMS: ")
    # print(set(synonyms))
    # print('\n HYPERNYMS:')
    # print(set(hypernyms))
    # print('\n HYPONYMS:')
    # print(set(hyponyms))
    # print('\n DERIVATIONALLY RELATED FORMS:')
    # print(set(deriv))
    nymLists = synonyms + hypernyms + hyponyms + deriv
    uniqueNyms = set(nymLists)
    uniqueNymList = list(uniqueNyms)
    # print(uniqueNymList)
    # print("ANTONYMS", uniqueAntonymList)
    return uniqueNymList, uniqueAntonymList


# TODO: handle 5-item predicate() tags
# TODO: handle conditionals - SPECIFICALLY X -> Y; Y -> Z, how to avoid Y just being stored twice (target appears)
# TODO: make overarching situationGraph which contains Item/Prop graphs and has graph-wide functions (move some to it)

# FORMAT OF A QUESTION:
# QUESTION
# [R,S]
# property(R,active,pos)-7/3
# predicate(S,be,A,R)-7/1

# Concept: See if there is a property "active" (Don't create it) (make a list of all nodes that are property "active")
# Then see if the predicate A has an edge to such a node?
# CURRENTLY QUESTION TEST INVOLVES QUESTION AT END.  WILL NEED TO TEST QUESTION IN MIDDLE
# Alternatively, create the network of the question and then try to map it onto the graph and see if that works?

# TODO: Extend wordnet checking, then add on verbnet and framenet

# CONCEPT: Have a flag on properties that mark them as true or not (isActive, isPresent, etc.)
# CONCEPT: For conditionals, set up a disconnected graph that details what happens if the IF section is true.
# Then, when that statement arrives, trigger the THEN.
# CONCEPT: When a term comes in that is not existing ("ongoing" vis-a-vis "active"), request explanation and
# store explanation alongside the term.
# NOTE: Conditionals are treated as an "and" by default - if you have X, Y => Z, both X and Y must be true.
# In the PVT case, since THE target appears in THE box, the trigger case will be identical,
# save for predicate reference ID, to the conditional case.
# If it were A target appears in A box, then the conditional case would create its own target and box -
# case that would need handling.\
# Because of this, may not need to create disconnected graph for conditionals, instead just store the
# lines that make up the conditional and test each incoming line to see if it triggers?
# Need to be able to check multiple lines if the trigger is multi-line (maybe do a look-ahead if first line is found?)

# Should find some way to encode non-triggered conditionals in case the knowledge is relevant
# (maybe do a look through the conditionals and see if it's found?)
# If it is found in conditional but not in graph, should return that it knows of its existence but that it's not true???

# Alternatively, implement the Transition part of the ontology.

# Potential concern: more synonyms being added to a label may lead to drift and inaccuracy
# Potential risk of recursive conditional triggering: A conditional runs itself
# (or something similar enough to re-trigger)


def DRSToItem():
    import matplotlib.pyplot as plt
    # Declare relevant variables
    DRSGraph = None
    DRSLines = []
    # Read in DRS instructions from file
    # DRSFile = open("DRS_read_in.txt", "r")
    DRSFile = open("DRS_read_in.txt", "r")
    for line in DRSFile:
        # Get DRS command and remove any leading and ending whitespace
        DRSLines.append(line.strip())
    # Get numbers of which lines are headers ([A, B, C, ...] and conditionals (=>) )
    symbolLines = getSymbolLines(DRSLines)
    # instructionCountInMatchingIfBlock = 0

    categorizedDRSLines = categorizeDRSLines(DRSLines, symbolLines)
    # print(categorizedDRSLines)
    # print(categorizedDRSLines)

    # Get all if-then sets
    conditionalSets = getConditionals(DRSLines, categorizedDRSLines)

    # print(conditionalSets)
    # Set up the predicate switcher
    predSwitcher = predicateSwitcher()

    # Set up counter for question response
    questionCounter = 1

    # Iterate through the DRS instructions
    for index, currentInstruction in enumerate(DRSLines):
        # take next instruction or exit
        # nextStep = input("Enter anything to read in next line\n")
        nextStep = ''

        # As long as no "exit" given
        if nextStep != 'exit':
            print(currentInstruction)
            # print(conditional)
            # If the current line is an instruction
            if categorizedDRSLines.get(index) == 'instruction':
                # print(currentInstruction)
                # Get the predicate type and contents
                # , predSwitcher, DRSGraph - potentially unused parameters removed
                instructionCountInMatchingIfBlock, conditionalWithMatchingIfBlock = \
                    checkCurrentInstructionIf(DRSLines, index, currentInstruction, conditionalSets)
                if instructionCountInMatchingIfBlock == 0:
                    DRSGraph = splitAndRun(currentInstruction, predSwitcher)
                else:
                    # instructionCountInMatchingIfBlock = instructionCountInMatchingIfBlock - 1
                    pass

                # DRSGraph = checkCurrentInstructionIf(DRSLines, index, currentInstruction,
                # conditionalSets, predSwitcher, DRSGraph)
        # Break out of loop with exit
        else:
            break

    # On end of reading in instructions
    # process conditionals first:
    for conditional in conditionalSets:
        if not conditional.processed:
            DRSGraph = runFullConditional(conditional, predSwitcher, DRSGraph, conditionalSets)

    # Set up questionSwitcher
    qSwitcher = questionSwitcher()
    questionInput = input('Please enter a question')
    # "exit" is trigger word to end questioning
    while questionInput != 'exit':
        # "eoq" is trigger
        # while questionInput != 'eoq':
        # HANDLE QUESTIONS HERE
        #    questionInput = questionInput.strip()
        #    predicateSplit = questionInput.split('(', 1)
        #    predicateType = predicateSplit[0]
        #    predicateContents = predicateSplit[1]
        #    #print(categorizedDRSLines.get(index))
        #    qSwitcher.callFunction(predicateType, predicateContents, DRSGraph)
        #    print(currentInstruction)
        #    questionInput = input('Please enter a DRS line for your question')
        questionLines = APEWebserviceCall(questionInput)
        while questionLines is None:
            questionInput = input('There was an error with the ACE entered - please try again.')
            questionLines = APEWebserviceCall(questionInput)

        for currentLine in questionLines:
            predicateSplit = currentLine.split('(', 1)
            predicateType = predicateSplit[0]
            predicateContents = predicateSplit[1]
            # print(categorizedDRSLines.get(index))
            qSwitcher.callFunction(predicateType, predicateContents, DRSGraph)
            print(currentInstruction)
        #    questionInput = input('Please enter a DRS line for your question')

        # NEED TO PASS FULL DRS TO QUESTIONSWITCHER AND THEN HANDLE WITHIN THAT

        # Once 'eoq' has been entered, process the question.
        # Get list of words to check -nyms for
        # qcheckWordList = qSwitcher.wordsToNymCheck
        # nymWordList, antonymList = getNyms(checkWordList)
        # print(nymWordList)
        result = qSwitcher.resolveQuestion()
        if result:
            print("Question", str(questionCounter), "Answer: Yes")
        elif not result:
            print("Question", str(questionCounter), "Answer: No")
        else:
            print("Question", str(questionCounter), "Answer: Unknown")
        questionCounter = questionCounter + 1
        # qSwitcher.clearVariables()
        # I have my doubts about these lines below but they seem to work
        DRSGraph = qSwitcher.returnDRSGraph()
        predSwitcher.updateDRSGraph(DRSGraph.graph)
        # Reset qSwitcher to be a new question switcher
        qSwitcher = questionSwitcher()
        questionInput = input('Please enter a DRS line for your question')

    # Once "exit" has been entered
    # At end of program, if an ontology was built at all, print it out and export it in GraphML
    if DRSGraph is not None:
        networkx.draw(DRSGraph.graph, labels=networkx.get_node_attributes(DRSGraph.graph, 'value'))
        plt.show()
        jsonFile = open("jsonFile.txt", "w")
        jsonSerializable = networkx.readwrite.json_graph.node_link_data(DRSGraph.graph)
        jsonOutput = json.dumps(jsonSerializable)
        jsonFile.write(jsonOutput)
        networkx.write_graphml_lxml(DRSGraph.graph, "DRSGraph.graphml")


DRSToItem()
