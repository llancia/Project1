import re
import numpy as np
import sys
import os
import nltk as nl
from nltk.stem import SnowballStemmer
snowball_stemmer = SnowballStemmer("italian")
from collections import Counter


###Funzione per splittare e fare il dizionario
def bag(read_data, threshold=1):
    #print read_data
    #tokenizza, rimuovi le stopword e fai lo stemming
    read_data=  re.findall(r"[a-zA-Z]+", read_data)
    #print read_data
    filtered_words = [word for word in read_data if word not in nl.corpus.stopwords.words('italian')]
    #print filtered_words
    read_data = [snowball_stemmer.stem(word).encode("utf-8") for word in filtered_words]
    out = dict(Counter(read_data))
    return {i:out[i] for i in out if out[i]>= threshold}


def incrindex(k, leng):
    if k<leng:
        return k+1
    else:
        return k
    
def addtoIndex(I, bag, posting_list, doc_id):
    #print "unisco il file", doc_id
    list1 = I.keys()
    list2 = bag.keys()
    list1.sort()
    list2.sort()
    l1 =len(list1)
    l2=len(list2)
    a = 0
    b = 0
    if len(list1)==0:
        print "creo il primo indice\n"
        for key, value in bag.iteritems():
            I[key]=1
            posting_list[key]= [[doc_id, value]]
        return
    while(a<l1 and b<l2):
        #print "a=",a,"b=",b
        if list1[a]==list2[b]:
            I[list1[a]]+=1
            posting_list[list1[a]].append([doc_id, bag[list2[b]]])
            a=incrindex(a, l1)
            b=incrindex(b, l2)
        elif list1[a]>list2[b]:
            #appendere al dizionario
            I[list2[b]]=1
            posting_list[list2[b]]=[[doc_id, bag[list2[b]]]]
            b=incrindex(b, l2)
        else: #list1[a]<list2[b]
            a=incrindex(a, l1)
    ##PROBLABILMENTE SUPERFLUO        
    if b<l2:
        I[list2[b]]=1
        posting_list[list2[b]]=[[doc_id, bag[list2[b]]]]
        b=incrindex(b, l2)



def readfile(number):
    path= "./documents/documents-"+str((number/500) *500).zfill(6)+"-"+str((number/500)*500 +500).zfill(6)+"/"
    file = open(path+str(number).zfill(6)+".txt","r")
    data=file.readline().decode("utf-8")
    return data    

def intersect(set1, set2):
    set1.sort()
    set2.sort()
    inter=[]
    l1 = len(set1)
    l2 = len(set2)
    a=0
    b=0
    while(a<l1 and b<l2):
        if set1[a]==set2[b]:
            inter.append(set1[a])
            a=incrindex(a, l1)
            b =incrindex(b, l2)
        elif set1[a]>set2[b]:
            b =incrindex(b, l2)
        else: #list1[a]<list2[b]
            a=incrindex(a, l1)
            
    return inter
    
def jaccard(s1, s2):
    st1=set(s1)
    st2=set(s2)
    u = set(st1).union(st2)
    i = set(st1).intersection(st2)
    return float(len(i))/len(u)

def single_linkage(D, k=2):
    ncluster = len(D[0])
    cluster = range(len(D[0]))
    np.fill_diagonal(D, np.inf)
    while (ncluster >k):
        #Troviamo il pi vicino 
        x, y = np.unravel_index(D.argmin(), D.shape)
        #Joiniamo i pi vicini
      
        cluster = [x if item == y else item for item in cluster]     
        #aggiorniamo la matrice
        D[x][y] = np.inf
        D[y][x] = np.inf
        for index in range(len(D[0])):
            if (D[x][index]==np.inf or D[y][index]==np.inf):
                val = np.inf
            else:
                val = min(D[x][index], D[y][index])
            D[x][index] = val
            D[y][index] = val
            D[index][x] = val
            D[index][y] = val
        ncluster = ncluster - 1
    return cluster


def clustering(listofdocs, k):
    baglist = [bag(item,2).keys() for item in listofdocs]
    Matrix = [[1-jaccard(baglist[x],baglist[y]) for x in range(len(baglist))] for y in range(len(baglist))]
    Matrix=np.array(Matrix)
    B=single_linkage(Matrix, k)
    
    clusterList=[[]for item in range(max(B)+1)]

    for item in range(len(Matrix[0])):
            clusterList[B[item]].append(item)
            
    new_clist = []
    for i in range(len(clusterList)):
        if clusterList[i] != []:
            new_clist.append(clusterList[i])

    return new_clist
