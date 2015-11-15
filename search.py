from  p1lib import *
from linecache import getline
try:
    query = sys.argv[1]
except: 
    query = raw_input("Query?->")

data_query = bag(query)

vocfile = open("./index/vocabulary.txt","r")
temp = vocfile.read().splitlines()
#print temp
Index={}
for item in temp:
        item = item.split("\t")
        Index[item[1]]=item[0]



        
result = intersect(Index.keys(), data_query.keys())
postings ={}
#postingfile =  open("./index/postings.txt","r")
for word in result:
        temp = getline("./index/postings.txt",int(Index[word])+1).split("\t")
        postings[temp[0]] = [temp[n] for n in range(1,len(temp)-1)]


if len(result)>0:

    list_res = postings[Index[result[0]]]

    for item in result:
        list_res = intersect(list_res, postings[Index[item]])

   
    res_file =[ readfile(int(res_item)) for res_item in list_res]
    cllist=  clustering(res_file, len(res_file)/2)
    for cluster in cllist:
        for item in cluster:
            print res_file[item]
            print "\n"
        print "\n-------------------------------\n"
else:

    print "No document found"

