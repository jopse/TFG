#!/bin/python
import math
import numpy as np
import fileinput as fin
import sys
from itertools import groupby


class NodoAbstracto: pass

class Hoja(NodoAbstracto):
    def __init__(self, clase):
        self.clase = clase

class Nodo(NodoAbstracto):
    def __init__(self, atributo):
        self.atributo = atributo
        self.ramas = list()
    def newBranch(self, valor, nodo):
        self.ramas.append((valor, nodo))


def id3(inst, default):
    if len(inst) == 0:
        return Hoja(default)
    elif noAtrib(inst):
        return Hoja(mayoritaria(inst))
    elif len(clases(inst)) == 1:
        return Hoja(clases(inst)[0])
    else:
        A = chooseAttr(inst)
        nodo = Nodo(A)
        for i in listValues(A, inst):
            dinst = clear(A, pickinstancias(inst,A,i))
            nodo.newBranch(i, id3(dinst,default))
        return nodo


def chooseAttr(insts):
    def entropAttr(atrib):
        def exp(v): return nij(atrib,v) / len(insts) * entropVal(atrib,v)
        return sum([exp(v) for v in listValues(atrib, insts)])

    def entropVal(a, v):
        def exp(c): return nijc(a,v,c)/nij(a,v)*math.log(nijc(a,v,c)/nij(a,v),2)
        return -sum([exp(c) for c in clases(pickinstancias(insts,a,v))])

    def nij(a, v): return len(pickinstancias(insts, a, v))
    def nijc(a, v, c): return len([x for x in pickinstancias(insts, a, v) if x[1] == c])

    atributos = range(len(insts[0][0]))
    entr = [entropAttr(x) for x in atributos]
    return entr.index(min(entr))


def parseData(filename, classCol):
    filedata = transpose([line.replace('\n','').split(', ') for line in fin.input(filename)])
    clases = filedata[classCol]
    data = transpose(filedata[:classCol] + filedata[classCol+1:])
    return list(zip(data, clases))


def mayoritaria(insts):
    clases = dict()
    for a,c in insts:
        if c in clases: clases[c] += 1
        else: clases[c] = 1
    vmax = 0
    cmax = list(clases.keys())[0]
    for k,v in clases.items():
        if v > vmax:
            vmax = v
            cmax = k
    return cmax


def clear(atrib, insts): return [(x[0][:atrib] + x[0][atrib+1:], x[1]) for x in insts]
def clases(insts): return list(set([x[1] for x in insts]))
def listValues(atrib, insts): return set([x[0][atrib] for x in insts])
def pickinstancias(insts, atrib, value): return [x for x in insts if x[0][atrib] == value]
def transpose(lista): return np.asarray(lista).T.tolist()
def noAtrib(insts): return len(insts) > 0 and sum([len(x[0]) for x in insts]) == 0

def toString(arbol):
    s = ' '
    if type(arbol).__name__ == 'Nodo':
        s += str(arbol.atributo) + '{'
        for v, x in arbol.ramas: s += str(v) + ':' + toString(x) + ','
        s += '} '
    elif type(arbol).__name__ == 'Hoja':
        s += '#' + str(arbol.clase) + '# '
    return s

def evalua(arbol, ejemplo):
    if type(arbol).__name__ == 'Nodo':
        valor = ejemplo[0][arbol.atributo]
        darbol = arbol.ramas[0][1]
        for v,a in arbol.ramas:
            if v == valor: darbol = a
        return evalua(darbol, ejemplo)
    elif type(arbol).__name__ == 'Hoja':
        return arbol.clase

def main():
    if len(sys.argv) >= 3:
        instancias = parseData(sys.argv[1], int(sys.argv[3]))
        arbol = id3(instancias, clases(instancias)[0])
        print(toString(arbol))

        if len(sys.argv) == 4:
            aciertos = 0
            fallos = 0
            test = parseData(sys.argv[2], int(sys.argv[3]))
            for ejemplo in test:
                claseP = evalua(arbol, ejemplo)
                if claseP == ejemplo[1]:
                    aciertos += 1
                else:
                    fallos += 1
            print('aciertos: ' + str(aciertos) + ', fallos: ' + str(fallos))



if __name__ == '__main__':
    main()
