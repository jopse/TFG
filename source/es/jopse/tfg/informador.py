# -*- coding: utf-8 -*-
'''
Created on 17/2/2016

@author: Jose Angel Gonzalez Mejias
'''
from selenium import selenium

def main():
        selenium = selenium("localhost", 4444, "*chrome", "https://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=Y2vqevvN9vQCNYmXZRx&preferencesSaved=")
        selenium.start()

        sel = selenium
        sel.open("/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=Y2vqevvN9vQCNYmXZRx&preferencesSaved=")
        sel.type("id=value(input1)", "Tirnauca Cristina")
        sel.click("id=UA_GeneralSearch_input_form_sb")
        sel.wait_for_page_to_load("30000")
    
        selenium.stop()

if __name__ == "__main__":
    main()
