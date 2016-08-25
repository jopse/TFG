# -*- coding: utf-8 -*-
'''
Created on 18/08/2016

@author: Jose Angel Gonzalez Mejias
'''
import urllib.request as request
import sys
import http.client
import json

def main():
    conn = http.client.HTTPSConnection("api.elsevier.com")
    URL = "/content/search/author?query=authlast({0})%20and%20authfirst({1})&apiKey=b3a71de2bde04544495881ed9d2f9c5b"
    headers = {
        'cache-control': "no-cache"
    }
    name = "michael"
    lastName = "gonzalez harbour"
    conn.request("GET", URL.format(name,lastName), headers=headers)

    res = conn.getresponse()
    data = res.read()
    print(data)
    #data_string = json.load(data)
    #entradas = data_string
    #for entrada in entradas:
    #    if(name == entrada['preferred-name']['given-name'].lower() and lastName == entrada['preferred-name']['surname'].lower()):
    #        print(entrada['preferred-name'])
    #print(entradas)
if __name__ == "__main__":
    main()
