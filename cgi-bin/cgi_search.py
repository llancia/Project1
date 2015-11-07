#!/Users/lorenzo/anaconda/bin/python
import sys
from  p1lib import *


def readfile(number):
    path= "./documents/documents-"+str((number/500) *500).zfill(6)+"-"+str((number/500)*500 +500).zfill(6)+"/"
    file = open(path+str(number).zfill(6)+".txt","r")
    data=file.readline().decode("utf-8")
    return data    

import cgi,cgitb 
cgitb.enable()
request = cgi.FieldStorage()
query = request["query"].value
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
        postings[item[0]] = [item[n] for n in range(1,len(item)-1)]

        
result = intersect(Index.keys(), data_query.keys())


list_res = postings[Index[result[0]]]

for item in result:
        list_res = intersect(list_res, postings[Index[item]])
print "Content-type:text/html\r\n\r\n"

for res_item in list_res:
        print "<li class='card'>"
        afile = readfile(int(res_item))
        afile= afile.split("\t")
        for a_item in afile:
                print "<p>"
                print a_item.encode("utf-8")
                print "</ p>"
        print "</ li>"


