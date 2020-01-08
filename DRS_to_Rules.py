import re

def lowercase(s):
    return s[:1].lower() + s[1:] if s else ''

def parseVarLine(line):
    return ((line.split('[')[1]).split(']')[0]).split(',')

def parseObjectLine(line):
    line=(line.split('(')[1]).split(',')
    return [line[0],line[1]]

def lookupObject(letter):
    for pair in objs:
        if pair[0] == letter: return pair[1].lower()
    return False

def subObject(letter,string):
    for pair in objs:
        if pair[0] == letter: unnamedFacts.remove(pair[1]) ; pair[1] = string ; return True
    return False

def lookupProperty(letter):
    for pair in props:
        if pair[0] == letter: return pair[1]
    raise

def parsePropertyLine(line):
    line=(line.split('(')[1]).split(',')
    return(line[0],line[1])

def parsePredicateLine(line):
    line=(line.split('(',1)[1]).split(',')[1:]
    line[2]=line[2].split(')')[0]
    if len(line[1]) > 1: line[-2]=(line[-2].split('(')[1]).split(')')[0]
    if len(line[1]) > 1 and line[0] == 'be':
        a = lookupObject(line[2])
        subObject(line[2],lowercase(line[1]))
        return '{}({})'.format(a,line[1])
    elif line[0] == 'be': 
        b = lookupObject(line[2])
        a = lookupObject(line[1])
        if not b: 
            return 'hasProperty({},{})'.format(a.capitalize(),lookupProperty(line[2]).capitalize())
        else:
            rules.append('{}(X) => {}(X)'.format(a,b)) ; head = [] ; body = []
    else:
        return '{}({},{})'.format(line[0],lookupObject(line[1]).capitalize(),lookupObject(line[2]).capitalize())

def flipSide(antecedent,consequent):
    if not antecedent and not consequent: addAllFacts() ; antecedent = True
    elif antecedent: consequent = True ; antecedent = False
    else: antecedent = True ; consequent = False
    return antecedent,consequent

def addAllFacts():
    for pred in preds:
        facts.append(pred)

def addRule():
    pass

if __name__ == "__main__":
    varlist = []
    objs = []
    preds = []
    props = []
    
    facts = []
    rules = []
    head = []
    body = []
    
    drsfile = open("DRS.txt","r")
    antecedent = False
    consequent = False
    unnamedFacts = []
    
    for line in drsfile:
        if not ' ' in line:
            if 'object'in line:
                objs.append(parseObjectLine(line))
                unnamedFacts.append(objs[-1][1])
            elif 'named' in line or 'string' in line:
                preds.append(parsePredicateLine(line))
    
    drsfile.seek(0)
    
    for fact in unnamedFacts:
        preds.append('{}({})'.format(fact,fact.capitalize()))
    
    for line in drsfile:
        if '[' in line:
            varlist.extend(parseVarLine(line))
            if ' ' in line: 
                antecedent,consequent = flipSide(antecedent,consequent)
                if antecedent: 
                    if len(head) > 0 and len(body) > 0: rules.append('{} => {}'.format(','.join(head),','.join(body))) 
                    head = [] ; body = []
        if 'object' in line and ' ' in line:
            objs.append(parseObjectLine(line)) 
        elif 'property' in line:
            props.append(parsePropertyLine(line))
        elif 'predicate' in line and not ('named' in line or 'string' in line):
            if not antecedent and not consequent: preds.append(parsePredicateLine(line))
            elif antecedent: head.append(parsePredicateLine(line))
            else: body.append(parsePredicateLine(line))
    
    if len(head) > 0 and len(body) > 0: rules.append('{} => {}'.format(','.join(head),','.join(body)))
    
    drsfile.close()
    
    rulesfile = open("Rules.txt","w")
    
    rulesfile.write("Facts:\n")
    
    for fact in facts:
        rulesfile.write('{}\n'.format(fact))
    
    rulesfile.write('\nRules:\n')
    
    for rule in rules:
        rulesfile.write('{}\n'.format(rule))
    
    rulesfile.close()