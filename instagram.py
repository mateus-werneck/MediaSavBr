import requests, re, time, urllib, os, webbrowser, json, tempfile, shutil, pickle
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By


def instaPost(url, response, formato, firefox, decoded, button):
    if (auth(firefox, button) == True):   
        firefox.get(url)
        time.sleep(1)
        html = firefox.page_source
        time.sleep(1)
        encodedImg = re.search(r'"display_url":"(.*?)",', html)
        encodedVideo = re.search(r'"video_url":"(.*?)",', html)
        if (encodedImg == None and encodedVideo == None):
            return False
        else:
            if (encodedVideo == None):
                decoded.append(encodedImg.group(1).replace(r"\u0026", "&"))
            else:
                decoded.append(encodedVideo.group(1).replace(r"\u0026", "&"))
            for url in decoded:
                if (url != ''):
                    size = len(decoded) - 1
                    if (response == 'Computador'):
                        if (formato == '.jpg'):
                            name = 'instagram' + '0' + str(size) + formato
                            count = 0
                            for i in range(100):
                                if (os.path.isfile(os.getcwd() + '/' + 'instagram' + '0' + str(i) + '.jpg') == True):
                                    count += 1
                                    name = 'instagram' + '0' + str(count) + '.jpg'
                                else:
                                    break
                            urllib.request.urlretrieve(decoded[size], name)
                            return True
                        elif(formato == '.mp4'):
                            name = 'instagram' + '0' + str(size) + formato
                            count = 0
                            for i in range(100):
                                if (os.path.isfile(os.getcwd() + '/' + 'instagram' + '0' + str(i) + '.mp4') == True):
                                    count += 1
                                    name = 'instagram' + '0' + str(count) + '.mp4'
                                else:
                                    break
                            urllib.request.urlretrieve(decoded[size], name)
                            return True
                    elif(response == 'Navegador'):
                        webbrowser.open(url)
                        return True

                    else:
                        return False
                else:
                    return False

def instaStories(url, response, formato, firefox, decoded, button):
    if (auth(firefox, button) == True):
        firefox.get(url)   
        time.sleep(2)
        view = firefox.find_element_by_class_name('sqdOP.L3NKy.y1rQx.cB_4K')
        view.click()
        if (response == 'Computador'):
            if (formato == '.jpg'):
                decoded.append(firefox.find_element_by_tag_name("img").get_attribute("src"))
                size = len(decoded) - 1
                name = 'instagram' + '0' + str(size) + formato
                count = 0
                for i in range(100):
                    if (os.path.isfile(os.getcwd() + '/' + 'instagram' + '0' + str(i) + '.jpg') == True):
                        count += 1
                        name = 'instagram' + '0' + str(count) + '.jpg'
                    else:
                        break
                urllib.request.urlretrieve(decoded[size], name)
                return True
            elif(formato == '.mp4'):
                decoded.append(firefox.find_element_by_tag_name('source').get_attribute("src"))
                size = len(decoded) - 1
                name = 'instagram' + '0' + str(size) + formato
                count = 0   
                for i in range(100):
                    if (os.path.isfile(os.getcwd() + '/' + 'instagram' + '0' + str(i) + '.mp4') == True):
                        count += 1
                        name = 'instagram' + '0' + str(count) + '.mp4'
                    else:
                        break
                urllib.request.urlretrieve(decoded[size], name)
                return True

        elif(response == 'Navegador'):
            if (formato == '.jpg'):
                file = firefox.find_element_by_tag_name("img").get_attribute("src")
                return True
            elif(formato == '.mp4'):
                file = firefox.find_element_by_tag_name('source').get_attribute("src")
                webbrowser.open(file)
                return True
            else:
                return False        

       
def auth(firefox, button):
    if (button == 0):
        username = 'pythonauthusr1234'
        password = 'instagramauthpass123'
        firefox.get("https://www.instagram.com/accounts/login/")
        time.sleep(1)
        usern = firefox.find_element_by_name("username")
        usern.send_keys(username)
        passw = firefox.find_element_by_name("password")
        passw.send_keys(password)
        time.sleep(1)
        log_cl = firefox.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
        log_cl.click()
        time.sleep(4)
        title = firefox.title
        if (title == "Login • Instagram"):
            time.sleep(1)
            username = 'pythonauthusr12345'
            usern = firefox.find_element_by_name("username")
            usern.send_keys(username)
            passw = firefox.find_element_by_name("password")
            passw.send_keys(password)
            time.sleep(1)
            log_cl = firefox.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
            log_cl.click()
            time.sleep(4)
            title = firefox.title
            if (title == "Login • Instagram"):
                time.sleep(1)
                username = 'pythonauthusr123456'
                usern = firefox.find_element_by_name("username")
                usern.send_keys(username)
                passw = firefox.find_element_by_name("password")
                passw.send_keys(password)
                time.sleep(1)
                log_cl = firefox.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
                log_cl.click()
                time.sleep(4)
                title = firefox.title
                if (title == "Login • Instagram"):
                    firefox.quit()
                    return False
            else:
                return True

        else:
            return True
    elif(button > 0):
        return True               