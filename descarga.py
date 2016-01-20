# -*- coding: utf-8 -*-
'''
Created on 1/10/2015

@author: Jose Angel Gonzalez Mejias
'''
import urllib.request as request
from html.entities import name2codepoint
from html.parser import HTMLParser
import xml.etree.cElementTree as ET

'''
Redefinición de metodos para facilitar el parseado
'''
bodyData = []
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print ("Start tag:", tag)
        for attr in attrs:
            print ("     attr:", attr)
    def handle_endtag(self, tag):
        print ("End tag  :", tag)
    def handle_data(self, data):
        global bodyData
        bodyData.append(data)
        print ("Data     :", data)
    def handle_comment(self, data):
        print ("Comment  :", data)
    def handle_entityref(self, name):
        c = name2codepoint[name]
        print ("Named ent:", c)
    def handle_charref(self, name):
        if name.startswith('x'):
            c = int(name[1:], 16)
        else:
            c = int(name)
        print ("Num ent  :", c)
    def handle_decl(self, data):
        print ("Decl     :", data)

#Creacion del parser
parser=MyHTMLParser()
#Variable que contendra todo el codigo de todos los proyectos
consolidatorGrantsProjects=""

#Recorre todas las 62 paginas para extraer los proyectos solamente
for i in range(62):
    page=str(i)
    url='http://erc.europa.eu/projects-and-results/erc-funded-projects?f[1]=sm_field_cordis_project_funding%3AConsolidator%20Grants%20%28CoG%29&page=' + page
    with request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
        contenido = html.split('<ul>')
        contenido = contenido[1]
        contenido = contenido.split('</ul>')
        contenido = contenido[0]
        #print(contenido)
        consolidatorGrantsProjects+=contenido
parser.feed(consolidatorGrantsProjects)

print("----------")
print(bodyData)

# Coloca primero el acronimo del proyecto para seguir un orden logico
contador=1
for i in range(len(bodyData)):
    if contador == 6:
        bodyData.insert(i-5, bodyData.pop(i))
        bodyData.insert(i-5, bodyData.pop(i))
    if "Rcn" in bodyData[i]:
        contador=1
    contador+=1
print("----------")
print(bodyData)

#convierte a arbol xml los proyectos
top = ET.Element("CGProjects")
for i in range(len(bodyData)):
    if(bodyData[i] == "Project acronym"):
        lastProject = ET.SubElement(top, "Project")
        lastProject.attrib={"name":bodyData[i+1]}
    elif(bodyData[i] == "Rcn"):
        rcn = ET.SubElement(lastProject, "Rcn")
        rcn.text = bodyData[i+1]
    elif(bodyData[i] == "Nid"):
        nid = ET.SubElement(lastProject, "Nid")
        nid.text = bodyData[i+1]
    elif(bodyData[i] == "Host Institution (HI)"):
        hi = ET.SubElement(lastProject, "HI")
        hi.text = bodyData[i+1]
    elif(bodyData[i] == "Project"):
        p = ET.SubElement(lastProject, "Project")
        p.text = bodyData[i+1]
    elif(bodyData[i] == "Researcher (PI)"):
        pi = ET.SubElement(lastProject, "PI")
        pi.text = bodyData[i+1]
    elif(bodyData[i] == "Call details"):
        cd = ET.SubElement(lastProject, "Call_Details")
        cd.text = bodyData[i+1]
    elif(bodyData[i] == "Summary"):
        sm = ET.SubElement(lastProject, "Summary")
        sm.text = bodyData[i+1]
    elif(bodyData[i] == "Website (HI)"):
        if(bodyData[i+1] != "Max ERC funding"):
            web = ET.SubElement(lastProject, "Web")
            web.text = bodyData[i+1]
        else:
            web = ET.SubElement(lastProject, "Web")
            web.text = " "
    elif(bodyData[i] == "Max ERC funding"):
        mef = ET.SubElement(lastProject, "Max_ERC_funding")
        mef.text = bodyData[i+1]
    elif(bodyData[i] == "Duration"):
        dur = ET.SubElement(lastProject, "Duration")
        sd = ET.SubElement(dur, "Start_date")
        sd.text = bodyData[i+2]
        ed = ET.SubElement(dur, "End_date")
        ed.text = bodyData[i+4]
        i+=4
    i+=1

# excritura en un fichero xml del arbol
tree = ET.ElementTree(top)
tree.write("salida.xml")
