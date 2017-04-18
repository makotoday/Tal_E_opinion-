# -*- coding: utf-8 -*-

"""
Created on Fri Apr  7 20:40:06 2017
@author: Sébastien
"""

import urllib
import html.parser as ps
import codecs as co

class MyHTMLParser(ps.HTMLParser):

    def __init__(self):
        ps.HTMLParser.__init__(self)
        self.recording = 0 
        self.data = []
    def handle_starttag(self, tag, attrs):
        if(tag=='p'and len(attrs)==1 and attrs[0]== ('itemprop', 'description') ):
            self.recording = 1
            print('ok', tag,attrs)
        # notes des commentaires
        elif(tag=='span' and len(attrs)==3 and attrs[0]==('class','stareval-note') 
        and attrs[1]== ('itemprop','ratingValue')):
           self.data.append(str(attrs[2]))
           print(attrs[2])

    def handle_data(self, data):
       if self.recording:
           self.data.append(data)


    def handle_endtag(self,tag):
        if(tag=='p' and self.recording):
            self.recording -=1


# page allocine :
#  balise de début comm : <p itemprop="description"> ex à 3412
# balise de notes : <span class="stareval-note" itemprop="ratingValue" content="4,5">
# fin : <p>
# enregistre les commentaires du corpus html
def logComments(sourcehtml):
    print(sourcehtml)

# doit reconnaitre si une phrase contient une négation ou pas
def negationDansPhrase(phrase):
    for i in range(0,len(phrase)):
        if("pas"==phrase[i]):
            return True
      
    return False
    
def decodeAccent(comment):
        comment = comment.replace("\\xc3\\xa9","é")
        comment = comment.replace("\\xc3\\xa8","è")
        comment = comment.replace("\\xc3\\xaa","ê").replace("\\xc3\\xab","e")
        comment = comment.replace("\\xc3\\xa0","à")
        comment = comment.replace("\\xc5\\x93","oe")
        comment = comment.replace("\\xe2\\x80\\x93",",")
        comment = comment.replace("\\xe2\\x80\\x99","'")
        comment = comment.replace("\\xc3\\xa7",'ç')
        comment = comment.replace("\\xe2\\x80\\xa6",".")
        comment = comment.replace("\\xc3\\xb4","ô")
        comment = comment.replace("\\xc2\\xab","\"").replace("\\xc2\\xbb","\"")
        comment = comment.replace("\\\'","'").replace("\'","'")
        comment = comment.replace("\\n",'')
        return comment
    
# pour le corpus : assigne une valeur plus grande pour les verbes
# de la phrase selon la note de l'avis
# avis : liste des tokens de l'avis
#note : valeur entière correspondant à la note de l'avis
    
def assigneVal(note, avis):
    tab = []
    i = 0
    for mot in avis:
       tab.append(mot,avis)
    return tab

if __name__=="__main__":
    
    sock = urllib.request.urlopen("http://www.allocine.fr/film/fichefilm-226739/critiques/spectateurs/")
    htmlsrc = sock.readlines()
    
    
    sock.close()
    parser = MyHTMLParser()
    
    for i in range(0,len(htmlsrc)):
        struni = str(htmlsrc[i])
        parser.feed(struni)
       
    listcomments = parser.data
    i = 0
    while(i<len(listcomments)):
        comment = listcomments[i]
    
        # enlevement des caractères en trop (\n b et ')
        listcomments[i] = decodeAccent(listcomments[i])

        if(listcomments[i] =='' or listcomments[i].isspace()==True):
           listcomments.pop(i)
        else:
            i+=1
    #       print(parser.getpos(),comment)
    #       print("EETTT\n\n", struni)
    
    print(listcomments)
    parser.close()
    
    