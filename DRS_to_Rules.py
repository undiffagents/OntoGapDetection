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

def falseNegCheck(name):
    for pair in objs:
        if pair[1] == name: return pair[1].lower()
    return False    

def isFact(term):
    for fact in facts:
        fact = fact.split('(')[0]
        if fact == term: return True
    return False

def lookupTerm(letter):    
    a = ''
    term = lookupObject(letter)
    if not term: return term
    for obj in objs:
        if obj[1] == term: 
            a = obj[1]
            break
    if a in namedFacts:
        a = namedFacts[term]
    newatom = '{}({})'.format(a,obj[0])
    if a == '': newatom = '{}({})'.format(obj[1],obj[0])        
    if antecedent: body.append(newatom)
    else: head.append(newatom)
    unGround.append(newatom)
    return obj[0]

def subObject(letter,string):
    for pair in objs:
        if pair[0] == letter: unnamedFacts.remove(pair[1]) ; namedFacts[string] = pair[1] ; pair[1] = string ; return True
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
        b = line[1]
        a = lookupObject(line[2])
        if not a:
            a = falseNegCheck(line[1].lower())
            b = lookupProperty(line[2])
            return 'hasProperty({},{})'.format(a,b)
        else:
            subObject(line[2],lowercase(b))
            return '{}({})'.format(a,b)
    elif line[0] == 'be': 
        b = lookupObject(line[2])
        a = lookupObject(line[1])   
        if not b: 
            return 'hasProperty({},{})'.format(lookupTerm(line[1]),lookupProperty(line[2]))
        else:
            rules.append('{}({}) => {}({})'.format(a,line[1],b,line[1]))
            datalog.append('{}({}) :- {}({}).'.format(b,line[1],a,line[1]))
            queries.append('{}({})?'.format(b,line[1]))
            body = [] ; head= []
            return
    elif not antecedent and not consequent:
        a = lookupObject(line[1])
        b = lookupObject(line[2])
        return '{}({},{})'.format(line[0],a,b)
    else:
        a = lookupTerm(line[1])
        b = lookupTerm(line[2])     
        return '{}({},{})'.format(line[0],a,b)

def flipSide(antecedent,consequent):
    if not antecedent and not consequent: addAllFacts() ; antecedent = True
    elif antecedent: consequent = True ; antecedent = False
    else: antecedent = True ; consequent = False
    return antecedent,consequent

def addAllFacts():
    for pred in preds:
        facts.append(pred)

def extractVars(atom):
    return ((atom.split('(')[1]).split(')')[0]).split(',')

def determineVars(lists):
    vrs = []
    for atom in lists:
        vrs.extend(extractVars(atom))
    return set(vrs)


def checkVars(atom):
    vrsBody = determineVars(body)
    vrsHead = determineVars(head)
    while not vrsHead.issubset(vrsBody):
        
        for atom in head:
            b = set(extractVars(atom))
            if b.issubset(vrsBody):
                print()
            else:
                head.remove(atom)
                body.append(atom)
        
        vrsBody = determineVars(body)
        vrsHead = determineVars(head)        

if __name__ == "__main__":
    varlist = []
    unGround = []
    objs = []
    preds = []
    props = []
    
    facts = []
    rules = []
    datalog = []
    queries = []
    body = []
    head= []
    
    drsfile = open("DRS.txt","r")
    antecedent = False
    consequent = False
    unnamedFacts = []
    namedFacts = {}
    
    for line in drsfile:
        if not ' ' in line:
            if 'object'in line:
                objs.append(parseObjectLine(line))
                unnamedFacts.append(objs[-1][1])
            elif 'named' in line or 'string' in line:
                preds.append(parsePredicateLine(line))
            elif 'property' in line:
                props.append(parsePropertyLine(line))
    
    drsfile.seek(0)
    
    for fact in unnamedFacts:
        preds.append('{}({})'.format(fact,fact))
    
    for line in drsfile:
        #print(line)
        if '[' in line:
            varlist.extend(parseVarLine(line))
            if ' ' in line: 
                antecedent,consequent = flipSide(antecedent,consequent)
                if antecedent: 
                    if len(body) > 0 and len(head) > 0: 
                        body = list(set(body)) ; head= list(set(head))
                        for a in body:
                            if a in head: head.remove(a)
                        rules.append('{} => {}'.format(','.join(body),','.join(head))) 
                        for atom in head:
                            datalog.append('{} :- {}.'.format(atom,','.join(body)))
                            queries.append('{}?'.format(atom))
                    body = [] ; head= []
        elif ' object' in line:
            objs.append(parseObjectLine(line)) 
        elif ' property' in line:
            props.append(parsePropertyLine(line))
        elif 'predicate' in line and not ('named' in line or 'string' in line):
            if not antecedent and not consequent: preds.append(parsePredicateLine(line))
            elif antecedent: body.append(parsePredicateLine(line))
            elif len(body) == 0 and len(head) == 0:  
                a = parsePredicateLine(line)
            elif len(body) > 0:
                a = parsePredicateLine(line)
                checkVars(a)
                head.append(a)
    
    if len(body) > 0 and len(head) > 0: 
        rules.append('{} => {}'.format(','.join(body),','.join(head)))
        for atom in head:
            datalog.append('{} :- {}.'.format(atom,','.join(body)))
            queries.append('{}?'.format(atom))
    
    drsfile.close()
    
    rulesfile = open("Rules.txt","w")
    datalogfile = open("datalog.dl","w")
    
    rulesfile.write("Facts:\n")
    datalogfile.write("%facts\n")

    for fact in facts:
        rulesfile.write('{}\n'.format(fact))
        datalogfile.write('{}.\n'.format(fact))
    
    rulesfile.write('\nRules:\n')
    datalogfile.write("\n%rules\n")
    
    for rule in rules:
        rulesfile.write('{}\n'.format(rule))
    for rule in datalog:
        datalogfile.write('{}\n'.format(rule))
    
    rulesfile.close()

    datalogfile.write("\n%queries\n")
    
    for question in queries:
        datalogfile.write('{}\n'.format(question))

    datalogfile.close()
