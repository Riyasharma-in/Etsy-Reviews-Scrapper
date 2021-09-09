# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 10:24:53 2021

@author: Ria
"""

import pickle
import time
from time import sleep
import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import os

start_time = time.time()
person = []
date = []
stars = []
review = []
sentiment = []
#defining export_data funtion to export the data in variables
def export_data():
    if 'scrappedReviews.csv' in os.listdir(os.getcwd()):
        df1 = pd.read_csv('scrappedReviews.csv')
        '''Exporting data'''
        
        
        
        for i in range(0,len(df1["Person"])):
            if df1["Person"][i] not in person:
                person.append(df1["Person"][i])
                date.append(df1["Date"][i])
                stars.append(df1["Stars"][i])
                review.append(df1["Reviews"][i])
                sentiment.append(df1["Sentiment"][i])
        
        dataframe1 = pd.DataFrame()
        dataframe1["Person"] = person
        dataframe1["Date"] = date
        dataframe1["Stars"] = stars
        dataframe1["Reviews"] = review
        dataframe1["Sentiment"] = sentiment
        
        result = pd.concat([df1,dataframe1])
        result.to_csv('scrappedReviews.csv',index=False)
    else:
        '''Exporting data'''
        dataframe1 = pd.DataFrame()
        dataframe1["Person"] = person
        dataframe1["Date"] = date
        dataframe1["Stars"] = stars
        dataframe1["Reviews"] = review
        dataframe1["Sentiment"] = sentiment
        dataframe1.to_csv('scrappedReviews.csv',index=False)

#defining function for Checking the sentiment of any review
def check_review(reviewtext):
    '''
    Check the review is positive or negative'''
    file = open("pickle_model.pkl", 'rb')
    pickle_model = pickle.load(file)
    file = open("feature.pkl", 'rb')
    vocab = pickle.load(file)
    #reviewText has to be vectorised, that vectorizer is not saved yet
    #load the vectorize and call transform and then pass that to model preidctor
    #load it later
    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    vectorised_review = transformer.fit_transform(loaded_vec.fit_transform([reviewtext]))
    # Add code to test the sentiment of using both the model
    # 0 == negative   1 == positive
    out = pickle_model.predict(vectorised_review)
    return out[0]

def run_scraper(page):
    global person,review
    print("Starting Chrome:")
    global step
    step = pd.DataFrame()
    
    browser = webdriver.Chrome(ChromeDriverManager().install())

    URL ='https://www.etsy.com/in-en/c/jewelry-and-accessories?ref=pagination&page={}'
    
    try:
        #Count for every page of website
        
            
        URL = URL.format(page)
        browser.get(URL)
        
        print("Scraping Page:",page)
        #xpath of product table
        PATH_1 = '/html/body/div[5]/div/div[1]/div/div[4]/div[2]/div[2]/div[3]/div/div/ul'
        #getting total items
        items = browser.find_element_by_xpath(PATH_1)
        items = items.find_elements_by_tag_name('li')
        #available items in page
        end_product = len(items)
        #Count for every product of the page
        for product in range(0,end_product):
            
            print("     Scarping reviews for product",product+1)
            #clicking on product
            try:
                items[product].find_element_by_tag_name('a').click()
            except:
                print('Product link not found')
                
            
            #switch the focus of driver to new tab
            windows = browser.window_handles
            browser.switch_to.window(windows[1])
            
                
            
            try:
                PATH_2 = '//*[@id="same-listing-reviews-panel"]/div'
                count = browser.find_element_by_xpath(PATH_2)
                #Number of review on any page
                count = count.find_elements_by_class_name('wt-grid__item-xs-12')
                for r1 in range(1,len(count)+1):
                    dat1 = browser.find_element_by_xpath(
                                '//*[@id="same-listing-reviews-panel"]/div/div[{}]/div[1]/div[2]/p[1]'.format(
                                    r1)).text
                    if dat1[:dat1.find(',')-6] not in person:
                        try:
                            person.append(dat1[:dat1.find(',')-6])
                            date.append(dat1[dat1.find(',')-6:])
                        except Exception:
                            person.append("Not Found")
                            date.append("Not Found")
                        try:
                            stars.append(browser.find_element_by_xpath(
                                '//*[@id="same-listing-reviews-panel"]/div/div[{}]/div[2]/div/div/div[1]/span/span[1]'.format(
                                    r1)).text[0])
                        except Exception:
                            stars.append("No stars")
                        try:
                            review.append(browser.find_element_by_xpath(
                                '//*[@id="review-preview-toggle-{}"]'.format(r1-1)).text)
                            sentiment.append(check_review(browser.find_element_by_xpath(
                                '//*[@id="review-preview-toggle-{}"]'.format(r1-1)).text))
                        except Exception:
                            review.append("No Review")
                            sentiment.append(check_review("No Review"))
            except Exception:
                try:
                    count = browser.find_element_by_xpath('//*[@id="reviews"]/div[2]/div[2]')
                    count = count.find_elements_by_class_name('wt-grid__item-xs-12')
                    
                    for r2 in range(1,len(count)+1):
                        dat1 = browser.find_element_by_xpath(
                                    '//*[@id="reviews"]/div[2]/div[2]/div[{}]/div[1]/p'.format(r2)).text
                        if dat1[:dat1.find(',')-6] not in person:
                            try:
                                
                                person.append(dat1[:dat1.find(',')-6])
                                date.append(dat1[dat1.find(',')-6:])
                            except Exception:
                                person.append("Not Found")
                                date.append("Not Found")
                            try:
                                stars.append(browser.find_element_by_xpath(
                                    '//*[@id="reviews"]/div[2]/div[2]/div[{}]/div[2]/div[1]/div[1]/div[1]/span/span[1]'.format(
                                        r2)).text[0])
                            except Exception:
                                stars.append("No Stars")
                            try:
                                review.append(browser.find_element_by_xpath(
                                    '//*[@id="review-preview-toggle-{}"]'.format(
                                        r2-1)).text)
                                sentiment.append(check_review(
                                    browser.find_element_by_xpath(
                                    '//*[@id="review-preview-toggle-{}"]'.format(
                                        r2-1)).text))
                            except Exception:
                                review.append("No Review")
                                sentiment.append(check_review(
                                    "No Review"))                                        
                except Exception:
                    try:
                        count = browser.find_element_by_xpath('//*[@id="reviews"]/div[2]/div[2]')
                        count = count.find_elements_by_class_name('wt-grid__item-xs-12')
                        
                        for r3 in range(1,len(count)+1):
                            dat1 = browser.find_element_by_xpath(
                                        '//*[@id="same-listing-reviews-panel"]/div/div[{}]/div[1]/p'.format(r3)).text
                            if dat1[:dat1.find(',')-6] not in person:
                                try:
                                    person.append(dat1[:dat1.find(',')-6])
                                    date.append(dat1[dat1.find(',')-6:])
                                except Exception:
                                    person.append("Not Found")
                                    date.append("Not Found")
                                try:
                                    stars.append(browser.find_element_by_xpath(
                                        '//*[@id="same-listing-reviews-panel"]/div/div[{}]/div[2]/div[1]/div[1]/div[1]/span/span[1]'.format(r3)).text[0])
                                except Exception:
                                    stars.append("No Stars")
                                try:
                                    review.append(browser.find_element_by_xpath(
                                        '//*[@id="review-preview-toggle-{}"]'.format(r3-1)).text)
                                    sentiment.append(check_review(browser.find_element_by_xpath(
                                        '//*[@id="review-preview-toggle-{}"]'.format(r3-1)).text))
                                except Exception:
                                    review.append("No Review")
                                    sentiment.append(check_review("No Review"))
                    except Exception:
                        print("Error")
                        continue
                
            browser.close()
            #swtiching focus to main tab
            browser.switch_to.window(windows[0])
            #export data after every product
            #export_data()
        
        
    except Exception as e_1:
        print(e_1)
        print("Program stoped:")
    export_data()
    browser.quit()
    
    
    
#defining the main function
def main():
    logging.basicConfig(filename='solution_etsy.log', level=logging.INFO)
    logging.info('Started')
    if 'page.txt' in os.listdir(os.getcwd()):
        with open('page.txt','r') as file1:
            page = int(file1.read())
        for i in range(page,251):
            run_scraper(i)
    else:
        for i in range(1,251):
            with open('page.txt','w') as file:
                file.write(str(i))
            run_scraper(i)
    
    export_data()
    print("--- %s seconds ---" % (time.time() - start_time))
    logging.info('Finished')
# Calling the main function 
if __name__ == '__main__':
    main()


