# -*- coding: utf-8 -*-
'''
Created on 12/09/2016

@author: Jose Angel Gonzalez Mejias
'''
import matplotlib.pyplot as plt
def main(quartilesPI):
    # The slices will be ordered and plotted counter-clockwise.
    labels = 'Q1', 'Q2', 'Q2', 'Q$'
    sizes = [quartilesPI[0], quartilesPI[1], quartilesPI[2], quartilesPI[3]]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

    plt.show()
