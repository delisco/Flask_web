import leveldb
import requests
import pandas as pd
from bs4 import BeautifulSoup
from gtts import gTTS

# converting functions
def cvt_to_bytes(string):
    # leave type check for system exceptions
    return string.encode('utf-8')


def cvt_to_string(bytestring):
    # leave type check for system exceptions
    return bytestring.decode('utf-8')


def cvt_b(key, value):
    key_b = key
    value_b = value
    if isinstance(key, type('str')):
        key_b = cvt_to_bytes(key)
    if isinstance(value, type('str')):
        value_b = cvt_to_bytes(value)
    return key_b, value_b


def cvt_s(key, value):
    key_s = key
    value_s = value
    if isinstance(key, (type(b'bytes'), type(bytearray(b'bytes')))):
        key_s = cvt_to_string(key)
    if isinstance(value, (type(b'bytes'), type(bytearray(b'bytes')))):
        value_s = cvt_to_string(value)
    return key_s, value_s


# database functions
def init(filename):
    db = leveldb.LevelDB(filename)
    return db


def insert(db, key, value):
    key_b, name_b = cvt_b(key, value)
    db.Put(key_b, name_b)


def delete(db, key):
    key_b = cvt_to_bytes(key)
    db.Delete(key_b)


def update(db, key, value):
    key_b, name_b = cvt_b(key, value)
    db.Put(key_b, name_b)


def search(db, key):
    key_b = cvt_to_bytes(key)
    value = db.Get(key_b)
    value_str = cvt_to_string(value)
    return value_str


def dump(db):
    for key, value in db.RangeIter():
        key_s, value_s = cvt_s(key, value)
        print (key_s, value_s)

def load_news(db):
    tnl_news = ""
    for key, value in db.RangeIter():
        key_s, value_s = cvt_s(key, value)
        tnl_news = tnl_news + key_s + '-' +value_s + '/'
    return tnl_news

def get_hypenews(url):
    resp = requests.get(url) 
    soup = BeautifulSoup(resp.text, 'html.parser')
    titles = soup.find_all('div','post-box-content-title')
    #print(titles)
    title_list = [] # 先建立
    for title in titles:
        #print(title.h2.text)
        title_list.append(title.h2.text)

    time_list = []    
    times = soup.find_all('span','time')
    for time in times:
        #print(time.text)
        time_list.append(time.text)
    
    
    link_list = []    
    links = soup.find_all('div','post-box-content-title') 
    #print(links)
    for link in links:
    #print(link.a.get('href'))
    #print(link.get('href'))
        link_list.append(link.a.get('href'))


    con_list = []
    for i in range(len(link_list)):
        resp_1 = requests.get(link_list[i])
        soup_1 = BeautifulSoup(resp_1.text, 'html.parser')
        con = soup_1.find_all('article','post-body-content')
        for c in con:
        #print(c.p.text)
            con_list.append(c.p.text)
        
        
    id_list = []
    for i in range(len(title_list)):
        id_list.append(i) 

    pic_list = []    
    pics = soup.find_all('div','post-box-image-container')
    for pic in pics:
    #print(pic.img.get('src'))
        link_list.append(pic.img.get('src'))
    

    hype_list = [id_list, title_list, time_list, link_list, con_list, pic_list]
    df = pd.DataFrame(hype_list)
    df = pd.DataFrame.transpose(df)
    return hype_list
    #print(df.head())


def translate_text_to_speech(text):
    if text is not None:
        tts=gTTS(text, lang='zh')
        print(text)
        tts.save("hypebeast.mp3") 

    