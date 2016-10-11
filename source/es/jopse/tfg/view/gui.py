# -*- coding: utf-8 -*-
'''
Created on 22/08/2016

@author: Jose Angel Gonzalez Mejias
'''
import easygui as gui
import sys
import os
from controller import descarga
from controller import buscaPIinfo
from controller import piInfo
from controller import infoDeXML
from model import author

def errorMsg(methodToRun, errmsg, title):
    gui.msgbox(errmsg, title)
    methodToRun()

def enterInfo():
    msg = "Por favor, inserta la información del investigador"
    title = "Identificador"
    fieldNames = ["Nombre","Apellidos"]
    fieldValues = []
    fieldValues = gui.multenterbox(msg, title, fieldNames)

    # make sure that none of the fields was left blank
    while 1:
        if fieldValues == None: break #Resultado vacio
        if fieldValues == False: break #Boton cancel
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" es un campo requerido.\n\n' % fieldNames[i])

        if errmsg == "":
            # no problems found
            authors = buscaPIinfo.main(fieldValues)
            msg ="Elige un resultado para continuar:"
            title = "Identificador"
            choices = []
            for a in authors:
                choices.append("{0} - {1}, {2} - {3}".format(a.initials,a.surename,a.givenName,a.identifier))
            choice = gui.choicebox(msg, title, choices)
            return choice
        else:
            errorMsg(enterInfo, errmsg, title)
            return

def selectPanel():
    msg ="Elige un panel para continuar:"
    title = "Identificador"
    choices = []
    paneles = ["P1 - (PE) Physical Sciences & Engineering","P2 - (LS) Life Sciences","P3 - (SH) Social Sciences & Humanities","P4 - (ID) Interdisciplinary"]
    for panel in paneles:
        choices.append(panel)
    choice = gui.choicebox(msg, title, choices)
    return choice

def descargaFicheros(projectType):
    gui.msgbox("Inicializando, espere por favor...")
    condicion1 = os.path.isfile('resources/final_{0}_P1.xml'.format(projectType))
    condicion2 = os.path.isfile('resources/final_{0}_P2.xml'.format(projectType))
    condicion3 = os.path.isfile('resources/final_{0}_P3.xml'.format(projectType))
    condicion4 = os.path.isfile('resources/final_{0}_P4.xml'.format(projectType))
    if(condicion1 and condicion2 and condicion3 and condicion4):
        if confirmacionDescarga(projectType):
            print("Start {0!s}".format(projectType))
            descarga.main(projectType)
    else:
        descarga.main(projectType)

def confirmacionDescarga(projectType):
    return gui.ccbox("Ya hay proyectos descargados de {0}. ¿Quiere actualizar los datos?".format(projectType))

def showPIinfo(piSelected):
    piID = piSelected.split(",")[1].split("-")[1].split(" ")[1].split(":")[1]
    piInfo.main(piID)

def sacaInfoDeXML():
    projectTypes = ["CoG","AdG","StG"]
    for projectType in projectTypes:
        for i in range(1,4):
            infoDeXML.main(i,projectType)

def main(msg="Bienvenido al identificador", title="Identificador", ok_button="OK"):
    root = gui.ccbox(msg, title, ('Entrar','Hasta pronto'))

    if root:
        #descargaFicheros('PoC')
        descargaFicheros('CoG')
        descargaFicheros('AdG')
        #descargaFicheros('SyG')
        descargaFicheros('StG')
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
