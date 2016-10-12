# -*- coding: utf-8 -*-
'''
Created on 18/08/2016

@author: Jose Angel Gonzalez Mejias
'''
import sys
import json
import requests
from model import author


def main(fieldValues):
    name = fieldValues[0]
    lastName = fieldValues[1]

    return buscaAutorPorNombreApellido(name,lastName)

def buscaAutorPorNombreApellido(name,lastName):
    f = open('resources/application.properties','r')
    properties = f.read()
    properties = json.loads(properties)
    apiKey = properties["ApiKey"]
    f.close()

    authors = []
    url = "https://api.elsevier.com/content/search/author"
    query = "authlast({0}) and authfirst({1})".format(lastName,name)
    querystring = {"query":query,"apiKey":apiKey}
    headers = {
        'accept': "application/json",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    decoded = json.loads(response.text)

    entradas = decoded["search-results"]["entry"]
    totalResults = int(decoded["search-results"]["opensearch:totalResults"])
    if totalResults > 0:
        for entrada in entradas:
            authors.append(author.Author(entrada["preferred-name"]["initials"],entrada["preferred-name"]["given-name"],entrada["preferred-name"]["surname"],entrada["dc:identifier"]))
    else:
        print("Autor no encontrado {0} {1}".format(name,lastName))
        return 0
    #Devuelve los resultados de la busqueda
    return authors

def buscaIDPorNombreApellidoHI(nombre,apellidos,hi):
    f = open('resources/application.properties','r')
    properties = f.read()
    properties = json.loads(properties)
    apiKey = properties["ApiKey"]
    f.close()

    authors = []
    url = "https://api.elsevier.com/content/search/author"
    query = "authlast({0}) and authfirst({1}) and affil({2})".format(apellidos,nombre,hi)

    querystring = {"query":query,"apiKey":apiKey}
    headers = {
        'accept': "application/json",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    decoded = json.loads(response.text)

    entradas = decoded["search-results"]["entry"]
    return entradas[0]["dc:identifier"]

if __name__ == "__main__":
    main()
