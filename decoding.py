import re
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from twitter import getTwitter
from instagram import instaPost, instaStories

firefox_options = Options()
firefox_options.add_argument("--headless")
firefox = webdriver.Firefox(options=firefox_options)

def getMedia(url, formato, response, media, button):
    decoded = []
    if (media.group(0) == 'https://www.instagram.com/p'):
        if (instaPost(url, response, formato, firefox, decoded, button) == True):
            return True
        else: 
            return False

    elif(media.group(0) == 'https://www.instagram.com/stories'):
        if (instaStories(url, response, formato, firefox, decoded, button) == True):
            return True
        else: 
            return False

    elif(media.group(0) == 'https://twitter.com/'):
        if (getTwitter(url, response, formato, firefox, decoded) == True):
            return True
        else: 
            return False

def killFirefox():
    firefox.quit()
