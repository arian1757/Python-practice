from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import requests

Brand=input('give me brand:')
Model=input('give me the model:')
driver=webdriver.Chrome()

driver.get('https://www.truecar.com/used-cars-for-sale/')


select_brand= Select(driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/main/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div/div[2]/div[1]/form/div[1]/div/div[1]/label/div[2]/select'))
select_brand.select_by_visible_text(Brand)

sleep(2)
select_model=Select(driver.find_element(By.XPATH, '//*[@id="tabs--2--panel--0"]/form/div[1]/div/div[2]/label/div[2]/select'))
select_model.select_by_visible_text(Model)

driver.find_element(By.XPATH, '//*[@id="tabs--2--panel--0"]/form/div[2]/button').click()

sleep(2)
currentUrl= driver.current_url
r=requests.get(currentUrl)

soup=BeautifulSoup(r.text,'html.parser')

links=[]

val=soup.find_all('a', attrs={'class':"linkable order-2 vehicle-card-overlay"})

    
for i in range (20):
    links.append(val[i].get('href'))
        

sleep(5)
n=0
for adv in links:
    n+=1
    r_adv=requests.get('https://www.truecar.com%s' % (adv))

    soup=BeautifulSoup(r_adv.text,'html.parser')
    value_price=soup.find('div',attrs={'data-test':"vdpPreProspectPrice"})
    value_price=value_price.text
    value_mile=soup.find('p',attrs={'class':"margin-top-1"})
    value_mile=value_mile.text
    print('number %d, its price is %s and its Mileage is %s' % (n,value_price,value_mile))
    













