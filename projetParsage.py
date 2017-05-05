# -*- coding: utf-8 -*-
"""
Created on Thu May  4 21:52:58 2017

@author: Sébastien
"""

import urllib
import re
from bs4 import BeautifulSoup


# doit reconnaitre si une phrase contient une négation ou pas
def negationDansPhrase(phrase):
    for i in range(0,len(phrase)):
        if("pas"==phrase[i]):
            return True
            
def normalise(sent, lang):
    sent = re.sub("\'\'", '"', sent) # two single quotes = double quotes
    sent = re.sub("[`â€˜â€™]+", r"'", sent) # normalise apostrophes/single quotes
    sent = re.sub("[â‰ªâ‰«â€œâ€]", '"', sent) # normalise double quotes

    if lang=="en":
        sent = re.sub("([a-z]{3,})or", r"\1our", sent) # replace ..or words with ..our words (American versus British)
        sent = re.sub("([a-z]{2,})iz([eai])", r"\1is\2", sent) # replace ize with ise (..ise, ...isation, ..ising)
    if lang=="fr":
        replacements = [("keske", "qu' est -ce que"), ("estke", "est -ce que"), ("bcp", "beaucoup")] # etc.
        for (original, replacement) in replacements:
            sent = re.sub("(^| )"+original+"( |$)", r"\1"+replacement+r"\2", sent)
    return sent
    
def tokenise_en(sent):

    # deal with apostrophes
    sent = re.sub("([^ ])\'", r"\1 '", sent) # separate apostrophe from preceding word by a space if no space to left
    sent = re.sub(" \'", r" ' ", sent) # separate apostrophe from following word if a space if left
    cannot_precede = ["M", "Prof", "Sgt", "Lt", "Ltd", "co", "etc", "[A-Z]", "[Ii].e", "[eE].g"] #non-exhaustive list
    regex_cannot_precede = "(?:(?<!"+")(?<!".join(cannot_precede)+"))" 
    
    sent = re.sub(regex_cannot_precede+"([\.\,\;\:\)\(\"\?\!]( |$))", r" \1", sent)
    sent = re.sub("((^| )[\.\?\!]) ([\.\?\!]( |$))", r"\1\2", sent) 

    sent = sent.split() # split on whitespace
    return sent

def tokenise(sent, lang):
    if lang=="en":
        return tokenise_en(sent)
    elif lang=="fr":
        return tokenise_fr(sent)
    else:
        exit("Lang: "+str(lang)+" not recognised for tokenisation.\n")


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


if __name__=="__main__":
    
    #page allocine
    sock = urllib.request.urlopen("http://www.allocine.fr/film/fichefilm-226739/critiques/spectateurs/")
    src = sock.read()
    sock.close()
    comments = []
    notes = []
    comments, notes = chargement(src)
    
    
    for i in range(0,len(comments)):   
        print(comments[i])
        print(notes[i])
    
    sents = []
    for i in range(0,len(comments)):     
        sents.append(tokenise(comments[i],"en"))
    
    print(sents)