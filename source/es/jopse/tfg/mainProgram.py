# -*- coding: utf-8 -*-
'''
Created on 19/1/2016

@author: Jose Angel Gonzalez Mejias
'''
import descarga as program
import logging
from tkinter import *

def main():
    
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='example.log',level=logging.INFO)
    logging.info('Downloading CoG')
    program.main('CoG')
    logging.info('Downloading StG')
    program.main('StG')
    logging.info('Downloading PoC')
    program.main('PoC')
    logging.info('Finished Download')
    
    ventana = Tk()
    ventana.config()
    pad=3
    ventana.geometry("{0}x{1}+0+0".format(ventana.winfo_screenwidth()-pad, ventana.winfo_screenheight()-pad))
    ventana.resizable(width=FALSE, height=FALSE)
    ventana.title("Universidad de Cantabria")
    ventana.mainloop()
    
    
if __name__ == '__main__':
    main()