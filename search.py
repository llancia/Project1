from  p1lib import *

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

postingfile =  open("./index/postings.txt","r")
temp = postingfile.read().splitlines()
postings ={}
for item in temp:
        item = item.split("\t")
        postings[item[0]] = [item[n] for n in range(1,len(item))]

        
result = intersect(Index.keys(), data_query.keys())
#print result


list_res = postings[Index[result[0]]]
for item in result:
        list_res = intersect(list_res, postings[Index[item]])
print list_res



