from flask import Flask,render_template,request,redirect,url_for
import json
import urllib.request
from datetime import datetime
from urllib.request import urlopen
import sqlite3
conn = sqlite3.connect('com.sqlite',check_same_thread=False)
c=conn.cursor()
app = Flask(__name__)
@app.route('/',methods=['GET', 'POST'])
async def test(): #informacja kanału
    testy=[]
    if request.method=='POST' and 'key_api' in request.form and 'channel_id' in request.form:
        id_channel=request.form['channel_id']
        key_api=request.form['key_api']
        data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id="+id_channel+"&part=snippet&key="+key_api).read()
        subs=json.loads(data)["items"][0]["statistics"]["subscriberCount"] #subkrycji
        chanelname=json.loads(data)["items"][0]["snippet"]["title"] #nazwa kanłu
        viewcount=json.loads(data)["items"][0]["statistics"]["viewCount"] #wyświelenia
        liczba_film=json.loads(data)["items"][0]["statistics"]["videoCount"] #ilośc filmów
        create_channel=json.loads(data)["items"][0]["snippet"]["publishedAt"] #utorzenie kanału
        customUrl=json.loads(data)["items"][0]["snippet"]["customUrl"] #customowy url
        imagechannel=json.loads(data)["items"][0]["snippet"]["thumbnails"]["medium"]["url"] #zdjęcie kanału
        subkrycji=int(subs)
        testy.append(chanelname)
        testy.append(subkrycji)
        testy.append(viewcount)
        testy.append(liczba_film)
        testy.append(datetime.strptime(create_channel,"%Y-%m-%dT%H:%M:%SZ"))
        testy.append(customUrl)
        testy.append(imagechannel)
    return render_template("test.html",testy=testy)
@app.route('/channel',methods=['GET', 'POST'])
async def channel(): #informacja filmu/live
    test=[]
    if request.method=='POST' and 'key_api' in request.form and 'id_film' in request.form:
        id_film=request.form['id_film']
        key_api=request.form['key_api']
        data_f=urllib.request.urlopen("https://www.googleapis.com/youtube/v3/videos?part=statistics&id="+id_film+"&part=snippet&key="+key_api).read()
        likecount=json.loads(data_f)["items"][0]["statistics"]["likeCount"] #łapki w górę
        title=json.loads(data_f)["items"][0]["snippet"]["title"] #nazwa filmu/live
        chnaelnamevideo=json.loads(data_f)["items"][0]["snippet"]["channelTitle"] #nazwa kanłu
        nazywo=json.loads(data_f)["items"][0]["snippet"]["liveBroadcastContent"] #czy jest na żywo
        publikacja=json.loads(data_f)["items"][0]["snippet"]["publishedAt"] #publikacja filmu/live
        test.append(chnaelnamevideo)
        test.append(title)
        kom=json.loads(data_f)["items"][0]["statistics"]
        if "viewCount" in kom:
            viewcount=json.loads(data_f)["items"][0]["statistics"]["viewCount"] #wyświelenia
            test.append(viewcount)
        else:
            m="Film widoczny dla wspierających"
            test.append(m)
        test.append(likecount)
        test.append(nazywo)
        test.append(datetime.strptime(publikacja,"%Y-%m-%dT%H:%M:%SZ"))
        minaturka=json.loads(data_f)["items"][0]["snippet"]["thumbnails"]["high"]["url"]#minaturka filmu
        if "commentCount" in kom:
            kom_count=json.loads(data_f)["items"][0]["statistics"]["commentCount"] #liczba komentarzy
            test.append(kom_count)
        else:
            m="Wyłączone komentarze"
            test.append(m)
        test.append(minaturka)
    return render_template("channel.html",test=test)
@app.route('/coments',methods=['GET', 'POST'])
async def coments(): #informacja filmu/live
    c.execute("SELECT * FROM com")
    s=c.fetchall()
    if request.method=='POST' and 'key_api' in request.form and 'id_film' in request.form and 'count' in request.form and 'odp' in request.form:
        id_film=request.form['id_film']
        key_api=request.form['key_api']
        count=request.form['count']
        odp=request.form['odp']
        data= data =urllib.request.urlopen("https://www.googleapis.com/youtube/v3/commentThreads?key="+key_api+"&textFormat=plainText&part=snippet&part=replies&videoId="+id_film+"&maxResults="+count).read()
        il=json.loads(data)["pageInfo"]["totalResults"]
        print(il)
        for ia in range(il):
            names=json.loads(data)["items"][ia]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]#nazwa kanału
            comt=json.loads(data)["items"][ia]["snippet"]["topLevelComment"]["snippet"]["textDisplay"]#treść
            published=json.loads(data)["items"][ia]["snippet"]["topLevelComment"]["snippet"]["publishedAt"]#publikacja
            p=datetime.strptime(published,"%Y-%m-%dT%H:%M:%SZ")
            x=json.loads(data)["items"][ia]["snippet"]["totalReplyCount"]#ilośc comments
            likes=json.loads(data)["items"][ia]['snippet']["topLevelComment"]["snippet"]["likeCount"]#polubnienia komentarzy
            if odp=="1":
                c.execute('INSERT INTO com VALUES(?,?,?,?)' ,(names,comt,p,likes))
            if odp=="2":
                c.execute("DELETE FROM com")
            c.connection.commit()
    return render_template("comments.html",s=s)

if __name__=="__main__":
    app.run(host="192.168.0.220") #wprowadz adres ip komputera
















