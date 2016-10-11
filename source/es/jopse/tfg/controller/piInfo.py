# -*- coding: utf-8 -*-
'''
Created on 30/08/2016

@author: Jose Angel Gonzalez Mejias
'''
from html.entities import name2codepoint
from html.parser import HTMLParser
import urllib.request as request
import sys

URL = "https://www.scopus.com/authid/detail.uri?authorId={0}"

class MyHTMLParser(HTMLParser):
    docCntLnk = False
    totalCiteCount = False
    citationCntLnk = False
    coAuthCntLnk = False
    posibleH = False
    posibleH2 = False
    posibleH3 = False

    todosProyecto = []
    bodyData = dict()
    projects = False
    esEtiqueta = False
    saltarEtiqueta = False
    empiezaP = -1
    etiqueta = ""
    pages = False
    numPages = 0
    def handle_starttag(self, tag, attrs):
        if(tag == "a"):
            for attr in attrs:
                if("id" in attr):
                    if('docCntLnk' in attr):
                        self.docCntLnk = True
                    elif("totalCiteCount" in attr):
                        self.totalCiteCount = True
                    elif("citationCntLnk" in attr):
                        self.citationCntLnk = True
                    elif("coAuthCntLnk" in attr):
                        self.coAuthCntLnk = True
                    else:
                        continue
        elif(tag == "li"):
            for attr in attrs:
                if("class" in attr and "addInfoRow row3" in attr):
                    self.posibleH = True
        elif(tag == "div"):
            for attr in attrs:
                if("class" in attr and "valueColumn" in attr and self.posibleH):
                    self.posibleH2 = True
        elif(tag == "span"):
            if self.posibleH and self.posibleH2:
                self.posibleH3 = True

    def handle_endtag(self, tag):
        if(tag == "a"):
            self.docCntLnk = False
            self.totalCiteCount = False
            self.citationCntLnk = False
            self.coAuthCntLnk = False
        elif(tag == "li"):
            self.posibleH = False
        elif(tag == "div"):
            self.posibleH2 = False
        elif(tag == "span"):
            self.posibleH3 = False
        else:
            pass
    def handle_data(self, data):
        if self.docCntLnk:
            docs = data
        if self.totalCiteCount:
            totalCites = data
        if self.citationCntLnk:
            citationCnt = data
        if self.coAuthCntLnk:
            coAuthCount = data
        if self.posibleH3:
            hindex = data
    def handle_comment(self, data):
        pass
    def handle_entityref(self, name):
        c = name2codepoint[name]
    def handle_charref(self, name):
        if name.startswith('x'):
            c = int(name[1:], 16)
        else:
            c = int(name)
    def handle_decl(self, data):
        pass

def main(authorId):

    #Creacion del parser
    parser=MyHTMLParser()
    with request.urlopen(URL.format(authorId)) as response:
        html = response.read()
        html = html.decode('utf-8')

        parser.feed(html)
        hindex = parser.hindex
        docs = parser.docs
        totalCites = parser.totalCites
        citationCnt = parser.citationCnt
        coAuthCount=parser.coAuthCount

    return [hindex,docs,totalCites,citationCnt,coAuthCount]
if __name__ == "__main__":
    main(sys.argv)
