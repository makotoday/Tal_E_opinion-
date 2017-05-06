# -*- coding: utf-8 -*-
"""
Created on Sat May  6 17:26:35 2017

@author: Sébastien
"""
import projetParsage as pars
import fonctionsTokenise as ftok
import urllib

#-------------methode teste------------------------------------------------#
def testNegation(commentaire,tauxNegatif,note_commentaire):
    taux= pars.ProbNCommentaire(commentaire)
    if(taux<tauxNegatif):
        print("bon commentaire\t TN:"+str(taux)+"\t Note C:"+str(note_commentaire))

        
def ImportList(pathfile):
      liste=[]
      mot_list=[]
      with open(pathfile, "r") as filepointer:
         for line in filepointer.readlines():
            if line.strip()=="": continue # ignore blank paragraphs
            new_line=line.strip(',')
            tmp= ftok.segment_into_sents(new_line.strip())            
            liste=tmp+liste # remove whitespace with strip()
         for mot in liste:
            tmp= ftok.normalise(mot,"fr")
            tmp=ftok.tokenise(tmp,"en")
            mot_list.append(tmp)
      return liste
      
def evalueComment(comment):
    motsPos = biblioMotPositif()
    motsNeg = biblioMotNegatif()
    evalu = 0
    # test negation
    for phrase  in enumerate (comment):
        for verbe in enumerate(motsPos[0]):
            if(pars.containVerbePrem(verbe[1],phrase)):
                evalu+=1
        for verbe2 in enumerate(motsNeg[0]):
            if(pars.containVerbePrem(verbe2[1],phrase)):
                evalu-=1
        for adj in enumerate(motsPos[1]):
            if(pars.containMot(adj[1],phrase)):
                evalu+=1
        for adj2 in enumerate(motsNeg[1]):
            if(pars.containMot(adj2[1],phrase)):
                evalu-=1
    return evalu
    
# simple analyse en comptant le nombre de mots positifs et négatifs    
def analyse1(comments, notes):
    i = 0;
    for comment in commentsTok:
        evalcom = 0;
        for phrase in comment:
            evalcom += evalueComment(phrase)
    print("comment"+str(i)+"  :"+str(evalcom)+ " vs note :"+str(notes[i]))
    i+=1
    
    

def AnalyseComment3(comment,motsPos,motsNeg):
    prob_p=0
    prob_n=0
    mot_total=0
    for phrase in comment:
        mot_total+=len(phrase)
        for verbe in enumerate(motsPos[0]):
            if(pars.containVerbePrem(verbe[1],phrase)):
                prob_p+=1
        for verbe2 in enumerate(motsNeg[0]):
            if(pars.containVerbePrem(verbe2[1],phrase)):
                prob_n+=1
                
        for adj in enumerate(motsPos[1]):
            if(pars.containMot(adj[1],phrase)):
                prob_p+=1
        for adj2 in enumerate(motsNeg[1]):
            if(pars.containMot(adj2[1],phrase)):
                prob_n+=1
        for mot in enumerate(motsPos[2]):
            if(pars.containMot(mot,phrase)):
                prob_p+=1
        for mot in enumerate(motsNeg[2]):
            if(pars.containMot(mot,phrase)):
                prob_n+=1
                
    list_prob=[prob_p,prob_n]
    return list_prob

def Decision(comment,motPos,motNeg):
    poid_p=0
    poid_n=0
    prob=AnalyseComment3(comment,motPos,motNeg)
    prob_cn= pars.ProbNCommentaire(comment)
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
    
# prise en compte de la négation dans la phrase
def analyse4(comment,motsPos,motsNeg):
    
    neg = False
    noteComment = 0
    for phrase in comment:
        neg = False
        listMot = []
        if(pars.negationDansPhrase(phrase)): neg = True 
        for verbe in motsPos[0]:                
            if(pars.containVerbePrem(verbe,phrase)):
                listMot.append(1)
        for adj in enumerate(motsPos[1]):
            if(pars.containMot(adj[1],phrase)):
                listMot.append(1)
        for mot in enumerate(motsPos[2]):
            if(pars.containMot(mot[1],phrase)):     
                listMot.append(1)
        for verbe2 in motsNeg[0]:
            if(pars.containVerbePrem(verbe2,phrase)):
                listMot.append(-1)               
        for adj2 in enumerate(motsNeg[1]):
            if(pars.containMot(adj2[1],phrase)):
                listMot.append(-1)       
        for mot in enumerate(motsNeg[2]):
            if(pars.containMot(mot[1],phrase)):
                listMot.append(-1)
 
        if(neg): 
            for p in listMot:
                p = -p # inversion du poids du mot
        for p in listMot:
            noteComment += p
    print(noteComment)
    if(noteComment>0): return "Positif"
    elif(noteComment  <0): return "Negatif"
    else: return "neutre"
    
    
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
        commentsFilm, notesFilm = pars.chargement(src)
        comments+=commentsFilm
        notes+= notesFilm
    print("fin chargement de "+str(len(comments))+" comments")
    
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
        #analyse1(commentsTok,notes);
    # ajout d' adjectifs négatifs via un fichier .txt    
    motPos= pars.biblioMotPositif()
    motNeg= pars.biblioMotNegatif()
    motN_import=ImportList("mot_negatif.txt")+ImportList("adj_negatif.txt")
    motP_import=ImportList("adj_positif.txt")
    motN_import = ftok.normalise(str(motN_import),'fr')
    
    #print(motN_import)
    motPos.append(motP_import)
    motNeg.append(motP_import)
    
#    print("------------TROSIEME ANALYSE-----------------")
#    for z in range(0,len(commentsTok)):
#        tmp=Decision(commentsTok[z],motPos,motNeg)
#        if(tmp[0]>tmp[1]):
#            print("comment"+str(z)+" : P="+str(tmp[0])+"  N="+str(tmp[1])+" Avis + vs note : " +str(notes[z]))
#        else :
#            print("comment"+str(z)+" : P="+str(tmp[0])+" N="+str(tmp[1])+" Avis - vs note : " +str(notes[z]))
#    
    print("------------QUATRIEME ANALYSE-----------------")
    for i in range(0,len(commentsTok)):
       print("comment"+str(i) + " : "+analyse4(commentsTok[i],motPos,motNeg)+" vs note : " +str(notes[i]))
    
    
