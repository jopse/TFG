# -*- coding: utf-8 -*-
'''
Created on 17/2/2016

@author: Jose Angel Gonzalez Mejias
'''
import xml.etree.ElementTree as ET
import sys

def main(argv):
    global projectType
    projectType = argv
    
    investigadores = []
    
    tree = ET.parse('salida_{0}.xml'.format(projectType))
    root = tree.getroot()
    for project in root:
        for child in project:
            if child.tag == 'PI':
                if not child.text == ' ':
                    investigadores.append(child.text)
    return investigadores

if __name__ == "__main__":
    main(sys.argv)
