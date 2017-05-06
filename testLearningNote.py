# -*- coding: utf-8 -*-
"""
Created on Fri May  5 23:50:59 2017

@author: Sébastien
"""

# Creation d'un corpus avec pour chaque mot positif ou négatif un poids

def addToCorpus(comment, note, corpus):
    
    for i in range(0,len(comment)):
        if(corpus[comment[i]]!=None):
            corpus[comment[i]] += note/5
        # mylist.append(notes[i]* comments.count(comments[i]))
        #calcul probabilité et lissage :
    return corpus
    
def initCorpus(motPos, motNeg):
    corpus = {} # creation d'un dictionnaire avec des poids sur les mots
    for typePos in enumerate(motPos):
        for mot in enumerate(typePos):
            corpus[mot] = 5;# poids de base d'un mot +
    
    for typeNeg in enumerate(motNeg):
        for mot in enumerate(typeNeg):
            corpus[mot] = 0;# poids de base d'un mot -
            
def corpusToproba(corpus):
    sommePoids = 0
    for i in range(0,len(corpus)):
        somme += corpus[i]

    