# -*- coding: utf-8 -*-
'''
Created on 19/1/2016

@author: Jose Angel Gonzalez Mejias
'''
import descarga as program
import logging

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='example.log',level=logging.INFO)
    logging.info('Downloading CoG')
    program.main('CoG')
    logging.info('Downloading StG')
    program.main('StG')
    logging.info('Downloading PoC')
    program.main('PoC')
    logging.info('Finished Download')

if __name__ == '__main__':
    main()
