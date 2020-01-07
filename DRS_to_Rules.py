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
        if pair[0] == letter: pair[1] = string ; return True
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
        print(line)
        return '{}({})'.format(a,line[1])
    elif line[0] == 'be': 
        b = lookupObject(line[2])
        a = lookupObject(line[1])
        if not b: 
            return 'hasProperty({},{})'.format(a.capitalize(),lookupProperty(line[2]).capitalize())
        else:
            print('{}(X) => {}(X)'.format(a,b))    
    else:
        return '{}({},{})'.format(line[0],lookupObject(line[1]).capitalize(),lookupObject(line[2]).capitalize())  

varlist = []
objs = []
preds = []
props = []

facts = []
rules = []

drsfile = open("DRS.txt","r")
antecedent = False
consequent = False

for line in drsfile:
    if '[' in line:
        varlist.extend(parseVarLine(line))
        if ' ' in line: antecedent = True ; consequent = False
    elif '=>' in line:
        antecedent = False ; consequent = True
    elif 'object' in line:
        objs.append(parseObjectLine(line))
    elif 'property' in line:
        props.append(parsePropertyLine(line))
    elif 'predicate' in line:
        preds.append(parsePredicateLine(line))

print(objs)
print(preds)
print(facts)
print(rules)

drsfile.close()
