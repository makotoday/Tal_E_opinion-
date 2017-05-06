# -*- coding: utf-8 -*-
"""
Created on Thu May  4 21:52:58 2017

@author: Sébastien
"""
import re
from bs4 import BeautifulSoup




def chargement(htmlsrc):
    soup = BeautifulSoup(htmlsrc,"lxml")
    com = []
    notes = []
    # tout les commentaires
    for p in soup.find_all('p'):
        if(p.get('itemprop',0)=='description'):
          com.append(p.get_text())
          
    #toute les notes
    for p in soup.find_all('span'):
        note = p.get('content',0)
        if(note!=0): 
            notes.append(note)
    return com,notes
    
# ---------- bibliothèque de mots à enrichir ------------- #

def biblioMotPositif():
    # verbes du premier groupe positifs
    verbePosPrem = ['aimer','adorer','interesser','innover']
    # liste d'adjectifs positifs
    adjs = ['honorable','agréable','spectaculaire','émouvant','bien','bon','bonne','heureux','sympa','super']
    motsPos = []
    motsPos.append(verbePosPrem)
    motsPos.append(adjs)
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
    negavar = ['aucun', 'aucune']
    for j in range(0,len(negainv)):
            if(negainv[j] in phrase):
                return True
    for k in range(0,len(negavar)):
        if(negavar[k] in phrase):
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
    
    return False

def containMot(mot, phrase):
    for i in range(0,len(phrase)):
        if(mot==phrase[i]): return True
    return False  
    
    
    #---------------Début méthode permettant l'apprentissage------------------#
#la methode calcule le pourcentage de phrase  négatif dans le commentaire 
def ProbNCommentaire(commentaire):
    nbligne = len(commentaire); 
    nb_ligneN = 0.0
    for  phrase in commentaire: 
        if(negationDansPhrase(phrase)==True):
            nb_ligneN=nb_ligneN+1
    return (nb_ligneN/nbligne)
    
#-------------Fin méthode  permettant l'apprentissage----------------------#

