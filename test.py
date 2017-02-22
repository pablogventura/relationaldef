# -*- coding: utf-8 -*-
#!/usr/bin/env python   
from minion import is_isomorphic
from parser import stdin_parser
from minion import automorphisms, isomorphisms, is_isomorphic_to_any
from itertools import chain
from models import RelationalModel
from relations import Relation


class Counterexample(Exception):
    def __init__(self,ce):
        self.ce = ce

def main():
    t01 = Relation("T0",2)
    t02 = Relation("T0",2)
    r01 = Relation("R0",2)
    r01.add((0,0))
    r02 = Relation("R0",2)
    r02.add((0,0))
    g1=RelationalModel([0, 2],{'T0': t01, 'R0': r01})
    g2=RelationalModel([0, 6],{'T0': t02, 'R0': r02})

    
    print (is_isomorphic_to_any(g2,[g1],["R0"]))
        

class GenStack(object):
    def __init__(self, generator):
        self.stack = [generator]
    
    def add(self,generator):
        self.stack.append(generator)
    
    def next(self):
        result = None
        while result is None:
            try:
                result = next(self.stack[-1])
            except IndexError:
                raise StopIteration
            except StopIteration:
                del self.stack[-1]
        return result
            
        


def is_open_rel(model, target_rels):
    base_rels = tuple((r for r in model.relations if r not in target_rels))
    spectrum = sorted(model.spectrum(target_rels),reverse=True)
    size = spectrum[0]
    print ("Spectrum=%s"%spectrum)
    S = set()
    
    genstack = GenStack(model.substructures(size))

    while True:
        try:
            current = genstack.next()
        except StopIteration:
            break
        iso = is_isomorphic_to_any(current, S, base_rels)
        if iso:
            if not iso.iso_wrt(target_rels):
                raise Counterexample(iso)
        else:
            for aut in automorphisms(current,base_rels):
                if not aut.aut_wrt(target_rels):
                    raise Counterexample(aut)
            S.add(current)
            print("agrego %s" % current)
            try:
                size = next(x for x in spectrum if x < len(current)) # EL SIGUIENTE EN EL ESPECTRO QUE SEA MAS CHICO QUE LEN DE SUBUNIVERSE
                genstack.add(current.substructures(size))
            except StopIteration:
                # no tiene mas hijos
                pass
    print ("Diversity=%s"%len(S)) # TODO las k-diversidades por separado
    
    return True




if __name__ == "__main__":
    main()
