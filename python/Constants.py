# GRAPH GENERATION

# Item Graph nodes and edge
CONST_ITEM_NODE = 'Item'
CONST_ITEM_NAME_NODE = 'ItemName'
CONST_ITEM_AFFORDANCE_NODE = 'ItemAffordance'
CONST_ITEM_DESCRIPTION_NODE = 'ItemDescription'
CONST_ITEM_ROLE_NODE = 'ItemRole'
CONST_ITEM_OP_NODE = 'ItemOp'
CONST_ITEM_COUNT_NODE = 'ItemCount'

CONST_ITEM_HAS_NAME_EDGE = 'ItemHasName'
CONST_ITEM_HAS_AFFORDANCE_EDGE = 'ItemHasAffordance'
CONST_ITEM_HAS_DESCRIPTION_EDGE = 'ItemHasDescription'
CONST_ITEM_HAS_ROLE_EDGE = 'ItemHasRole'
CONST_ITEM_HAS_OP_EDGE = 'ItemHasOp'
CONST_ITEM_HAS_COUNT_EDGE = 'ItemHasCount'

# Property Graph nodes and edges
CONST_PROP_NODE = 'Property'
CONST_PROP_ADJECTIVE_NODE = 'PropertyAdjective'
CONST_PROP_SEC_OBJECT_NODE = 'PropertySecondaryObject'
CONST_PROP_TERT_OBJECT_NODE = 'PropertyTertiaryObject'
CONST_PROP_DEG_NODE = 'PropertyDegree'
CONST_PROP_COMP_TARGET_NODE = 'PropertyCompTarget'

CONST_PROP_HAS_ADJECTIVE_EDGE = 'PropertyHasAdjective'
CONST_PROP_HAS_SEC_OBJECT_EDGE = 'PropertyHasSecondaryObject'
CONST_PROP_HAS_TERT_OBJECT_EDGE = 'PropertyHasTertiaryObject'
CONST_PROP_HAS_DEG_EDGE = 'PropertyHasDegree'
CONST_PROP_HAS_COMP_TARGET_EDGE = 'PropertyHasCompTarget'

# Action Graph nodes and edges
CONST_ACTION_NODE = 'Action'
CONST_ACTION_VERB_NODE = 'ActionVerb'

CONST_ACTION_HAS_VERB_EDGE = 'ActionHasVerb'

# Modifier Graph nodes and edges
CONST_MODPP_NODE = 'ModPP'
CONST_MODPP_PREP_NODE = 'ModPPPrep'

CONST_MODPP_HAS_PREP_EDGE = 'ModPPHasPrep'

# Relation Graph node
CONST_RELATION_NODE = "RelationOf"

CONST_RELATION_IS_ATTRIBUTE_EDGE = "IsAttribute"
CONST_RELATION_HAS_PARENT_EDGE = "HasParent"
CONST_RELATION_IS_PARENT_EDGE = "IsParent"
CONST_RELATION_HAS_ATTRIBUTE_EDGE = "HasAttribute"

# Conditional Graph node
CONST_CONDITIONAL_NODE = "Conditional"

CONST_TRUE_CONDITION_OF_EDGE = "TrueConditionOf"
CONST_HAS_TRUE_CONDITION_EDGE = "HasTrueCondition"
CONST_FALSE_CONDITION_OF_EDGE = "FalseConditionOf"
CONST_HAS_FALSE_CONDITION_EDGE = "HasFalseCondition"
CONST_CONSEQUENCE_OF_EDGE = "ConsequenceOf"
CONST_HAS_CONSEQUENCE_EDGE = "HasConsequence"

# Assorted keys and edge names
CONST_NODE_VALUE_KEY = 'value'

CONST_IS_MEMBER_EDGE = 'IsMemberOf'
CONST_HAS_MEMBER_EDGE = 'HasMember'
CONST_IS_EQUIVALENT_EDGE = 'IsEquivalentTo'
CONST_HAS_A_EDGE = 'HasA'
CONST_IS_PART_OF_EDGE = 'IsPartOf'
CONST_IS_EDGE = 'Is'
CONST_IS_SOURCE_EDGE = 'IsSourceOf'
CONST_HAS_SOURCE_EDGE = 'HasSource'
CONST_HAS_TARGET_EDGE = 'HasTarget'
CONST_IS_TARGET_EDGE = 'IsTargetOf'
CONST_MODIFIES_VERB_EDGE = 'ModifiesVerb'
CONST_MODIFIES_OBJECT_EDGE = 'ModifiesObject'
CONST_IS_MODIFIED_EDGE = 'isModifiedBy'
CONST_TRIGGERS_IF_TRUE_EDGE = 'triggersIfTrue'
CONST_TRIGGERS_IF_FALSE_EDGE = 'triggersIfFalse'
CONST_TRIGGERED_BY_EDGE = 'isTriggeredBy'


# LINE CATEGORIZATION

CONST_HEADER_LINE_SYMBOL = '['
CONST_HEADER_LINE_TAG = 'header'
CONST_CONDITIONAL_LINE_SYMBOL = '=>'
CONST_CONDITIONAL_LINE_TAG = 'conditional'
CONST_QUESTION_LINE_SYMBOL = 'QUESTION'
CONST_QUESTION_LINE_TAG = 'question-tag'
CONST_NEGATION_LINE_SYMBOL = 'NOT'
CONST_NEGATION_LINE_TAG = 'not-tag'
CONST_NECESSITY_LINE_SYMBOL = 'MUST'
CONST_NECESSITY_LINE_TAG = 'must-tag'
CONST_INSTRUCTION_HEADER_TAG = 'instruction-header'
CONST_QUESTION_HEADER_TAG = 'question-header'
CONST_NEGATION_HEADER_TAG = 'not-header'
CONST_NECESSITY_HEADER_TAG = 'must-header'
CONST_THEN_HEADER_TAG = 'then-header'
CONST_IF_HEADER_TAG = 'if-header'
CONST_IF_NEGATION_HEADER_TAG = 'if-not-header'
CONST_INSTRUCTION_TAG = 'instruction'
CONST_QUESTION_TAG = 'question'
CONST_NEGATION_TAG = 'negation'
CONST_NECESSITY_TAG = 'must-tag'
CONST_JUNK_LINE_TAG = 'junk-tag'

# CONDITIONAL HANDLING
CONST_IF_TAG = 'if'
CONST_IF_NEGATION_TAG = 'if-not'
CONST_THEN_TAG = 'then'
CONST_CONSEQUENCE_FLAG = 'CONSEQUENCEFLAG'

# DRS TAGS
CONST_PRED_VERB_BE = 'be'
CONST_PRED_SUBJ_NAMED = 'named'
CONST_PRED_VERB_HAVE = 'have'
CONST_PRED_GROUP_DESC = 'GROUP'
CONST_PRED_MOD_TAG = 'mod'

# REGEX SEARCH STRINGS
CONST_REGEX_ITEM_NODE = "Item\\d+"
CONST_REGEX_PROPERTY_NODE = "Property\\d+"
