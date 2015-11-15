#!/usr/bin/env python
import sys
from  p1lib import *
from linecache import getline

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
    print "Content-type:text/html\r\n\r\n"
    for cluster in cllist:
        print "<div class='cluster'><h5>cluster</h5><ul class='collapsible small-container' data-collapsible='accordion'>"
        for item in cluster:
            print "<li>"
            part = res_file[item].split("\t")
            print '<div class="collapsible-header">'
            print part[0].encode("utf-8")
            print '</div>'
            print '<div class="collapsible-body">'
            print '<span>'+part[1].encode("utf-8")+'</span>'
            print '<span>'+part[2].encode("utf-8")+'</span>'
            print '<p><a class="btn" href="'+part[3].encode("utf-8")+'">link</a></p>'
            print '<p>'+part[4].encode("utf-8")+'</p>'                        
            print '</div>'
            print "</li>"
        print "</ul></div>"
else:

    print "No document found"
    
## list_res = postings[Index[result[0]]]

## for item in result:
##         list_res = intersect(list_res, postings[Index[item]])
## print "Content-type:text/html\r\n\r\n"

## for res_item in list_res:
##         print "<li class='card'>"
##         afile = readfile(int(res_item))
##         afile= afile.split("\t")
##         for a_item in afile:
##                 print "<p>"
##                 print a_item.encode("utf-8")
##                 print "</ p>"
##         print "</ li>"


