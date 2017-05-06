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
#-------------methode teste------------------------------------------------#
def testNegation(commentaire,tauxNegatif,note_commentaire):
    taux=ProbNCommentaire(commentaire)
    if(taux<tauxNegatif):
        print("bon commentaire\t TN:"+str(taux)+"\t Note C:"+str(note_commentaire))

        
def ImportList(pathfile):
      liste=[]
      mot_list=[]
      with open(pathfile, "r") as filepointer:
         for line in filepointer.readlines():
            if line.strip()=="": continue # ignore blank paragraphs
            new_line=line.strip(',')
            tmp=ftok.segment_into_sents(new_line.strip())            
            liste=tmp+liste # remove whitespace with strip()
         for mot in liste:
            tmp=ftok.normalise(mot,"fr")
            tmp=ftok.tokenise(tmp,"en")
            mot_list.append(tmp)
      return liste

def AnalyseComment2(comment,motsPos,motsNeg):
    prob_p=0
    prob_n=0
    mot_total=0
    for phrase in comment:
        mot_total+=len(phrase)
        for verbe in enumerate(motsPos[0]):
            if(containVerbePrem(verbe[1],phrase)):
                prob_p+=1
        for verbe2 in enumerate(motsNeg[0]):
            if(containVerbePrem(verbe2[1],phrase)):
                prob_n+=1
                
        for adj in enumerate(motsPos[1]):
            if(containMot(adj[1],phrase)):
                prob_p+=1
        for adj2 in enumerate(motsNeg[1]):
            if(containMot(adj2[1],phrase)):
                prob_n+=1
        for mot in enumerate(motsPos[2]):
            if(containMot(mot,phrase)):
                prob_p+=1
        for mot in enumerate(motsNeg[2]):
            if(containMot(mot,phrase)):
                prob_n+=1
                
    taux_p=prob_p/mot_total
    taux_n=prob_n/mot_total
    print("prob_p :"+str(prob_p)+"   prob_n  :"+str(prob_n))
    if(prob_p>prob_n):
        return True
    else :
        return False 

def AnalyseComment3(comment,motsPos,motsNeg):
    prob_p=0
    prob_n=0
    mot_total=0
    for phrase in comment:
        mot_total+=len(phrase)
        for verbe in enumerate(motsPos[0]):
            if(containVerbePrem(verbe[1],phrase)):
                prob_p+=1
        for verbe2 in enumerate(motsNeg[0]):
            if(containVerbePrem(verbe2[1],phrase)):
                prob_n+=1
                
        for adj in enumerate(motsPos[1]):
            if(containMot(adj[1],phrase)):
                prob_p+=1
        for adj2 in enumerate(motsNeg[1]):
            if(containMot(adj2[1],phrase)):
                prob_n+=1
        for mot in enumerate(motsPos[2]):
            if(containMot(mot,phrase)):
                prob_p+=1
        for mot in enumerate(motsNeg[2]):
            if(containMot(mot,phrase)):
                prob_n+=1
                
    list_prob=[prob_p,prob_n]
    return list_prob
    




def Decision(comment,motPos,motNeg):
    poid_p=0
    poid_n=0
    prob=AnalyseComment3(comment,motPos,motNeg)
    prob_cn=ProbNCommentaire(comment)
    if(prob[0]-prob[1]>1): poid_p+=1
    else : poid_n+=1
    if(prob_cn<0.5): poid_p+=1
    else : poid_n+=1
    taux=prob_cn-0.5
    if(taux>0.0):
        poid_n+=1
        poid_n+=taux*10
    else : 
        poid_p+=1
        poid_p+=1
    liste=[poid_p,poid_n]
    return liste
    
    
    
#-----------fin methode teste----------------------------------------------#
            
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
    print("-------------SECOND ANALYSE ----------------------------------")
    motPos=biblioMotPositif()
    motNeg=biblioMotNegatif()
    motN_import=ImportList("mot_negatif.txt")+ImportList("adj_negatif.txt")
    motP_import=ImportList("adj_positif.txt")
    motPos.append(motP_import)
    motNeg.append(motP_import)
    k=0
    for comment in commentsTok:
        if(AnalyseComment2(comment,motPos,motNeg)==True):
            print("comment"+str(k)+"  :"+"Programme dit avis Positif "+ " vs note :"+str(notes[k])) 
        else :
            print("comment"+str(k)+"  :"+"Programme dit avis Negatif "+" vs note :"+str(notes[k]))
        k+=1
    
    print("------------TROSIEME ANALYSE ----------------------")
    z=0
    for comment in commentsTok:
        tmp=Decision(comment,motPos,motNeg)
        if(tmp[0]>tmp[1]):
            print("comment"+str(z)+" : poid P "+str(tmp[0])+" poid N "+str(tmp[1])+"Avis Bon  vs note : " +str(notes[z]))
        else :
            print("comment"+str(z)+" : poid P "+str(tmp[0])+" poid N "+str(tmp[1])+"Avis Negative  vs note : " +str(notes[z]))
        z+=1

    
    
