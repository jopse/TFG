# -*- coding: utf-8 -*-
'''
Created on 1/10/2015

@author: Jose Angel Gonzalez Mejias
'''
import urllib.request as request
import logging
from html.entities import name2codepoint
from html.parser import HTMLParser
import xml.etree.cElementTree as ET
import sys

SHORT_URL="/projects-and-results/erc-funded-projects?f[2]=sm_field_cordis_project_funding%3A{0!s}%20%28{1!s}%29"
URL = "http://erc.europa.eu"+SHORT_URL+"&page={2!s}"
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
    pages = False
    numPages = 0
    def handle_starttag(self, tag, attrs):
        if(tag == "ul"):
            self.projects = True
        elif(tag == "a" and SHORT_URL.format(ABBR[projectType],projectType) in attrs):
            self.pages = True
    def handle_endtag(self, tag):
        if(tag == "ul"):
            self.projects = False
        elif(tag == "a"):
            self.pages = False
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
        elif self.pages:
            self.numPages = data
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

def main(argv):
    global projectType
    projectType = argv

    #Creacion del parser
    parser=MyHTMLParser()
    parser2=MyHTMLParser()

    top = ET.Element("{0}Projects".format(projectType))
    #Recorre todas las paginas para extraer los proyectos
    #f = open('salida_{0}.html'.format(projectType),'a')
    pages = 0
    with request.urlopen(URL.format(ABBR[projectType],projectType,0)) as response:
        html = response.read()
        html = html.decode('utf-8')
        #f.write(html)
        parser2.feed(html)
        pages = parser2.numPages
    #f.close()
    #f = open('salida_{0}.html'.format(projectType),'a')
    for i in range(pages):
        with request.urlopen(URL.format(ABBR[projectType],projectType,i)) as response2:
            html2 = response2.read()
            html2 = html2.decode('utf-8')
            #f.write(html)
            parser.feed(html)
    #f.close()
    #convierte a arbol xml los proyectos
    for j in range(len(parser.todosProyecto)):
        proyectoAux = parser.todosProyecto[j]
        lastProject = ET.SubElement(top, 'Project')
        try:
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
        except KeyError:
            continue
    f = open('salida_{0}.xml'.format(projectType),'w')
    f.write('<?xml version="1.0" encoding="utf-8"?>')
    f.write('<!DOCTYPE {0}Projects SYSTEM "validador.dtd">'.format(projectType))
    f.close()
    # excritura en un fichero xml del arbol
    tree = ET.ElementTree(top)
    tree.write('salida_{0}.xml'.format(projectType))

if __name__ == "__main__":
    main(sys.argv)
