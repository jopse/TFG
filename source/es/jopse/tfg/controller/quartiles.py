# -*- coding: utf-8 -*-
from urllib import request
from xlrd import open_workbook
import operator
import os

def main():

    #os.remove('resources/SJR.xlsx')
    #request.urlretrieve ("https://www.journalmetrics.com/documents/SNIP_IPP_SJR_complete_1999_2015%20(June%202016).xlsx", "resources/SJR.xlsx")
    #book = open_workbook('resources/SJR.xlsx')
    book = open_workbook('resources/SNIP_IPP_SJR_complete_1999_2015%20(June%202016).xlsx')
    sheet = book.sheet_by_index(0)
    nrows = sheet.nrows
    ncols = sheet.ncols
    nJournals = ncols-1
    sjrList,maxList,qList = {1999:[],2000:[],2001:[],2002:[],2003:[],2004:[],2005:[],2006:[],2007:[],2008:[],2009:[],2010:[],2011:[],2012:[],2013:[],2014:[],2015:[]},{},{}
    for row_index in range(nrows):
        if row_index == 0:
            continue
        try:
            os.remove('resources/journals/{0}.txt'.format(sheet.cell(row_index,3).value))
        except OSError:
            pass
        f = open('resources/journals/{0}.txt'.format(sheet.cell(row_index,3).value),'a+')
        f.write('{"sjr":{')
        year = ""
        for col_index in range(9,56):
            #Saco los valores de cada Journal para cada año
            if(col_index == 9):
                year = 1999
            elif(col_index == 12):
                year = 2000
            elif(col_index == 15):
                year = 2001
            elif(col_index == 18):
                year = 2002
            elif(col_index == 21):
                year = 2003
            elif(col_index == 24):
                year = 2004
            elif(col_index == 26):
                year = 2005
            elif(col_index == 29):
                year = 2006
            elif(col_index == 32):
                year = 2007
            elif(col_index == 35):
                year = 2008
            elif(col_index == 38):
                year = 2009
            elif(col_index == 41):
                year = 2010
            elif(col_index == 44):
                year = 2011
            elif(col_index == 46):
                year = 2012
            elif(col_index == 49):
                year = 2013
            elif(col_index == 52):
                year = 2014
            elif(col_index == 55):
                year = 2015
            else:
                continue
            value = sheet.cell(row_index,col_index).value.replace(".","")
            sjrList[year].append(value)
            if year == 2015:
                f.write('"{0}":"{1}"'.format(year,value))
            else:
                f.write('"{0}":"{1}",'.format(year,value))
        f.write('}}')
        f.close()
    #Max & min de cada año
    for year in range(1999,2016):
        currentMax = int(max(sjrList[year]))
        maxList[year] = currentMax
        qList[year] = [1*(currentMax/4),2*(currentMax/4),3*(currentMax/4),4*(currentMax/4)]
    try:
        os.remove('resources/quartiles.txt')
    except OSError:
        pass
    f = open('resources/quartiles.txt','w')
    f.write('{"quartiles":{')
    for q in qList:
        qs = qList[q]
        if q == 2015:
            f.write('"{0}":{{'.format(q))
            f.write('"q1":"{0}","q2":"{1}","q3":"{2}","q4":"{3}"}}'.format(qs[0],qs[1],qs[2],qs[3]))
        else:
            f.write('"{0}":{{'.format(q))
            f.write('"q1":"{0}","q2":"{1}","q3":"{2}","q4":"{3}"}},'.format(qs[0],qs[1],qs[2],qs[3]))

    f.write('}}')
    f.close()
if __name__ == "__main__":
    main()
