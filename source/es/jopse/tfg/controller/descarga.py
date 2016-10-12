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
import sys, os
from shutil import copyfile

SHORT_URL="/projects-and-results/erc-funded-projects?f[2]=sm_field_cordis_project_funding%3A{0!s}%20%28{1!s}%29"
URL = "http://erc.europa.eu{0!s}&page={1!s}"
ABBR = {'CoG':'Consolidator%20Grants','StG':'Starting%20Grant','PoC':'Proof%20of%20Concept', 'AdG':'Advanced%20Grant','SyG':'Synergy%20Grants'}
PANEL = {'P1':'/projects-and-results/erc-funded-projects?f[0]=sm_field_cordis_project_subpanel%3APE1&f[1]=sm_field_cordis_project_subpanel%3APE2&f[2]=sm_field_cordis_project_subpanel%3APE3&f[3]=sm_field_cordis_project_subpanel%3APE4&f[4]=sm_field_cordis_project_subpanel%3APE5&f[5]=sm_field_cordis_project_subpanel%3APE6&f[6]=sm_field_cordis_project_subpanel%3APE7&f[7]=sm_field_cordis_project_subpanel%3APE8&f[8]=sm_field_cordis_project_subpanel%3APE9&f[9]=sm_field_cordis_project_subpanel%3APE10&f[12]=sm_field_cordis_project_funding%3A{0!s}%20%28{1!s}%29', 'P2':'/projects-and-results/erc-funded-projects?f[0]=sm_field_cordis_project_funding%3A{0!s}%20%28{1!s}%29&f[1]=sm_field_cordis_project_subpanel%3ALS1&f[2]=sm_field_cordis_project_subpanel%3ALS2&f[3]=sm_field_cordis_project_subpanel%3ALS3&f[4]=sm_field_cordis_project_subpanel%3ALS4&f[5]=sm_field_cordis_project_subpanel%3ALS5&f[6]=sm_field_cordis_project_subpanel%3ALS6&f[7]=sm_field_cordis_project_subpanel%3ALS7&f[8]=sm_field_cordis_project_subpanel%3ALS8&f[9]=sm_field_cordis_project_subpanel%3ALS9', 'P3':'/projects-and-results/erc-funded-projects?f[0]=sm_field_cordis_project_funding%3A{0!s}%20%28{1!s}%29&f[1]=sm_field_cordis_project_subpanel%3ASH1&f[2]=sm_field_cordis_project_subpanel%3ASH2&f[3]=sm_field_cordis_project_subpanel%3ASH3&f[4]=sm_field_cordis_project_subpanel%3ASH4&f[5]=sm_field_cordis_project_subpanel%3ASH5&f[6]=sm_field_cordis_project_subpanel%3ASH6','P4':'/projects-and-results/erc-funded-projects?f[0]=sm_field_cordis_project_funding%3A{0!s}%20%28{1!s}%29&f[1]=sm_field_cordis_project_subpanel%3AID1'}

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
        elif(tag == "a"):
            for attr in attrs:
                if("class" in attr and 'last active' in attr):
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
        if self.pages:
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
    try:
        main2(argv, 'P1')
    except Exception:
        print('salio una excepcion')
    try:
        main2(argv, 'P2')
    except Exception:
        print('salio una excepcion')
        pass
    try:
        main2(argv, 'P3')
    except Exception:
        print('salio una excepcion')
        pass
    try:
        main2(argv, 'P4')
    except Exception:
        print('salio una excepcion')
        pass

def main2(argv, pan):
    global projectType
    projectType = argv
    global urlToOpen
    urlToOpen = PANEL[pan]

    #Creacion del parser
    parser=MyHTMLParser()
    parser2=MyHTMLParser()

    top = ET.Element("Projects".format(projectType,pan))
    #Recorre todas las paginas para extraer los proyectos
    allPages = False
    pages = 0
    while(allPages == False):
        if(pages == 0):
            with request.urlopen(URL.format(urlToOpen.format(ABBR[projectType],projectType),0)) as response:
                html = response.read()
                html = html.decode('utf-8')

                parser2.feed(html)
                pages = parser2.numPages
                pages = int(pages)
                if(pages==0):
                    f = open('resources/projects/final_{0}_{1}.xml'.format(projectType,pan),'w')
                    f.write('<?xml version="1.0" encoding="ISO-8859-1"?>')
                    f.write('<!DOCTYPE {0}Projects Panel{1}SYSTEM "validador.dtd">'.format(projectType,pan))
                    f.close()
                    raise Exception
                print(pages)
        else:
            for i in range(pages):
                #print(i)
                #print(URL.format(urlToOpen.format(ABBR[projectType],projectType),str(i)))
                with request.urlopen(URL.format(urlToOpen.format(ABBR[projectType],projectType),str(i))) as response2:
                    html2 = response2.read()
                    html2 = html2.decode('ISO-8859-1')

                    parser.feed(html2)
            allPages = True

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
    f = open('resources/projects/salida_{0}_{1}.xml'.format(projectType,pan),'w')
    f.write('<?xml version="1.0" encoding="ascii"?>')
    f.write('<!DOCTYPE {0}Projects Panel{1}SYSTEM "validador.dtd">'.format(projectType,pan))
    f.close()
    # excritura en un fichero xml del arbol
    tree = ET.ElementTree(top)
    tree.write('resources/projects/salida_{0}_{1}.xml'.format(projectType,pan))
    copyfile('resources/projects/salida_{0}_{1}.xml'.format(projectType,pan),'resources/projects/final_{0}_{1}.xml'.format(projectType,pan))
    os.remove('resources/projects/salida_{0}_{1}.xml'.format(projectType,pan))

if __name__ == "__main__":
    main(sys.argv)
