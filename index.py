from  p1lib import *

#Creo l'indice
I={}
posting_list= {}

#Per ogni file 63364:
meta_file = open("./documents/num_of_file.txt", "r")


TOT_FILE =int(meta_file.read())
meta_file.close()
for number in range(TOT_FILE):
    #leggilo
    data = readfile(number)

    progress= "completamento "+str( (number*1.)/TOT_FILE *100)+" %"
    print progress+"\r",
    sys.stdout.flush()

    
    #rimuovo gli url
    data = re.sub(r"http\S+", "", data)
    data= data.replace(u"\u20AC","")
    #rimuovo i prezzi
    #print data
    #data = re.sub(r"([0-9]{1,3}\.?){4,}", "", data)
    bags=  bag(data)
    #print bags
    addtoIndex(I,bags, posting_list, number)

print "----------------------------"

dictionary=I.keys()
dictionary.sort()
#print dictionary 
#print posting_list



#se non esiste la cartella index allora creala
if not os.path.exists("index"):
    os.makedirs("index")
outpath="./index/"
vocfile= open(outpath+"vocabulary.txt", "w")
postlistfile = open(outpath+"postings.txt", "w")
nword=0
for word in dictionary:
    vocfile.write(str(nword)+"\t"+word+"\n")
    outstr=""
    for element in posting_list[word]:
        outstr+=str(element[0])+"\t"
    postlistfile.write(str(nword)+"\t"+outstr+"\n")
    nword+=1

