import networkx


# Create Graph
def generateItemGraph(graphNumber):
    itemGraph = networkx.MultiDiGraph()
    itemGraph.add_node('Item' + str(graphNumber), value='')
    itemGraph.add_node('ItemName' + str(graphNumber), value='')
    itemGraph.add_node('ItemAffordance' + str(graphNumber), value='')
    itemGraph.add_node('ItemDescription' + str(graphNumber), value='')
    itemGraph.add_node('ItemRole' + str(graphNumber), value='')

    itemGraph.add_edge('Item' + str(graphNumber), 'ItemName' + str(graphNumber), value='ItemHasName')
    itemGraph.add_edge('Item' + str(graphNumber), 'ItemAffordance' + str(graphNumber), value='ItemHasAffordance')
    itemGraph.add_edge('Item' + str(graphNumber), 'ItemDescription' + str(graphNumber), value='ItemHasDescription')
    itemGraph.add_edge('Item' + str(graphNumber), 'ItemRole' + str(graphNumber), value='ItemHasRole')

    return itemGraph


def generatePropGraph(graphNumber):
    propGraph = networkx.MultiDiGraph()
    propGraph.add_node('Property' + str(graphNumber), value='')
    propGraph.add_node('PropertyAdjective' + str(graphNumber), value='')
    propGraph.add_node('PropertySecondaryObject' + str(graphNumber), value='')
    propGraph.add_node('PropertyTertiaryObject' + str(graphNumber), value='')
    propGraph.add_node('PropertyDegree' + str(graphNumber), value='')
    propGraph.add_node('PropertyCompTarget' + str(graphNumber), value='')

    propGraph.add_edge('Property' + str(graphNumber), 'PropertyAdjective' + str(graphNumber),
                       value='PropertyHasAdjective')
    propGraph.add_edge('Property' + str(graphNumber), 'PropertySecondaryObject' + str(graphNumber),
                       value='PropertyHasSecondaryObject')
    propGraph.add_edge('Property' + str(graphNumber), 'PropertyTertiaryObject' + str(graphNumber),
                       value='PropertyHasTertiaryObject')
    propGraph.add_edge('Property' + str(graphNumber), 'PropertyDegree' + str(graphNumber), value='PropertyHasDegree')
    propGraph.add_edge('Property' + str(graphNumber), 'PropertyCompTarget' + str(graphNumber),
                       value='PropertyHasCompTarget')

    return propGraph


def generateActionGraph(graphNumber):
    actionGraph = networkx.MultiDiGraph()
    actionGraph.add_node('Action' + str(graphNumber), value='')
    actionGraph.add_node('ActionVerb' + str(graphNumber), value='')

    actionGraph.add_edge('Action' + str(graphNumber), 'ActionVerb' + str(graphNumber), value='ActionHasVerb')

    return actionGraph


def generateModPPGraph(graphNumber):
    modPPGraph = networkx.MultiDiGraph()
    modPPGraph.add_node('ModPP' + str(graphNumber), value='')
    modPPGraph.add_node('ModPPPrep' + str(graphNumber), value='')

    modPPGraph.add_edge('ModPP' + str(graphNumber), 'ModPPPrep' + str(graphNumber), value='ModPPHasPrep')

    return modPPGraph


class ItemGraph(object):
    # Constructor
    def __init__(self, graphNumber):
        self.graphNumber = graphNumber
        if graphNumber is not None:
            self.graph = generateItemGraph(self.graphNumber)
        else:
            self.graph = None

    # Generic append method based on whatever target is passed in
    def __append(self, target, newValue):
        currentValue = self.graph.nodes(data=True)[target + str(self.graphNumber)]['value']
        if currentValue == '':
            updatedValue = newValue
        else:
            updatedValue = currentValue + '|' + newValue
        self.graph.nodes(data=True)[target + str(self.graphNumber)]['value'] = updatedValue

    # Generic replace method based on whatever target is passed in
    def __replace(self, target, newValue):
        self.graph.nodes(data=True)[target + str(self.graphNumber)]['value'] = newValue

    # Append/replace methods for each node value in Item Graph
    def appendItemValue(self, newValue):
        self.__append('Item', newValue)

    def replaceItemValue(self, newValue):
        self.__replace('Item', newValue)

    def appendItemName(self, newName):
        self.__append('ItemName', newName)

    def replaceItemName(self, newName):
        self.__replace('ItemName', newName)

    def appendItemAffordance(self, newAffordance):
        self.__append('ItemAffordance', newAffordance)

    def replaceItemAffordance(self, newAffordance):
        self.__replace('ItemAffordance', newAffordance)

    def appendItemDescription(self, newDescription):
        self.__append('ItemDescription', newDescription)

    def replaceItemDescription(self, newDescription):
        self.__replace('ItemDescription', newDescription)

    def appendItemRole(self, newRole):
        self.__append('ItemRole', newRole)

    def replaceItemRole(self, newRole):
        self.__replace('ItemRole', newRole)

    # Method to get the type of graph
    # def getTypeOfNode(self, node):
    #    print(node)
    #    print(self.graph.nodes[node])
    #    return self.graph.nodes[node]['value']

    # Method to find a node containing a given value
    def FindItemWithValue(self, valueToFind):
        if self.graph is not None:
            # iterate through all graph nodes
            for node, values in self.graph.nodes.data():
                # print(node, values)
                # If the current Node's value = the value passed in
                if values['value'] == valueToFind:
                    return node
        return None

    # Methods to add different types of edges between nodes
    def addGroupMembershipEdges(self, groupNode, memberNode):
        self.graph.add_edge(memberNode, groupNode, value='IsMemberOf')
        self.graph.add_edge(groupNode, memberNode, value='HasMember')

    def addNodeEquivalencyEdges(self, firstNode, secondNode):
        self.graph.add_edge(firstNode, secondNode, value='IsEquivalentTo')
        self.graph.add_edge(secondNode, firstNode, value='IsEquivalentTo')

    def addCompositionEdges(self, composedNode, partOfNode):
        self.graph.add_edge(composedNode, partOfNode, value='HasA')
        self.graph.add_edge(partOfNode, composedNode, value='IsPartOf')

    def addPropertyEdge(self, objectNode, propertyNode):
        self.graph.add_edge(objectNode, propertyNode, value='Is')

    # Methods to add different types of edges between nodes
    def addActionPerformerEdges(self, performerNode, actionNode):
        self.graph.add_edge(performerNode, actionNode, value='Performs')
        self.graph.add_edge(actionNode, performerNode, value='IsPerformedBy')

    def addActionTargetEdges(self, actionNode, targetNode):
        self.graph.add_edge(actionNode, targetNode, value='HasTarget')
        self.graph.add_edge(targetNode, actionNode, value='IsTargetOf')

    def addModifierVerbEdges(self, modifierNode, verbNode):
        self.graph.add_edge(modifierNode, verbNode, value='ModifiesVerb')
        self.graph.add_edge(verbNode, modifierNode, value='isModifiedBy')

    def addModifierObjectEdges(self, modifierNode, objectNode):
        self.graph.add_edge(modifierNode, objectNode, value='modifiesObject')
        self.graph.add_edge(objectNode, modifierNode, value='isModifiedBy')

    def addConditionalTriggerEdges(self, ifNodeValue, thenNodeValue):
        ifNode = self.FindItemWithValue(ifNodeValue)
        thenNode = self.FindItemWithValue(thenNodeValue)
        # We only want to trigger actions, not statement
        if ifNode is not None and thenNode is not None:
            if 'Action' in thenNode:
                self.graph.add_edge(ifNode, thenNode, value='triggers')
                self.graph.add_edge(thenNode, ifNode, value='isTriggeredBy')

    # Methods to replace values of specific nodes
    def ReplaceItemAffordanceAtSpecificNode(self, nodeToAddAffordance, newAffordance):
        node = self.FindItemWithValue(nodeToAddAffordance)
        if node is not None:
            edgesFromNode = self.graph.edges(node, data=True)
            for startNode, endNode, edgeValues in edgesFromNode:
                # If an edge has the value ItemHasName, then we want to modify the end node
                if edgeValues['value'] == 'ItemHasAffordance':
                    # Update graph with name
                    self.graph.nodes(data=True)[endNode]['value'] = newAffordance
                    return True
        else:
            print("No node with direct object reference as value found")
            return False

    # Methods to replace values of specific nodes
    def AppendItemAffordanceAtSpecificNode(self, nodeToAddAffordance, newAffordance):
        node = self.FindItemWithValue(nodeToAddAffordance)
        if node is not None:
            edgesFromNode = self.graph.edges(node, data=True)
            for startNode, endNode, edgeValues in edgesFromNode:
                # If an edge has the value ItemHasName, then we want to modify the end node
                if edgeValues['value'] == 'ItemHasAffordance':
                    # Update graph with name
                    currentValue = self.graph.nodes(data=True)[endNode]['value']
                    if currentValue == '':
                        updatedValue = newAffordance
                    else:
                        updatedValue = currentValue + '|' + newAffordance
                    self.graph.nodes(data=True)[endNode]['value'] = updatedValue
                    return True
        else:
            print("No node with direct object reference as value found")
            return False

    # Methods to replace values of specific nodes
    def AppendValueAtSpecificNode(self, nodeToAddValue, newValue):
        # Update graph with name
        currentValue = self.graph.nodes(data=True)[nodeToAddValue]['value']
        if currentValue == '':
            updatedValue = newValue
        else:
            updatedValue = currentValue + '|' + newValue
        self.graph.nodes(data=True)[nodeToAddValue]['value'] = updatedValue
        return True

    def ReplaceItemNameAtSpecificNode(self, nodeToAddName, newName):
        # Find Node
        node = self.FindItemWithValue(nodeToAddName)
        if node is not None:
            # Get list of edges from the node
            edgesFromNode = self.graph.edges(node, data=True)
            for startNode, endNode, edgeValues in edgesFromNode:
                # If an edge has the value ItemHasName, then we want to modify the end node
                if edgeValues['value'] == 'ItemHasName':
                    # Update graph with name
                    self.graph.nodes(data=True)[endNode]['value'] = newName
                    return True
        else:
            print("No node with direct object reference as value found")
            return False


class PropertyGraph(object):
    # Constructor
    def __init__(self, graphNumber):
        self.graphNumber = graphNumber
        if graphNumber is not None:
            self.graph = generatePropGraph(self.graphNumber)
        else:
            self.graph = None

    # Generic append method based on whatever target is passed in
    def __append(self, target, newValue):
        currentValue = self.graph.nodes(data=True)[target + str(self.graphNumber)]['value']
        if currentValue == '':
            updatedValue = newValue
        else:
            updatedValue = currentValue + '|' + newValue
        self.graph.nodes(data=True)[target + str(self.graphNumber)]['value'] = updatedValue

    # Generic replace method based on whatever target is passed in
    def __replace(self, target, newValue):
        self.graph.nodes(data=True)[target + str(self.graphNumber)]['value'] = newValue

    # Append/replace methods for each node value in Property Graph
    def appendPropValue(self, newValue):
        self.__append('Property', newValue)

    def replacePropValue(self, newValue):
        self.__replace('Property', newValue)

    def appendPropAdj(self, newAdjective):
        self.__append('PropertyAdjective', newAdjective)

    def replacePropAdj(self, newValue):
        self.__replace('PropertyAdjective', newValue)

    def appendPropSecObj(self, newSecondaryObject):
        self.__append('PropertySecondaryObject', newSecondaryObject)

    def replacePropSecObj(self, newSecondaryObject):
        self.__replace('PropertySecondaryObject', newSecondaryObject)

    def appendPropTertObj(self, newTertiaryObject):
        self.__append('PropertyTertiaryObject', newTertiaryObject)

    def replacePropTertObj(self, newTertiaryObject):
        self.__replace('PropertyTertiaryObject', newTertiaryObject)

    def appendPropDegree(self, newDegree):
        self.__append('PropertyDegree', newDegree)

    def replacePropDegree(self, newDegree):
        self.__replace('PropertyDegree', newDegree)

    def appendPropCompTarget(self, newCompTarget):
        self.__append('PropertyCompTarget', newCompTarget)

    def replacePropCompTarget(self, newCompTarget):
        self.__replace('PropertyCompTarget', newCompTarget)

    # Method to get the type of graph
    # def getTypeOfNode(self, node):
    #    return self.graph.nodes[node]['value']

    # Method to find a node containing a given value
    def FindPropertyWithValue(self, valueToFind):
        if self.graph is not None:
            # iterate through all graph nodes
            for node, values in self.graph.nodes.data():
                # If the current Node's value = the value passed in
                if values['value'] == valueToFind:
                    return node
        return None


class ActionGraph(object):
    # Constructor
    def __init__(self, graphNumber):
        self.graphNumber = graphNumber
        if graphNumber is not None:
            self.graph = generateActionGraph(self.graphNumber)
        else:
            self.graph = None

    # Generic append method based on whatever target is passed in
    def __append(self, target, newValue):
        currentValue = self.graph.nodes(data=True)[target + str(self.graphNumber)]['value']
        if currentValue == '':
            updatedValue = newValue
        else:
            updatedValue = currentValue + '|' + newValue
        self.graph.nodes(data=True)[target + str(self.graphNumber)]['value'] = updatedValue

    # Generic replace method based on whatever target is passed in
    def __replace(self, target, newValue):
        self.graph.nodes(data=True)[target + str(self.graphNumber)]['value'] = newValue

    # Append/replace methods for each node value in Property Graph
    def appendActionValue(self, newValue):
        self.__append('Action', newValue)

    def replaceActionValue(self, newValue):
        self.__replace('Action', newValue)

    def appendActionVerb(self, newVerb):
        self.__append('ActionVerb', newVerb)

    def replaceActionVerb(self, newValue):
        self.__replace('ActionVerb', newValue)

    # Method to get the type of graph
    # def getTypeOfNode(self, node):
    #    return self.graph.nodes[node]['value']

    # Method to find a node containing a given value
    def FindActionWithValue(self, valueToFind):
        if self.graph is not None:
            # iterate through all graph nodes
            for node, values in self.graph.nodes.data():
                # If the current Node's value = the value passed in
                if values['value'] == valueToFind:
                    return node
        return None


# Modifier_PP (adv will need a different graph)
class ModifierPPGraph(object):
    # Constructor
    def __init__(self, graphNumber):
        self.graphNumber = graphNumber
        if graphNumber is not None:
            self.graph = generateModPPGraph(self.graphNumber)
        else:
            self.graph = None

    # Generic append method based on whatever target is passed in
    def __append(self, target, newValue):
        currentValue = self.graph.nodes(data=True)[target + str(self.graphNumber)]['value']
        if currentValue == '':
            updatedValue = newValue
        else:
            updatedValue = currentValue + '|' + newValue
        self.graph.nodes(data=True)[target + str(self.graphNumber)]['value'] = updatedValue

    # Generic replace method based on whatever target is passed in
    def __replace(self, target, newValue):
        self.graph.nodes(data=True)[target + str(self.graphNumber)]['value'] = newValue

    # Append/replace methods for each node value in Property Graph
    def appendModPPValue(self, newValue):
        self.__append('ModPP', newValue)

    def replaceModPPValue(self, newValue):
        self.__replace('ModPP', newValue)

    def appendModPPPrep(self, newPreposition):
        self.__append('ModPPPrep', newPreposition)

    def replaceModPPPrep(self, newPreposition):
        self.__replace('ModPPPrep', newPreposition)

    # Method to get the type of graph
    # def getTypeOfNode(self, node):
    #    return self.graph.nodes[node]['value']

    # Method to find a node containing a given value
    def FindModWithValue(self, valueToFind):
        if self.graph is not None:
            # iterate through all graph nodes
            for node, values in self.graph.nodes.data():
                # If the current Node's value = the value passed in
                if values['value'] == valueToFind:
                    return node
        return None

