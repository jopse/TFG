# -*- coding: utf-8 -*-
'''
Created on 26/08/2016

@author: Jose Angel Gonzalez Mejias
'''
from view import gui
from controller import *
from controller import *
from model import id3

def main():
    #Descarga de proyectos
    #Descarga de todos los datos
    gui.main()

    #Sacar investigador y datos de cada investigador y guardarlo
    gui.sacaInfoDeXML()

    #Busqueda de PI
    ###Varios resultados -> muestra de todos y seleccion de uno
    panelSelected = gui.selectPanel()
    piSelected = gui.enterInfo()

    values = piSelected.split(" - ")
    fullName = values[1].split(", ")
    infoDeXML.getPITestValues(fullName[0],fullName[1],values[2],panelSelected.split[" - "][0])

    #Unir clases true con clases false
    unificador.main()

    #Aplicar ID3
    id3.main('resources/trainning.txt','test.txt',9)


if __name__ == "__main__":
    main()
