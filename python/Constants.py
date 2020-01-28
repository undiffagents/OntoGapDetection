# GRAPH GENERATION

# Item Graph nodes and edge
CONST_ITEM_NODE = 'Item'
CONST_ITEM_NAME_NODE = 'ItemName'
CONST_ITEM_AFFORDANCE_NODE = 'ItemAffordance'
CONST_ITEM_DESCRIPTION_NODE = 'ItemDescription'
CONST_ITEM_ROLE_NODE = 'ItemRole'

CONST_ITEM_HAS_NAME_EDGE = 'ItemHasName'
CONST_ITEM_HAS_AFFORDANCE_EDGE = 'ItemHasAffordance'
CONST_ITEM_HAS_DESCRIPTION_EDGE = 'ItemHasDescription'
CONST_ITEM_HAS_ROLE_EDGE = 'ItemHasRole'

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

# Assorted keys and edge names
CONST_NODE_VALUE_KEY = 'value'

CONST_IS_MEMBER_EDGE = 'IsMemberOf'
CONST_HAS_MEMBER_EDGE = 'HasMember'
CONST_IS_EQUIVALENT_EDGE = 'IsEquivalentTo'
CONST_HAS_A_EDGE = 'HasA'
CONST_IS_PART_OF_EDGE = 'IsPartOf'
CONST_IS_EDGE = 'Is'
CONST_PERFORMS_EDGE = 'Performs'
CONST_IS_PERFORMED_EDGE = 'IsPerformedBy'
CONST_HAS_TARGET_EDGE = 'HasTarget'
CONST_IS_TARGET_EDGE = 'IsTargetOf'
CONST_MODIFIES_VERB_EDGE = 'ModifiesVerb'
CONST_MODIFIES_OBJECT_EDGE = 'ModifiesObject'
CONST_IS_MODIFIED_EDGE = 'isModifiedBy'
CONST_TRIGGERS_EDGE = 'triggers'
CONST_TRIGGERED_BY_EDGE = 'isTriggeredBy'


# LINE CATEGORIZATION

CONST_HEADER_LINE_SYMBOL = '['
CONST_HEADER_LINE_TAG = 'header'
CONST_CONDITIONAL_LINE_SYMBOL = '=>'
CONST_CONDITIONAL_LINE_TAG = 'conditional'
CONST_QUESTION_LINE_SYMBOL = 'QUESTION'
CONST_QUESTION_LINE_TAG = 'question-tag'
CONST_NEGATION_LINE_SYMBOL = 'NOT'
CONST_NEGATION_LINE_TAG = 'negation-tag'
CONST_INSTRUCTION_HEADER_TAG = 'instruction-header'
CONST_QUESTION_HEADER_TAG = 'question-header'
CONST_NEGATION_HEADER_TAG = 'negation-header'
CONST_THEN_HEADER_TAG = 'then-header'
CONST_IF_HEADER_TAG = 'if-header'
CONST_INSTRUCTION_TAG = 'instruction'
CONST_QUESTION_TAG = 'question'
CONST_NEGATION_TAG = 'negation'

# CONDITIONAL HANDLING
CONST_IF_TAG = 'if'
CONST_THEN_TAG = 'then'


# DRS TAGS
CONST_PRED_VERB_BE = 'be'
CONST_PRED_SUBJ_NAMED = 'named'
CONST_PRED_VERB_HAVE = 'have'
CONST_PRED_GROUP_DESC = 'GROUP'
CONST_PRED_MOD_TAG = 'mod'
