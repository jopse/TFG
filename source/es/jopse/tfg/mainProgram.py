# -*- coding: utf-8 -*-
'''
Created on 19/1/2016

@author: Jose Angel Gonzalez Mejias
'''
import descarga as program
import buscaInformador as buscador
from tkinter import *
import logging

def main():
    
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='example.log',level=logging.DEBUG)
    logging.info('Descargando Proyectos CoG')
    program.main('CoG')
    logging.info('Descargando Proyectos StG')
    program.main('StG')
    logging.info('Descargando Proyectos PoC')
    program.main('PoC')
    
    logging.info('Descargando investigadores de CoG')
    investigadores = buscador.main('CoG')
    logging.info('Descargando investigadores de StG')
    for investigador in buscador.main('StG'):
        if investigador not in investigadores:
            investigadores.append(investigador)
    logging.info('Descargando investigadores de PoC')
    for investigador in buscador.main('PoC'):
        if investigador not in investigadores:
            investigadores.append(investigador)
            
    logging.info('Inversion nombres de investigadores')
    for investigador in investigadores:
        investigador.split()
        investigador.reverse()
    
    
    
    #ventana = Tk()
    #ventana.config()
    #pad=3
    #ventana.geometry("{0}x{1}+0+0".format(ventana.winfo_screenwidth()-pad, ventana.winfo_screenheight()-pad))
    #ventana.resizable(width=FALSE, height=FALSE)
    #ventana.title("Universidad de Cantabria")
    #ventana.mainloop()
    
    
if __name__ == '__main__':
    main()
