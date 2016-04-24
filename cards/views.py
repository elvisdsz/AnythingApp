from django.shortcuts import render
import twitter,textrazor,json,requests

from operator import itemgetter

# Create your views here.

textrazor.api_key = "API_KEY"

def index(request):
    location = {'latitude':request.POST.get("latitude",""),'longitude':request.POST.get("longitude","")}
    #context = {'location':location}

    lat = request.POST.get("latitude","13.3605")
    lon = request.POST.get("longitude","74.7864")

    radius_km = 100
    max_tweet_count = 15
    
    tweets = get_tweets(lat,lon,radius_km,max_tweet_count)
    #context = {'tweets':tweets}

    entities = []
    filtered_tweets = []
    for tweet in tweets:
        try:
            ent = get_entities(tweet.text)
            entities.append(ent)
            ft = {}
            if len(entities[-1])>0:
                ft['text'] = tweet.text
                ft['entities'] = entities[-1]
                ft['score'] = get_score(tweet.text)
                filtered_tweets.append(ft)
        except:
            pass
        #filtered_tweets.append({'text':'I love python.','entities':get_entities('I love python.'),'score':get_score('I love python.')})

    ents = []
    for x in entities:
        for y in x:
            if y['id'] == "Twitter" or y['id'] in [ents[z]['id'] for z in range(len(ents))]:
                continue
            ents.append(y)
    ents = sorted(ents, key=itemgetter('id'), reverse=True)
    #ents.sort()

    return render(request,'cards/index.html', {'tweets':filtered_tweets,'location':location,'len':len(tweets),'entities':ents})#context)


def get_tweets(lat,lon,radius=50,max_tweet_count=10):
    api = twitter.Api(consumer_key = "xxx",consumer_secret = "yyy", access_token_key ="zzz",access_token_secret = "fff")
    return api.GetSearch(geocode=(lat,lon,str(radius)+'km'),result_type='recent',count=max_tweet_count)


def get_entities(text):
    client = textrazor.TextRazor(extractors=["entities", "topics"])
    response = client.analyze(text)
    ret = []
    for entity in response.entities():
        if(int(entity.relevance_score)+int(entity.confidence_score)>0.5):
            ret.append({'id':entity.id, 'relevance_score':entity.relevance_score, 'confidence_score':entity.confidence_score, 'freebase_types':entity.freebase_types})
    return ret
    #entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types

def get_score(text):
    r = requests.post("https://api.havenondemand.com/1/api/sync/analyzesentiment/v1",data={'apikey':'7a592092-216a-4c1c-82f7-cad6bd5a9337','text':text})
    d = json.loads((r.content).decode('utf-8'))
    try:
        score = d['aggregate']['score']
    except:
        score = 0
    return score
