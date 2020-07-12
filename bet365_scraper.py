# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Load libraries
import selenium.common.exceptions
import time
import traceback
import json
import sys

#Auxiliar functions
def open_all(driver):
    # This function is no longer needed given that the bet365 webpage now displays 
    # all th edata openly.
    while True:
        try:
            # open_matches = driver.find_elements_by_class_name('slm-Market_HeaderClosed')
            open_matches = driver.find_elements_by_class_name('sm-SplashMarket_Header.sm-SplashMarket_HeaderOpen')
            for om in open_matches:
                om.click() 
            break
        except:
            traceback.print_exc(file=sys.stdout)
            continue

#Get the urls of all the matches
def get_matches_urls(driver):
    def get_matches():
        num_retries = 0
        while num_retries < 2:
            try:
                # all_matches = driver.find_elements_by_class_name("slm-CouponLink_Label")
                all_matches = driver.find_elements_by_class_name("sm-CouponLink_Title")
                break
            except:
                traceback.print_exc(file=sys.stdout)
                num_retries += 1
                continue
        return all_matches

    def match_click(all_matches, m):
        num_retries = 0
        while num_retries < 2:
            try:
                all_matches[m].click()
                break
            except:
                traceback.print_exc(file=sys.stdout)
                num_retries += 1
                continue 
            
    f = open('bet365_urls.json','w')
    # open_all(driver)
    all_matches = get_matches()
    all_matches_names = [a.text for a in all_matches]
    rango = list(range(len(all_matches_names)))
    for ai in rango:
        if (all_matches_names[ai] == ''):
            rango.remove(ai)
    fix_len = len(all_matches)
    all_matches_names_principal, all_matches_names_secondary = [], []
    urls_principal, urls_secondary = [], []
    urls_dict = {}
    for m in rango:
        try:
            match_click(all_matches, m)
            url = driver.current_url
            opens = driver.find_elements_by_class_name('cm-CouponMarketGroupButton_Text')
            if (len(opens) > 2):
                urls_principal.append(url)
                all_matches_names_principal.append(all_matches_names[m])
            else:
                urls_secondary.append(url)
                all_matches_names_secondary.append(all_matches_names[m])
                  
            time.sleep(1.5)
            print(m, all_matches_names[m], fix_len, len(all_matches))
        except:
            print('ERROR')
            traceback.print_exc(file=sys.stdout)     
            continue
        driver.back()
        open_all(driver)
        all_matches = get_matches()
    urls_dict['urls1'] = urls_principal ; urls_dict['urls2'] = urls_secondary
    urls_dict['names1'] = all_matches_names_principal ; urls_dict['names2'] = all_matches_names_secondary
    json.dump(urls_dict, f)
    return urls_dict
   
#Get cuotes and names of all the matches. Auxiliar functions.
def close_all(driver):
    opens = driver.find_elements_by_class_name('cm-CouponMarketGroupButton_Text')
    for op in opens: op.click() 
    return opens

def get_cuotes_and_names(driver, bet):
    while True:
        try:
            cuotes = driver.find_elements_by_class_name('gll-ParticipantOddsOnly_Odds')
            cuotes1 = cuotes
            cuotes = [c.text for c in cuotes]
            names = driver.find_elements_by_class_name('sl-CouponParticipantWithBookCloses_NameContainer')                
            names = [n.text for n in names]  
            if bet == 0:
                return cuotes, names 
            else:
                return cuotes1, names
        except selenium.common.exceptions.StaleElementReferenceException:
            continue
        except:
            traceback.print_exc(file=sys.stdout)
            continue            

#Get cuotes and names of all the matches.
def get_matches_cuotes_and_names(driver, importancia, bet):   
    try:
        if importancia == '1':
            lnames = []
            lcuotes = []
            opens = close_all(driver)
            opens.pop(0)
            for opi in list(range(len(opens))):
                opens[opi].click()
                cuotes, names = get_cuotes_and_names(driver, bet)
                lnames.append(names) ; lcuotes.append(cuotes)
                time.sleep(1.5)
                opens[opi].click()
            return lnames, lcuotes
            
        else:
            cuotes, names = get_cuotes_and_names(driver, bet)
            time.sleep(1.5)
            return names, cuotes
    except:
        traceback.print_exc(file=sys.stdout)
        pass