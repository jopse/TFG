# -*- coding: utf-8 -*-
'''
Created on 26/08/2016

@author: Jose Angel Gonzalez Mejias
'''
from view import gui
from controller import *
from controller import unificador

def main():
    #Descarga de proyectos
    #Descarga de todos los datos
    gui.main()

    #Sacar investigador y datos de cada investigador y guardarlo
    gui.sacaInfoDeXML()
    #Descarga datos de cuartiles
    gui.descargaJRC()
    #Busqueda de PI
    ###Varios resultados -> muestra de todos y seleccion de uno

    panelSelected = False
    while panelSelected is False:
        gui.Must()
        panelSelected = gui.selectPanel()
    piSelected = gui.enterInfo()

    values = piSelected.split(" - ")
    fullName = values[1].split(", ")
    infoDeXML.getPITestValues(fullName[0],fullName[1],values[2].split(":")[1],panelSelected.split(" - ")[0])

    #Unir clases true con clases false
    unificador.main()

    #Aplicar ID3
    gui.muestraResultado()

    #Mostrar estadísticas
    gui.muestraEstadisticas(values[2].split(":")[1],panelSelected.split(" - ")[0])

if __name__ == "__main__":
    main()
