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
    todosProyecto = []
    bodyData = dict()
    projects = False
    esEtiqueta = False
    saltarEtiqueta = False
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
                self.esEtiqueta = True
                self.saltarEtiqueta = False
            elif data == "Website (HI)":
                self.empiezaP+=1
                self.esEtiqueta = True
                self.saltarEtiqueta = True
            elif data == "Duration":
                self.empiezaP+=1
                self.esEtiqueta = True
                self.saltarEtiqueta = True
            else:
                self.saltarEtiqueta = False
            if self.empiezaP == 8 and data != "Researcher (PI)":
                self.empiezaP+=2
            if self.empiezaP >= 0 and self.esEtiqueta and not self.saltarEtiqueta:
                self.etiqueta = data
                self.empiezaP+=1
                self.esEtiqueta = False
            elif self.empiezaP >= 0 and not self.esEtiqueta and not self.saltarEtiqueta:
                self.bodyData[self.etiqueta] = data
                self.empiezaP+=1
                self.esEtiqueta = True
            if self.empiezaP > 23:
                self.empiezaP = -1
                self.todosProyecto.append(self.bodyData)
                self.bodyData = dict()
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

top = ET.Element("CGProjects")
#Recorre todas las 62 paginas para extraer los proyectos solamente
f = open('hecho.html','a')
for i in range(62):
    with request.urlopen(URL.format(ABBR['CoG'],'CoG',i)) as response:
        html = response.read()
        html = html.decode('utf-8')
        f.write(html)
        parser.feed(html)
f.close()
#convierte a arbol xml los proyectos
for j in range(len(parser.todosProyecto)):
    proyectoAux = parser.todosProyecto[j]
    lastProject = ET.SubElement(top, 'Project')
    print(proyectoAux)
    lastProject.attrib={'acronym':proyectoAux['Project acronym']}
    rcn = ET.SubElement(lastProject, 'Rcn')
    rcn.text = proyectoAux['Rcn']
    nid = ET.SubElement(lastProject, 'Nid')
    nid.text = proyectoAux['Nid']
    hi = ET.SubElement(lastProject,'HI')
    hi.text = proyectoAux['Host Institution (HI)']
    p = ET.SubElement(lastProject,'Name')
    p.text = proyectoAux['Project']
    pi = ET.SubElement(lastProject,'PI')
    if 'Researcher (PI)' in proyectoAux:
        pi.text = proyectoAux['Researcher (PI)']
    else:
        pi.text = " "
    cd = ET.SubElement(lastProject,'Call_Details')
    cd.text = proyectoAux['Call details']
    sm = ET.SubElement(lastProject,'Summary')
    sm.text = proyectoAux['Summary']
    mef = ET.SubElement(lastProject,'Max_ERC_funding')
    mef.text = proyectoAux['Max ERC funding']
    dur = ET.SubElement(lastProject,'Duration')
    sd = ET.SubElement(dur,'Start_date')
    sd.text = proyectoAux['Start date:']
    ed = ET.SubElement(dur, "End_date")
    ed.text = proyectoAux['End date:']

f = open('salida.xml','w')
f.write('<?xml version="1.0" encoding="utf-8"?>')
f.write('<!DOCTYPE CGProjects SYSTEM "validador.dtd">')
f.close()
# excritura en un fichero xml del arbol
tree = ET.ElementTree(top)
tree.write("salida.xml")
