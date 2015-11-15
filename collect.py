import urllib2
from bs4 import BeautifulSoup
import os
import time

def get_all_adcription(annurl):
    html = urllib2.urlopen(annurl)
    asoup = BeautifulSoup(html)
    adcription = asoup.find("p", {"class": "ki-view-ad-description"}).contents[0].encode("utf-8")
    return adcription

url = "http://www.kijiji.it/case/vendita/roma-annunci-roma/"
a = urllib2.urlopen(url)
soup = BeautifulSoup(a)
npage =  soup.find("a", { "class" : "last-page" })
npage=  int(npage.contents[0])

print "Trovate ", npage, " pagine di annunci da Kijiji\n"
npage = int(raw_input("Quante pagine devo scaricare? "))
#se non esiste la cartella documents allora creala
if not os.path.exists("documents"):
    os.makedirs("documents")
root="./documents/"
entry_id = 0
#iterare su tutte le pagine di kijiji

for kijpage in range(1,npage+1):
    print "Scarico pagina", kijpage, " di ", npage
    #lettura e parsing html
    pagurl = url+"?p="+str(kijpage)
    a = urllib2.urlopen(pagurl)
    soup = BeautifulSoup(a)

    #leggo sia gli annunci top che quelli normali
    topresult = soup.findAll("li", {"class": "item topad result"})
    results = soup.findAll("li", {"class": "item result"})
    results.extend(topresult)
    
    #iterazione su tutti gli annunci di una pagina
    for item in results:
        #Controllo se esista la cartella
        if entry_id%500 ==0:
            if not os.path.exists("documents/documents-"+str(entry_id).zfill(6)+"-"+str(entry_id+500).zfill(6)):
                os.makedirs("documents/documents-"+str(entry_id).zfill(6)+"-"+str(entry_id+500).zfill(6))
            path=root+"/documents-"+str(entry_id).zfill(6)+"-"+str(entry_id+500).zfill(6)+"/"
        #Apro il file
        record_entry = open (path+str(entry_id).zfill(6)+".txt", "w")
        #Leggo le singole parti
        title = item.h3.contents[0].encode("utf-8")
        location = item.find("p", {"class": "locale"}).contents[0].encode("utf-8")
        price = item.h4.contents[0].encode("utf-8")
        adurl = item.find("a", {"class": "cta"})
        adurl = adurl['href']
        # SE SI VUOLE SOLO IL SUNTO DELLA DESCRIZIONE DECOMMENTARE LA LINEA SUCCESSIVA
        #description = item.find("p", {"class": "description"}).contents[0].encode("utf-8")
        description = get_all_adcription (adurl)

        #Scrivo il file
        record_entry.write(title+"\t"+location+"\t"+price+"\t"+adurl+"\t"+description)
        #Chiudo il file
        record_entry.close()
        entry_id +=1
    time.sleep(0.1)

meta_file = open ( "./documents/num_of_file.txt", "w")
meta_file.write(str(entry_id-1))
meta_file.close()
    


