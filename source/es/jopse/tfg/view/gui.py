# -*- coding: utf-8 -*-
'''
Created on 22/08/2016

@author: Jose Angel Gonzalez Mejias
'''
import easygui as gui
import sys

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
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
          if fieldValues[i].strip() == "":
            errmsg = errmsg + ('"%s" es un campo requerido.\n\n' % fieldNames[i])

        if errmsg == "":
            fieldValues = gui.multenterbox(errmsg, title, fieldNames, fieldValues)
            break # no problems found
        else:
            errorMsg(enterInfo,errmsg,title)
    print("Reply was:", fieldValues)

def main(msg="Bienvenido al identificador", title="Identificador", ok_button="OK"):
    root = gui.ccbox(msg, title, ('Entrar','Hasta pronto'))
    if root:
        enterInfo()
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
