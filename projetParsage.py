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
    motsNegPrem = ['détester','plomber']
    #liste d'adjectif negatis
    adjs = ['défault','déception','décevant','mauvais','nul']
    motsNeg = []
    motsNeg.append(motsNegPrem)
    motsNeg.append(adjs)
    return motsNeg
    
# mots précédant appuyant l'adjectif (augmente le poids)
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
    # la phrase non tokenisé :
    phr = ""
    for p in phrase:
        phr = phr+str(p)+' '
    #present [:-2] enleve les 2 derniers caractères (er)
    regex = re.compile("(.*?)"+verbe[:-2]+"(e|es|ent|ons|ez|ent).*?", re.I)
    match_obj = re.match(regex, phr)
    if match_obj!= None: return True
    #participe passée    
    regex = re.compile("(.*?)"+verbe[:-2]+"(é|ée|és|ées).*?",re.I)
    match_obj = re.match(regex, phr)
    if match_obj!= None:       
        return True
 # what is captured by the brackets
#    mot = match_obj.string
#    preceding = match_obj.group(1)
#    suffix = match_obj.group(2)
    
    return False

def containMot(mot, phrase):
    for i in range(0,len(phrase)):
        if(mot==phrase[i]): return True
    return False   

def analyseComment(comment):
    motsPos = biblioMotPositif()
    motsNeg = biblioMotNegatif()
    evalu = 0
    # test negation
    for phrase  in enumerate (comment):
        for verbe in enumerate(motsPos[0]):
            if(containVerbePrem(verbe[1],phrase)):
                evalu+=1
        for verbe2 in enumerate(motsNeg[0]):
            if(containVerbePrem(verbe2[1],phrase)):
                evalu-=1
        for adj in enumerate(motsPos[1]):
            if(containMot(adj[1],phrase)):
                evalu+=1
        for adj2 in enumerate(motsNeg[1]):
            if(containMot(adj2[1],phrase)):
                evalu-=1
    return evalu
            
if __name__=="__main__":
    
    # pages allocine
    sources = ["http://www.allocine.fr/film/fichefilm-226739/critiques/spectateurs/",
    "http://www.allocine.fr/film/fichefilm-229678/critiques/spectateurs/",
    "http://www.allocine.fr/film/fichefilm-249110/critiques/spectateurs/"]
    
    comments = []
    notes = []
    for i in range(0,len(sources)):
        sock = urllib.request.urlopen(sources[i])
        src = sock.read()
        sock.close()
        commentsFilm, notesFilm = chargement(src)
        comments+=commentsFilm
        notes+= notesFilm
        
    
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

    i = 0;
    for comment in commentsTok:
        evalcom = 0;
        for phrase in comment:
            evalcom += analyseComment(phrase)
        print("comment"+str(i)+"  :"+str(evalcom)+ " vs note :"+str(notes[i]))
        i+=1
