# -*- coding: utf-8 -*-
'''
Created on 30/09/2016

@author: Jose Angel Gonzalez Mejias
'''
import glob

def main():
    files = glob.glob("resources/authors/*.txt")

    absoluteFile = open('resources/trainning.txt','w')
    for authorFile in files:
        with open('authorFile') as f:
            lines = f.readlines()
            absoluteFile.write(lines)

    absoluteFile.close()

if __name__ == "__main__":
    main(sys.argv)
