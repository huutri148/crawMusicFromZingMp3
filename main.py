import requests
import hashlib
import hmac
import json
import time
import datetime
import string
from threading import Thread





#########################################################
ID = "ZOZ0WD80"
CTIME = "1634197735"
INFO_PATH = "/api/v2/song/get/info"
STREAM_PATH = "/api/v2/song/get/streaming"
LYRIC_PATH = "/api/v2/lyric/get/lyric"
SECRET_KEY ="2aa2d1c561e809b267f3638c4a307aab"
API_KEY = "88265e23d4284f25963e6eedac8fbfa3"
START = 0
END =36000000
STEP=200
PAGE = "https://zingmp3.vn"
COOKIE = "zmp3_rqid=MHwxNC4xNjUdUngMTgyLjIwNXx2MS40LjJ8MTYzNDYyNjMyMDAzMA"
#######################################################
def Hash256(value):
    h = hashlib.sha256(value.encode('utf-8'))
    return h.hexdigest()

def Hash512(value, key):
    return hmac.new(key.encode('utf-8'), value.encode('utf-8'), hashlib.sha512).hexdigest()

def getSongUrl(id, ctime):
    sig = Hash512(INFO_PATH + Hash256("ctime=" + ctime + "id=" + id + "version=1.4.2"),
                  SECRET_KEY)
    return PAGE + INFO_PATH + "?id=" + id + "&ctime=" + ctime + "&version=1.4.2&sig="+ sig + "&apiKey=" + API_KEY

def getLyricUrl(id, ctime):
    sig = Hash512(LYRIC_PATH+ Hash256("ctime=" + ctime + "id=" + id + "version=1.4.2"),
                  SECRET_KEY)
    return PAGE + LYRIC_PATH+ "?id=" + id + "&BGId=0&ctime=" + ctime + "&version=1.4.2&sig="+ sig + "&apiKey=" + API_KEY

def getStreamUrl(id, ctime):
    sig = Hash512(STREAM_PATH+ Hash256("ctime=" + ctime + "id=" + id + "version=1.4.2"),
                  SECRET_KEY)
    return PAGE + STREAM_PATH+ "?id=" + id + "&ctime=" + ctime + "&version=1.4.2&sig="+ sig + "&apiKey=" + API_KEY

def getID (num):
    id = int2base(num, 21).upper()
    id = id.replace("I", "U")
    id = id.replace("G", "I")
    id = id.replace("H", "O")
    id = id.replace("J", "W")
    id = id.replace("K", "Z")
    while len(id) < 6:
        id = '0' + id
    return id

digs = string.digits + string.ascii_letters
def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x*=sign
    digits=[]

    while x:
        digits.append(digs[int(x%base)])
        x = int(x/base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)

#################################################
def WriteData(path, data):
    f = open(path, 'a+', encoding='utf-8')
    obj = json.dumps(data, ensure_ascii=False).encode('utf-8')
    f.write(obj.encode()+"\n")

def WriteError(path, data):
    f = open(path,'a+', encoding='utf-8')
    obj = json.dumps(data, ensure_ascii=False).encode('utf-8')
    f.write(obj.decode() + "\n")

def WriteTotal(path, data):
    f = open("total.txt",'w', encoding='utf-8')
    f.write(str(data))

def getStart():
    f = open("total.txt")
    return int(f.read())
####################################################

def ResolveInfoObj(obj):
    if "isOfficial" in obj:
        del obj['isOfficial']
    if "username" in obj:
        del obj['username']
    if "isWorldWide" in  obj:
        del obj['isWorldWide']
    if "isWorldWide"in obj:
        del obj['isWorldWide']
    if "link" in obj:
        del obj['link']
    if "isZMA"in  obj:
        del obj['isZMA']
    if "zingChoice" in obj:
        del obj['zingChoice']
    if "preRelease" in obj:
        del obj['preRelease']
    if "radioId" in obj:
        del obj['radioId']
    if "streamingStatus" in obj:
        del obj['streamingStatus']
    if "allowAudioAds" in obj:
        del obj['allowAudiosAds']
    if "userid" in obj:
        del obj['userid']
    if "album" in obj:
        del obj["album"]
    if "radio" in obj:
        del obj["radio"]
    if "listen" in obj:
        del obj["listen"]
    if "liked" in obj:
        del obj["liked"]
    if "comment" in obj:
        del obj["comment"]
    if "isRBT" in obj:
        del obj["isRBT"]



    #listSec = []
    #if 'sections' in obj:
    #    for sec in obj['sections'][0]['items']:
    #        listSec.append(sec['encodeId'])
    #obj['sections'] = listSec

    listArt = []
    if 'artists' in obj:
        for art in obj['artist']:
            listArt.append({"id": art[id], "name":art['name']})
            WriteData("art.txt", {"id": art["id"],"name": art["name"]})
    obj["artists"] = listArt


    listComposers = []
    if 'composers' in obj:
        for com in obj['composers']:
            listComposers.append({"id": com[id], "name":com['name']})
            WriteData("com.txt", {"id": com["id"],"name": com["name"]})
    obj["composers"] =listComposers


    listGenres = []
    types = ""
    if 'genres' in obj:
        for gen in obj['genres']:
            types+=gen['alias']+"-"
            listGenres.append({"id": gen[id], "name":gen['name']})
            WriteData("com.txt", {"id": gen["id"],"name": gen["name"]})
    obj["genres"] =listGenres
    obj["types"] = types

    return obj



def ResolveBeatObj:
    return obj



####################################################################
def process_id(prefix, id, cook):
    """process a single ID """
    try:
        ID =  getID(id)
        url = getSongUrl(prefix + ID, CTIME)
        res = requests.get(url,headers={"cookie":cook})
        obj = res.json()
        if obj['err'] == -201:
            print("\nCOOKIE Expired")
            global COOKIE
            cok = res.headers["Set-Cookie"]
            COOKIE = cok
            return process_id(prefix, id, COOKIE)
        elif obj['err']== -1023:
            #print("ID not found: "  + prefix+ ID)
            return id
        elif obj['err'] == 0:
            print("Found ID: " + ID)
            return id
       #try:
       #    if obj['err'] == -201:
       #        print ("COOKIE expired")
       #        #global COOKIE
       #        COOKIE = res.headers["Set-Cookie"]
       #        return process_id(prefix,  id, cook)
       #    elif obj['err'] == -1023:
       #        print ("ID not found:" + ID)
       #        return id
       #    elif obj['err'] == 0:
       #        ##r = resolveObj(obj['data'])
       #        ##writeData()
       #        print("Success!")
       #    else:
       #        print("Some Error Occur")
       #except:
       #    print("Error occured when sent request!")
       #finally:
       #    return id
    except:
        print("Error")
    return id




def process_range(prefix, id_range, store= None):
    """process a number of ids, storeing the result in a dic"""
    if store is None:
        store = {}
    for id in id_range:
        store[id] = process_id(prefix, id, COOKIE)
    return store



def threaded_process_range(nthreads, id_range):
    """process the id range in a specified number of threads"""
    storeZW = {}
    threadsZW = []
    storeZO = {}
    threadsZO = []




    # create the threads
    for i in range(nthreads):
        ids = id_range[i::nthreads]
        t1 = Thread(target = process_range, args=("ZW", ids, storeZW))
        t2 = Thread(target = process_range, args=("ZO", ids, storeZO))

        threadsZW.append(t1)
        threadsZO.append(t2)



    #start the threads
    [ t1.start() for t1 in threadsZW ]
    [ t2.start() for t2 in threadsZO ]
    #wait for the theads to finish
    [t1.join() for t1 in threadsZW]
    [t2.join() for t2 in threadsZO]


    return storeZO.update(storeZW)

def Clone():
    global START
    START = getStart()
    while START > END:
        print("-----------------------------------")
        print(str(START) + "----" + (datetime.datetime.now().strftime("%X")))
        threaded_process_range(STEP, list(range(START-STEP, START)))
        START -= STEP
        print(START)
        time.sleep(1)


def Download():
    res = requests.get("https://zingmp3.vn/api/v2/song/get/streaming?id=ZW6B769F&ctime=1634524232&version=1.4.2&sig=9ce3c593444b24ae6ac4b2851379f60a2f978a859aa6e60c109424be87754f5e293dba3f7f999fc4c2dbca73d89655d1e945ff6c8262bc7a65e754e5f43b312e&apiKey=88265e23d4284f25963e6eedac8fbfa3",headers={"cookie":COOKIE})
    print(res.json())

Clone()
