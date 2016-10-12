# -*- coding: utf-8 -*-
'''
Created on 30/08/2016

@author: Jose Angel Gonzalez Mejias
'''
from controller import buscaPIinfo
from controller import piInfo
import xml.etree.ElementTree as ET
import sys
import json
import requests
from model import author
from datetime import date

def main(panel,projectType):
    f = open('resources/application.properties','r')
    properties = f.read()
    properties = json.loads(properties)
    apiKey = properties["ApiKey"]
    f.close()

    print('final_{0}_P{1}.xml'.format(projectType,panel))
    tree = ET.parse('resources/projects/final_{0}_P{1}.xml'.format(projectType,panel))
    root = tree.getroot()

    for project in root.findall('Project'):
        print(project.find('Rcn').text)
        pi = project.find('PI').text
        pi = pi.split(" ")
        lastname = pi[-1]
        name = ""
        for word in pi[:-1]:
            name = name + word + " "
        name = name[:-1]
        authors = buscaPIinfo.buscaAutorPorNombreApellido(name,lastname)
        if authors == 0:
            continue
        auth = authors[0]
        fullName = "{0};{1}".format(lastname,name)
        identifier = auth.identifier.split(":")[1]

        year = project.find('Duration').find('Start_date').text.split("-")[0][1:]

        values = getPIValues(lastname,name,identifier,year)

        f = open('resources/authors/{0}.txt'.format(identifier),'a+')
        f.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, 1\n".format(values["fullName"],values["docs"],values["cited_by_count"],values["citation_count"],year,panel,values["hindex"],values["coauthor_count"],values["coAuthAvg"]))
        f.close()
    return 0

def getPITestValues(lastName,name,identifier,panel):
    year = date.today().year

    values = getPIValues(lastName,name,identifier,year)

    f = open('resources/test.txt','w')
    f.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, 1".format(values["fullName"],values["docs"],values["cited_by_count"],values["citation_count"],values["year"],panel,values["hindex"],values["coauthor_count"],values["coAuthAvg"]))
    f.close()

def getPIValues(lastName,name,identifier,year):
    f = open('resources/application.properties','r')
    properties = f.read()
    properties = json.loads(properties)
    apiKey = properties["ApiKey"]
    f.close()

    fullName = "{0};{1}".format(lastName,name)

    url = "https://api.elsevier.com/content/author/author_id/{0}".format(identifier)

    querystring = {"apiKey":apiKey,"view":"ENHANCED"}
    headers = {
        'accept': "application/json",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    decoded = json.loads(response.text)

    author_retrieval = decoded["author-retrieval-response"][0]

    hindex = author_retrieval["h-index"]
    coauthor_count = author_retrieval["coauthor-count"]

    coredata = author_retrieval["coredata"]
    docs = coredata["document-count"]
    cited_by_count = coredata["cited-by-count"]
    citation_count = coredata["citation-count"]

    url = "http://api.elsevier.com/content/search/scopus"

    querystring = {"apiKey":apiKey,"query":"AU-ID({0})".format(identifier),"field":"dc:identifier"}
    headers = {
        'accept': "application/json",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    decoded = json.loads(response.text)

    coAuthAvg = 0
    quartiles = getQuartiles()
    quartilesPI = [0,0,0,0]
    entradas = decoded["search-results"]["entry"]
    for entrada in entradas:

        docID = entrada["dc:identifier"]
        #print(docID)
        url = "http://api.elsevier.com/content/abstract/scopus_id/{0}".format(docID)

        querystring = {"apiKey":apiKey,"field":"prism:issn,authors"}
        headers = {
            'accept': "application/json",
            'cache-control': "no-cache"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        decoded = json.loads(response.text)

        quartil = "NONE"
        try:
            issn = decoded["abstracts-retrieval-response"]["coredata"]["prism:issn"]
            f = open('resources/journals/{0}.txt'.format(issn),'r')
            text = f.read()
            f.close()

            text = json.loads(text)
            sjr = text['sjr'][str(year)]
            quartilesPI = getQuartil(sjr,year,quartiles,quartilesPI)[1]
            quartil = getQuartil(sjr,year,quartiles,quartilesPI)[0]
        except:
            pass
        coAuthAvg = coAuthAvg + len(decoded["abstracts-retrieval-response"]["authors"])
    coAuthAvg = coAuthAvg/len(entradas)

    return {"fullName":fullName,"docs":docs,"cited_by_count":cited_by_count,"citation_count":citation_count,"year":year,"hindex":hindex,"coauthor_count":coauthor_count,"coAuthAvg":coAuthAvg,"quartil":quartil,"quartilesPI":quartilesPI}

def getPIQuartiles(identifier,panel):
    values = getPIValues("","",identifier,year)
    return values["quartilesPI"]

def getQuartiles():
    f = open('resources/quartiles.txt','r')
    text = f.read()
    f.close()
    return json.loads(text)

def getQuartil(sjr,year,quartiles,quartilesPI):
    qx = quartiles['quartiles'][str(year)]
    if sjr <= qx['q1']:
        quartilesPI[0] = quartilesPI[0]+1
        return ["q1",quartilesPI]
    elif sjr <= qx['q2']:
        quartilesPI[1] = quartilesPI[1]+1
        return ["q2",quartilesPI]
    elif sjr <= qx['q3']:
        quartilesPI[2] = quartilesPI[2]+1
        return ["q3",quartilesPI]
    else:
        quartilesPI[3] = quartilesPI[3]+1
        return ["q4",quartilesPI]

if __name__ == "__main__":
    main(sys.argv)
