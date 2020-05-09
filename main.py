from newsapi import NewsApiClient
from flask import Flask, jsonify, request
import static, json
from datetime import date, datetime, timedelta


app = Flask(__name__)

newsapi = NewsApiClient(api_key='e2d1833fb29542a6a14d8b6ac39c832a')

# /v2/top-headlines
def top_headlines(info):
    return newsapi.get_top_headlines(q='',sources=info,language='en',page_size=30)

top_headline_top = newsapi.get_top_headlines(q='',sources='bbc-news,the-verge',language='en')

# /v2/everything
prev = date.today().replace(day=1) - timedelta(days=1)
all_articles = newsapi.get_everything(q='',sources='bbc-news',from_param=prev,to= datetime.date(datetime.now()),language='en',page_size=100,page=1)

# /v2/sources
sources = newsapi.get_sources()


def data_filter(data):
    i = len(data["articles"]) - 1
    while i > -1:
        if (not data["articles"][i]["author"] or not data["articles"][i]["description"] or not data["articles"][i]["title"] or
        not data["articles"][i]["url"] or not data["articles"][i]["urlToImage"] or not data["articles"][i]["publishedAt"] 
        or not data["articles"][i]["source"]["id"] or not data["articles"][i]["source"]["name"] or len(data["articles"][i]["author"]) == 0
        or len(data["articles"][i]["description"])==0 or len(data["articles"][i]["title"])==0 or
        len(data["articles"][i]["url"]) == 0 or len(data["articles"][i]["urlToImage"])==0 or len(data["articles"][i]["publishedAt"])==0 
        or len(data["articles"][i]["source"]["id"])==0 or len(data["articles"][i]["source"]["name"])==0 or
        data["articles"][i]["author"]=='null' or data["articles"][i]["description"]=='null' or data["articles"][i]["title"]=='null' or
        data["articles"][i]["url"]=='null' or data["articles"][i]["urlToImage"]=='null' or data["articles"][i]["publishedAt"]=='null' 
        or data["articles"][i]["source"]["id"]=='null' or data["articles"][i]["source"]["name"]=='null'):
            del(data["articles"][i]) 
        i -= 1
    return data

#filter word for D3 
def filter_out_stop_word():
    f = open("stopwords_en.txt", "r")
    All_line = f.readlines()
    blacklist = {}
    for line in All_line:
        temp = line.strip('\n')
        temp = line.split('\t')
        temp = line.strip('\n')
        blacklist[temp] = 1
    
    CNN = top_headlines('cnn')
    FOX = top_headlines("fox-news")
    top = newsapi.get_top_headlines(q='',sources='',language='en',page_size=30)
    ret = {}
    
    for i in range(len(top["articles"])):
        temp = top["articles"][i]["title"].split()
        for word in temp:
            if word not in blacklist:
                ret[word] = 1 if word not in ret else ret[word] + 1

    # for i in range(len(CNN["articles"])):
    #     temp = CNN["articles"][i]["title"].split()
    #     for word in temp:
    #         if word not in blacklist:
    #             ret[word] = 1 if word not in ret else ret[word] + 1
    # for i in range(len(FOX["articles"])):
    #     temp = FOX["articles"][i]["title"].split()
    #     for word in temp:
    #         if word not in blacklist:
    #             ret[word] = 1 if word not in ret else ret[word] + 1
    #find first 30 highest frequency words
    for k , v in ret.items():
        ret[k] = str(v)

    ret_sorted = sorted(ret.items(),key=lambda x:x[1],reverse=True)    #for int
    result = []
    
    for i in range(30):
        if int(ret_sorted[i][1]) > 6:
            result.append([ret_sorted[i][0],6])
        else:
            result.append(ret_sorted[i])
    return result

@app.route('/', methods=['POST','GET'])
def send_home():     
    return app.send_static_file('index.html')


@app.route('/test', methods=['POST','GET'])
def get_news():
    front_data = request.get_data().decode("utf-8")
    if front_data == "cnn":
      
        ret = json.dumps(data_filter(top_headlines('cnn')))
        return ret
        
    if front_data == "fox-news":
        ret = json.dumps(data_filter(top_headlines("fox-news")))
        
        return ret
    
    if front_data == "top_headlines":
        data_filter(top_headline_top)
        return json.dumps(top_headline_top)
    #this get_source for intial
    if front_data == "get_source":
        return json.dumps(sources)
    
    if front_data == "word_cloud":
        return json.dumps(filter_out_stop_word())


@app.route('/search', methods = ['POST','GET'])
def find_searching():
    front_data = request.get_data().decode("utf-8")
    
    front_data = front_data.split(',')

    keyword = front_data[0]
    date_s = front_data[1]
    date_e = front_data[2]
    sour = front_data[3]
    if sour == 'all':
        sour = ''
    #return newsapi.get_everything(q=keyword, sources=sour, from_param=date_s, to=date_e, language='en', sort_by='publishedAt', page_size=100)
    ret = data_filter(newsapi.get_everything(q=keyword, sources=sour, from_param=date_s, to=date_e, language='en', sort_by='publishedAt', page_size=100))
    return json.dumps(ret)

@app.route('/api/getsource/<category>',methods=['GET'])
def get_source(category):
    
    front_data = category.lower()
    print(front_data)
    if front_data == "all":
        return json.dumps(sources)
    else:
        return json.dumps(newsapi.get_sources(category=front_data))

if __name__ == '__main__':
    #app.run(debug=True)
    app.run()



