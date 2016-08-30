# -*- coding: utf-8 -*-
'''
Created on 22/08/2016

@author: Jose Angel Gonzalez Mejias
'''
import easygui as gui
import sys
import os

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
            break # no problems found
        else:
            errorMsg(enterInfo,errmsg,title)
    return fieldValues
def descarga(desc, projectType):
    gui.msgbox("Inicializando, espere por favor...")
    condicion = False
    while(condicion == False):
        print("Start {0!s}".format(projectType))
        desc.main(projectType)
        condicion1 = os.path.isfile('resources/final_{0}_P1.xml'.format(projectType))
        condicion2 = os.path.isfile('resources/final_{0}_P2.xml'.format(projectType))
        condicion3 = os.path.isfile('resources/final_{0}_P3.xml'.format(projectType))
        condicion4 = os.path.isfile('resources/final_{0}_P4.xml'.format(projectType))
        if(condicion1 and condicion2 and condicion3 and condicion4): condicion = True

def main(desc, msg="Bienvenido al identificador", title="Identificador", ok_button="OK"):
    root = gui.ccbox(msg, title, ('Entrar','Hasta pronto'))

    if root:
        descarga(desc, 'PoC')
        descarga(desc, 'CoG')
        descarga(desc, 'AdG')
        descarga(desc, 'SyG')
        #descarga(desc, 'StG')
        return enterInfo()
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
