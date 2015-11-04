import re
import nltk as nl
from nltk.stem import SnowballStemmer
snowball_stemmer = SnowballStemmer("italian")
from collections import Counter


###Funzione per splittare e fare il dizionario
def bag(read_data, threshold=1):
    read_data= read_data
    #tokenizza, rimuovi le stopword e fai lo stemming
    read_data=  re.split("['\`\-\=\~\!\@\#\$\%\^\&\*\(\)\_\+\[\]\{\}\;\'\\\:\"\|\<\,\.\/\>\<\>\?\"\\s\''']+", read_data)
    filtered_words = [word for word in read_data if word not in nl.corpus.stopwords.words('italian')]
    read_data = [snowball_stemmer.stem(word).encode("utf-8") for word in filtered_words]
    
    out = dict(Counter(read_data))
    return {i:out[i] for i in out if out[i]>= threshold}

def incrindex(k, leng):
    if k<leng:
        return k+1
    else:
        return k
    
def addtoIndex(I, bag, posting_list, doc_id):
    print "unisco il file", doc_id
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
            
    if b<l2:
        I[list2[b]]=1
        posting_list[list2[b]]=[[doc_id, bag[list2[b]]]]
        b=incrindex(b, l2)



def readfile(number):
    
    path= "./documents/documents-"+str(number/500).zfill(6)+"-"+str(number/500 +500).zfill(6)+"/"
    file = open(path+str(number).zfill(6)+".txt","r")
    data=file.readline().decode("utf-8")
    return data    
#Creo l'indice
I={}
posting_list= {}

#Per ogni file:

for number in range(100):
    #leggilo
    data = readfile(number)
    print "file numero", number, "\n"
    #rimuovo gli url
    data = re.sub(r"http\S+", "", data)
    bags=  bag(data)
    #print bags
    addtoIndex(I,bags, posting_list, number)


print "----------------------------"
print I
print posting_list

