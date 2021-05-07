#!/usr/bin/python3


from time import sleep, strftime
from random import randint
import json 
import datetime
import tweepy, selenium

with open('twitter_cred.json', 'r') as outfile:
    keys = json.load(outfile)

with open('wallmart_cred.json', 'r') as outfile:
    walmar_cred = json.load(outfile)

auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
auth.set_access_token(keys["access_token"], keys["access_token_secret"])





def buy_from_wallmart():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as expected
    from selenium.webdriver.support.wait import WebDriverWait

    options = Options()
    options.add_argument("--headless")
    chromedriver_path = 'D:\Documents\BestBuyBot\chromedriver_win32\chromedriver.exe' # Change this to your own chromedriver path!
    webdriver = webdriver.Chrome(executable_path=chromedriver_path)
    wait = WebDriverWait(webdriver, timeout=10)
    webdriver.execute_script("document.body.style.zoom='80'")

    webdriver.get('https://www.walmart.ca/sign-in?from=%2Fen')
    username = wait.until(expected.visibility_of_element_located((By.ID, 'username')))
    #username = webdriver.find_element_by_id('username')
    username.send_keys(walmar_cred['email'])
    password = webdriver.find_element_by_id('password')
    password.send_keys(walmar_cred['pass'])

    button_login = webdriver.find_element_by_xpath("//button[contains(text(),'Sign in')]")
    button_login.click()
    sleep(2) 

    ps5_url = "https://www.walmart.ca/en/ip/playstation5-digital-edition/6000202198823"
    webdriver.get(ps5_url)
    sleep(2)



    add_button = webdriver.find_element_by_xpath("//button[contains(text(),'Add to cart')]")
    add_button.click()
    sleep(2) 
    cart_url = "https://www.walmart.ca/cart"
    webdriver.get(cart_url)

    checkout_button = webdriver.find_element_by_xpath("//button[contains(text(),'Proceed to checkout')]")
    checkout_button.click()
    sleep(2)

    try: 
        name = webdriver.find_element_by_id('firstName')
        name.send_keys('Angad')
        name = webdriver.find_element_by_id('lastName')
        name.send_keys('Singh')

        name = webdriver.find_element_by_id('pickupLocation')
        sleep(1)
        for _ in range(7): 
            name.send_keys(Keys.BACK_SPACE)
        name.send_keys("L7C1A8")
        find_button = webdriver.find_element_by_xpath("//button[contains(text(),'Find')]")
        find_button.click()
        sleep(1)
    except selenium.common.exceptions.NoSuchElementException: 
        print("Details already filed")

    order_button = webdriver.find_element_by_xpath("//button[contains(text(),'Place order')]")
    order_button.click()



if __name__ == "__main__":
    api = tweepy.API(auth)

    tweets = {} 
    while True: 
        for i in (313490867, 1116018402030759936):
            statuses = api.user_timeline(user_id=i)
            for s in statuses:
                if s.created_at not in tweets.keys(): 
                    print("{} : {}".format( s.created_at,  s.text))
                    tweets[s.created_at] = True
                if "#PS5" in s.text and "ONLINE ONLY" in s.text and s.created_at > datetime.datetime.strptime("2021-03-10", '%Y-%m-%d'): 
                    print("PS5 available for sale")  
                    buy_from_wallmart()
                    exit(0)
            sleep(5)