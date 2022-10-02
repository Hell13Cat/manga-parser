from itertools import count
from colorama import Fore, Back, Style
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import PIL
import requests
import time
import pickle
import os
import ctypes

def make_folder(folder):
    if not os.path.isdir(os.getcwd()+"\\"+folder):
        os.mkdir(os.getcwd()+"\\"+folder)

def make_file(file):
    if not os.path.isfile(os.getcwd()+"\\"+file):
        open(os.getcwd()+"\\"+file, "w")

def pprint(text, colors):
    dict_color = {"g": Back.GREEN, "y": Back.YELLOW, "r": Back.RED, "b": Back.BLUE}
    print(dict_color[colors] + str(text) + Style.RESET_ALL)

def pprintr(text, colors):
    dict_color = {"g": Back.GREEN, "y": Back.YELLOW, "r": Back.RED, "b": Back.BLUE}
    return dict_color[colors] + str(text) + Style.RESET_ALL

def get_name(num, source_name):
    ext_name = source_name.split(".")[-1]
    return ((3-len(str(num))) * "0") + str(num) + "." + ext_name

url_root = {
    "hentailib.me":{"img":"https://img.yaoi-chan.me/", "root":"https://hentailib.me"},
    "yaoilib.me":{"img":"https://img.yaoi-chan.me/", "root":"https://yaoilib.me/"},
    "mangalib.me":{"img":"https://img.yaoi-chan.me/", "root":"https://mangalib.me"}
}
exe_drive = os.getcwd()+"\\chromedriver\\chromedriver.exe"
make_folder("dw")
make_folder("cookies")
make_folder("chromedriver")
make_folder("cfg")
make_file("cfg\\list_load.txt")
make_file("cfg\\list_url.txt")
if not os.path.isfile(os.getcwd()+"\\chromedriver\\chromedriver.exe"):
    pprint("[ERROR] chromedriver not found! Please download for you Chrome version from https://chromedriver.storage.googleapis.com/index.html", "r")
    exit()
driver = webdriver.Chrome(executable_path=exe_drive)
driver.set_window_position(0, 0)
user32 = ctypes.windll.user32
screensize = [user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)]
driver.set_window_size(screensize[0], screensize[1])
ddd = input(pprintr("URL or Enter> ", "y"))
if ddd == "":
    url_gets = open("cfg/list_url.txt", "r").readlines()
    urls_gets = []
    for kk in url_gets:
        urls_gets.append(kk.replace("\n", ""))
else:
    urls_gets = [ddd]
for url_get in urls_gets:
    url_load = open("cfg/list_load.txt", "r").readlines()
    urls_load = []
    for kk in url_load:
        urls_load.append(kk.replace("\n", ""))
    if url_get not in url_load:
        dw_folder_root = os.getcwd() + "\dw\(" + url_get.split("//")[1].split("/")[0] + ") " + url_get.split("/")[-1].split("?")[0]
        pprint(dw_folder_root, "g")
        if not os.path.isdir(dw_folder_root):
            os.mkdir(dw_folder_root)
        url_domain = url_get.split("//")[1].split("/")[0]
        driver.get(url_get)
        pprint(url_domain, "g")
        if url_domain not in url_root.keys():
            pprint("Not support....", "r")
            exit()
        if os.path.isfile("cookies\\" + url_domain+".pkl"):
            cookies = pickle.load(open("cookies\\" + url_domain+".pkl", "rb"))
            pprint(cookies, "b")
            for cookie in cookies:
                driver.add_cookie(cookie)
        else:
            url_go = url_root[url_domain]["root"]
            driver.get(url_go)
            ddd = input(pprintr("Wait login....", "y"))
            cookies = driver.get_cookies()
            pickle.dump(cookies, open("cookies\\" + url_domain+".pkl","wb"))
            pprint(cookies, "b")
        driver.get(url_get)
        driver.save_screenshot("dw\(" + url_get.split("//")[1].split("/")[0] + ") " + url_get.split("/")[-1].split("?")[0] + ".png")
        if url_domain == "hentailib.me" or url_domain == "yaoilib.me" or url_domain == "mangalib.me":
            action_chains = ActionChains(driver)
            all_button = driver.find_elements_by_tag_name("li")
            manga_id = url_get.split("/")[-1].split("?")[0]
            pprint(manga_id, "g")
            for oo in all_button:
                try:
                    if "chapters" in str(oo.get_attribute("data-key")):
                        oo.click()
                except:
                    pass
            pages_np = driver.find_elements_by_tag_name("a")
            pages = []
            for ii in pages_np:
                if manga_id in str(ii.get_attribute("href")):
                    if "/v" in str(ii.get_attribute("href")):
                        pages.append(str(ii.get_attribute("href")).split("?")[0])
            pages = list(dict.fromkeys(pages))
            pprint(pages, "b")
            for page_cur in pages:
                driver.get(page_cur)
                name_ch = page_cur.split("/")[-2].replace("v", "") + "-" + page_cur.split("/")[-1].replace("c", "")
                dw_folder = dw_folder_root + "\\" + name_ch
                if not os.path.isdir(dw_folder):
                    os.mkdir(dw_folder)
                pprint(dw_folder, "g")
                all_button = driver.find_elements_by_tag_name("button")
                for oo in all_button:
                    try:
                        if "Мне есть 18 лет" in str(oo.text):
                            oo.click()
                    except:
                        pass
                all_button = driver.find_elements_by_tag_name("i")
                for oo in all_button:
                    try:
                        if "fa-cog" in str(oo.get_attribute("class")):
                            oo.click()
                    except:
                        pass
                all_button = driver.find_elements_by_tag_name("label")
                for oo in all_button:
                    try:
                        if "Вертикальный" in str(oo.text):
                            oo.click()
                    except:
                        pass
                all_button = driver.find_elements_by_tag_name("div")
                for oo in all_button:
                    try:
                        if "modal__close" in str(oo.get_attribute("class")):
                            oo.click()
                    except:
                        pass
                continue_scroll = 1
                all_button = driver.find_elements_by_tag_name("select")
                for oo in all_button:
                    try:
                        if "reader-pages" in str(oo.get_attribute("id")):
                            all_frame_base = oo
                    except:
                        pass
                all_frame = all_frame_base.find_elements_by_tag_name("option")
                for oo in all_frame:
                    oo.click()
                    time.sleep(0.1)
                list_img = []
                all_img = driver.find_elements_by_tag_name("img")
                for oo in all_img:
                    try:
                        if manga_id in str(oo.get_attribute("src")):
                            list_img.append(oo.get_attribute("src"))
                            action_chains.send_keys_to_element(oo, Keys.CONTROL, "c")
                    except:
                        pass
                cookie_req = {}
                for dd in cookies:
                    cookie_req[dd["name"]] = dd["value"]
                count_img = 1
                for img_url in list_img:
                    file_name_head = get_name(count_img, img_url.split("/")[-1])
                    pprint("[Downloading] "+file_name_head, "g")
                    req = requests.get(img_url, cookies=cookie_req, headers={'referer': page_cur})
                    file_name = dw_folder + "/" + file_name_head
                    file = open(file_name, "wb")
                    file.write(req.content)
                    file.close()
                    count_img += 1
            pprint("[READY]", "g")
        else:
            pprint("URL not support", "r")
    urls_load_w = "\n".join(urls_load) + "\n" + url_get
    open("cfg/list_load.txt", "w").write(urls_load_w)