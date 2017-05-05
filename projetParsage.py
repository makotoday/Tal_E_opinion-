# -*- coding: utf-8 -*-
"""
Created on Thu May  4 21:52:58 2017

@author: Sébastien
"""

import urllib
import fonctionsTokenise as ftok
import re
from bs4 import BeautifulSoup




def chargement(htmlsrc):
    soup = BeautifulSoup(htmlsrc,"lxml")
    
    # tout les commentaires
    for p in soup.find_all('p'):
        if(p.get('itemprop',0)=='description'):
          comments.append(p.get_text())
          
    #toute les notes
    for p in soup.find_all('span'):
        note = p.get('content',0)
        if(note!=0): 
            notes.append(note)
    return comments,notes
    
# ---------- bibliothèque de mots à enrichir ------------- #

def biblioMotPositif():
    # verbes du premier groupe positifs
    verbePosPrem = ['aimer','adorer','interesser','innover']
    # liste d'adjectifs positifs
    adjs = ['honorable','agréable','spectaculaire','émouvant','bien','bon','bonne','heureux','sympa','super']
    autres = ['divertir']
    motsPos = []
    motsPos.append(verbePosPrem)
    motsPos.append(adjs)
    motsPos.append(autres)
    return motsPos
    
def biblioMotNegatif():
    motsNegPrem = []
    motsNegPrem.appends('détester','plomber')
    #liste d'adjectif negatis
    adjs = ['défault','déception','décevant','mauvais','nul']
    motsNeg = []
    motsNeg.append(motsNegPrem)
    motsNeg.append(adjs)
    return motsNeg
    
# mots précédant appuyant l'adjectif
def EvalmotAppuie():
    motsAppFort = ['trés','sacré','vraiment']
    motsAppMoyen = ['assez','plutôt']    

    # doit reconnaitre si une phrase contient une négation ou pas
def negationDansPhrase(phrase):
    negainv = ['pas','trop','sans']
    negavar = ['aucun']
    for j in range(0,len(negainv)), k in range(0,len(negavar)):
            if(negainv[j] in phrase or negavar[k] in phrase[i]):
                return True
    
    return False
#aucune deception sans innovation
# expr positif vaut le coup

# --------------fin bibliotheque --------------------#

def containVerbePrem(verbe, phrase):
    verbe = verbe[:-2] #enleve les 2 derniers caractères
    regex = re.compile(".*? "+verbe+"(e|es|ent|ons|ez|ent).*?", re.I)
    phr = ""
    for p in phrase:
        phr = phr+p+' '
    match_obj = re.match(regex, phr)
    # what is captured by the brackets
#    mot = match_obj.string
#    preceding = match_obj.group(1)
#    suffix = match_obj.group(2)
    if match_obj!= None:
        print("contains the verb ’"+verbe+"er"+"’ in the present tense")

def testComment(comment):
    biblioMotPositif();
    # test negation
    for phrase  in enumerate (comment):
        phrase
            
if __name__=="__main__":
    
    # page allocine
    sock = urllib.request.urlopen("http://www.allocine.fr/film/fichefilm-226739/critiques/spectateurs/")
    src = sock.read()
    sock.close()
    comments = []
    notes = []
    comments, notes = chargement(src)
    
    commentsTok = []
    for c in enumerate(comments): 
        cstr = str(c)
        phrases = ftok.segment_into_sents(cstr)
        sentsTok = []
        for i in range(0,len(phrases)):   
            phrases[i] = ftok.normalise(phrases[i],"fr")
            phrases[i] = ftok.tokenise(phrases[i],"en")
            sentsTok.append(phrases[i])
        commentsTok.append(sentsTok)

    for comment in commentsTok:
        for phrase in comment:
            containVerbePrem('aller',phrase)
        
    