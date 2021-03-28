import requests, re, time, urllib, os, webbrowser, json, tempfile, shutil
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from natsort import natsorted
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips

def getTwitter(url, response, formato, firefox, decoded):
    temp_dir = tempfile.mkdtemp()
    if (response == 'Computador'):
        if (formato == '.jpg'):
            firefox.get(url)
            time.sleep(4)
            media = firefox.find_elements_by_css_selector('img.css-9pa8cd[alt="Image"]')
            n = 0
            for pbs in media:
                decoded.append(pbs.get_attribute("src"))
                n +=1
                size = len(decoded) - 1
                name = 'twitter' + '0' + str(size) + formato
            count = 0
            for i in range(100):
                if (os.path.isfile(os.getcwd() + '/' + 'twitter' + '0' + str(i) + '.jpg') == True):
                    count += 1
                    name = 'twitter' + '0' + str(count) + '.jpg'
                else:
                    break
            for i in range (n):
                name = 'twitter' + '0' + str(i + count) + '.jpg'
                urllib.request.urlretrieve(decoded[i + count], name)
            return True

        elif(formato == 'gif'):
            firefox.get(url)
            time.sleep(4)
            decoded.append(firefox.find_element_by_tag_name('video').get_attribute("src"))
            size = len(decoded) - 1
            name = 'twitter' + '0' + str(size) + ' .mp4'
            if (decoded[size] != ''):
                count = 0
                for i in range(100):
                     if (os.path.isfile(os.getcwd() + '/' + 'twitter' + '0' + str(i) + '.mp4') == True):
                        count += 1
                        name = 'twitter' + '0' + str(count) + '.mp4'
                     else:
                        break
                urllib.request.urlretrieve(decoded[size], name)
                return True

        elif(formato == '.mp4'):
            firefox.get(url)
            time.sleep(10)
            log = firefox.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")
            video =''
            with open(temp_dir + "/items.json", "w") as jsonFile:
                json.dump(log, jsonFile, indent = 6)
            jsonFile.close()
            with open (temp_dir + "/items.json", "r") as jsonFile:
                json_decoded = json.load(jsonFile)
                for i in range(len(json_decoded)):
                    if (re.match(r'https://video.twimg.com/', json_decoded[i]['name']) != None):
                        video = json_decoded[i]['name']
                        break
            jsonFile.close()
            if (re.search(r'https://video.twimg.com/(.*?).m3u8', video) != None):
                 m3u8c = re.search(r'https://video.twimg.com(.*?)?tag=', video)
                 encoded = []
                 if (m3u8c == None):
                    tipo='m4s'
                    urllib.request.urlretrieve(video, temp_dir + '/temp.txt')
                    with open (temp_dir + "/temp.txt", "r") as tempF:
                        for line in tempF:
                            if(re.search(r'.ts', line) != None):
                                encoded.append('https://video.twimg.com' + line)
                                tipo ='ts'
                    tempF.close()
                    directory = os.getcwd()
                    collection =[]
                    if(tipo == 'ts'):
                        for i in range(len(encoded)):
                            name = temp_dir + '/temp' + '0' + str(i) + '.ts'
                            urllib.request.urlretrieve(encoded[i], name)
                            video = VideoFileClip(name)
                            collection.append(video)
                            twitter = concatenate_videoclips(collection)
                            size = len(decoded)
                            final_name = 'twitter' + '0' + str(size) + '.mp4'
                        count = 0
                        for i in range(100):
                            if (os.path.isfile(directory + '/' + 'twitter' + '0' + str(i) + '.mp4') == True):
                                count += 1
                                final_name = 'twitter' + '0' + str(count) + '.mp4'
                            else:
                                break
                        twitter.to_videofile(final_name)
                        shutil.rmtree(temp_dir)
                        decoded.append('twittervideo')
                        return True
                    else:
                        shutil.rmtree(temp_dir)
                        return False

                 elif (m3u8c != None):
                    tipo='m4s'
                    urllib.request.urlretrieve(video, temp_dir + '/temp.txt')
                    with open (temp_dir + "/temp.txt", "r") as tempF:
                        for line in tempF:
                            if(re.search(r'.m3u8', line) != None):
                                m3u8c2 = 'https://video.twimg.com' + line
                                continue
                    tempF.close()
                    urllib.request.urlretrieve(m3u8c2, temp_dir + '/temp.txt')
                    with open (temp_dir + "/temp.txt", "r") as tempF:
                        for line in tempF:
                            if(re.search(r'.ts', line) != None):
                                encoded.append('https://video.twimg.com' + line)
                                tipo = 'ts'
                    tempF.close()
                    directory = os.getcwd()
                    collection =[]
                    if (tipo == 'ts'):
                        for i in range(len(encoded)):
                            name = temp_dir + '/temp' + '0' + str(i) + '.ts'
                            urllib.request.urlretrieve(encoded[i], name)
                            video = VideoFileClip(name)
                            collection.append(video)
                            twitter = concatenate_videoclips(collection)
                            size = len(decoded)
                            final_name = 'twitter' + '0' + str(size) + '.mp4'
                        count = 0
                        for i in range(100):
                            if (os.path.isfile(directory + '/' + 'twitter' + '0' + str(i) + '.mp4') == True):
                                 count += 1
                                 final_name = 'twitter' + '0' + str(count) + '.mp4'
                            else:
                                break
                        twitter.to_videofile(final_name)
                        shutil.rmtree(temp_dir)
                        decoded.append('twittervideo')
                        return True
                    else:
                        shutil.rmtree(temp_dir)
                        return False

                 else:
                    tipo='m4s'
                    encoded = []
                    with open (temp_dir + "/items.json", "r") as jsonFile:
                        json_decoded = json.load(jsonFile)
                        for i in range(len(json_decoded)):
                            if(re.search('"(.*?).ts', json_decoded[i]['name']) != None):
                                encoded.append(json_decoded[i]['name'])
                                tipo='ts'
                    jsonFile.close()
                    directory = os.getcwd()
                    collection =[]
                    if (tipo == 'ts'):
                        for i in range(len(encoded)):
                            name = temp_dir + '/temp' + '0' + str(i) + '.ts'
                            urllib.request.urlretrieve(encoded[i], name)
                            video = VideoFileClip(name)
                            collection.append(video)
                            twitter = concatenate_videoclips(collection)
                            size = len(decoded)
                            final_name = 'twitter' + '0' + str(size) + '.mp4'
                            count = 0
                        for i in range(100):
                            if (os.path.isfile(directory + '/' + 'twitter' + '0' + str(i) + '.mp4') == True):
                                count += 1
                                final_name = 'twitter' + '0' + str(count) + '.mp4'
                            else:
                                break
                        twitter.to_videofile(final_name)
                        shutil.rmtree(temp_dir)
                        decoded.append('twittervideo')
                        return True
                    else:
                        shutil.rmtree(temp_dir)
                        return False

    elif(response == 'Navegador'):
            if (formato == '.jpg'):
                firefox.get(url)
                time.sleep(5)
                decoded = firefox.find_element_by_css_selector('img.css-9pa8cd').get_attribute("src")
                if (decoded != ''):
                    webbrowser.open(decoded)
                    return True
            elif(formato == 'gif'):
                firefox.get(url)
                time.sleep(5)
                decoded = firefox.find_element_by_tag_name('video').get_attribute("src")
                if (decoded != ''):
                    webbrowser.open(decoded)
                    return True
                else:
                    firefox.quit()
                    return 0

    else:
        firefox.quit()
        return 0 