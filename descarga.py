# -*- coding: utf-8 -*-
'''
Created on 1/10/2015

@author: Jose Angel Gonzalez Mejias
'''
import urllib.request as request
from html.entities import name2codepoint
from html.parser import HTMLParser
import xml.etree.cElementTree as ET


URL = "http://erc.europa.eu/projects-and-results/erc-funded-projects?f[2]=sm_field_cordis_project_funding%3A{0!s}%20%28{1!s}%29&page={2!s}"
ABBR = {'CoG':'Consolidator%20Grants','StG':'Starting%20Grant','PoC':'Proof%20of%20Concept'}


'''
Redefinición de metodos para facilitar el parseado
'''

class MyHTMLParser(HTMLParser):
    bodyData = dict()
    projects = False
    empiezaP = -1
    etiqueta = ""
    def handle_starttag(self, tag, attrs):
        if(tag == "ul"):
            self.projects = True
    def handle_endtag(self, tag):
        if(tag == "ul"):
            self.projects = False
    def handle_data(self, data):
        if self.projects:
            if data == "Rcn":
                self.empiezaP = 0
            if self.empiezaP > 0 and self.empiezaP %2 == 0:
                self.etiqueta = data
                self.empiezaP+=1
            elif self.empiezaP > 0:
                self.bodyData[self.etiqueta] = data
                self.empiezaP+=1
            if self.empiezaP > 17:
                self.empiezaP = -1
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
#Creacion del parser
parser=MyHTMLParser()
#Variable que contendra todo el codigo de todos los proyectos
consolidatorGrantsProjects=""

#Recorre todas las 62 paginas para extraer los proyectos solamente
for i in range(1):
    with request.urlopen(URL.format(ABBR['CoG'],'CoG',i)) as response:
        html = response.read()
        html = html.decode('utf-8')
        f = open('hecho.html','w')
        f.write(html)
        f.close()
        parser.feed(html)
print(parser.bodyData)

exit()
#print("----------")
#print(bodyData)

# Coloca primero el acronimo del proyecto para seguir un orden logico
#contador=1
#for i in range(len(parser.bodyData)):
#    if contador == 6:
#        parser.bodyData.insert(i-5, parser.bodyData.pop(i))
#        parser.bodyData.insert(i-5, parser.bodyData.pop(i))
#    if "Rcn" in parser.bodyData[i]:
#        contador=1
#    contador+=1
#print("----------")
#print(bodyData)
f = open('salida.xml','w')
for i in range(len(parser.bodyData)):
    f.write(parser.bodyData[i])
f.close()

#convierte a arbol xml los proyectos
top = ET.Element("CGProjects")
exit()
for i in range(len(parser.bodyData)):
    if(parser.bodyData[i] == "Project acronym"):
        lastProject = ET.SubElement(top, "Project")
        lastProject.attrib={"acronym":parser.bodyData[i+1]}
    elif(parser.bodyData[i] == "Rcn"):
        rcn = ET.SubElement(lastProject, "Rcn")
        rcn.text = parser.bodyData[i+1]
    elif(parser.bodyData[i] == "Nid"):
        nid = ET.SubElement(lastProject, "Nid")
        nid.text = parser.bodyData[i+1]
    elif(parser.bodyData[i] == "Host Institution (HI)"):
        hi = ET.SubElement(lastProject, "HI")
        hi.text = parser.bodyData[i+1]
    elif(parser.bodyData[i] == "Project"):
        p = ET.SubElement(lastProject, "Name")
        p.text = parser.bodyData[i+1]
    elif(parser.bodyData[i] == "Researcher (PI)"):
        pi = ET.SubElement(lastProject, "PI")
        pi.text = parser.bodyData[i+1]
    elif(parser.bodyData[i] == "Call details"):
        cd = ET.SubElement(lastProject, "Call_Details")
        cd.text = parser.bodyData[i+1]
    elif(parser.bodyData[i] == "Summary"):
        sm = ET.SubElement(lastProject, "Summary")
        sm.text = parser.bodyData[i+1]
    elif(parser.bodyData[i] == "Website (HI)"):
        if(parser.bodyData[i+1] != "Max ERC funding"):
            web = ET.SubElement(lastProject, "Web")
            web.text = parser.bodyData[i+1]
        else:
            web = ET.SubElement(lastProject, "Web")
            web.text = " "
    elif(parser.bodyData[i] == "Max ERC funding"):
        mef = ET.SubElement(lastProject, "Max_ERC_funding")
        mef.text = parser.bodyData[i+1]
    elif(parser.bodyData[i] == "Duration"):
        dur = ET.SubElement(lastProject, "Duration")
        sd = ET.SubElement(dur, "Start_date")
        sd.text = parser.bodyData[i+2]
        ed = ET.SubElement(dur, "End_date")
        ed.text = parser.bodyData[i+4]
        i+=4
    else:
        pass
    i+=1
f = open('salida.xml','w')
f.write('<?xml version="1.0" encoding="utf-8"?>')
f.write('<!DOCTYPE CGProjects SYSTEM "validador.dtd">')
f.close()
# excritura en un fichero xml del arbol
tree = ET.ElementTree(top)
tree.write("salida.xml")
