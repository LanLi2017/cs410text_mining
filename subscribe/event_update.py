import urllib.request
from bs4 import BeautifulSoup
import csv
from collections import OrderedDict
import pandas as pd
import os
import pandas,sys
def events_update():
    theurl='http://calendars.illinois.edu/week/7'
    thepage=urllib.request.urlopen(theurl)
    soup=BeautifulSoup(thepage,'html.parser')
    # currenteventsoup=soup.find('div', id="ws-calendar-content")
    links=soup.find_all('a',href=True)
    eventlinks=[]
    allevents=[]
    for link in links:
        if 'eventId' in link['href']:
            url='http://calendars.illinois.edu'+link['href']
            if url not in eventlinks:
                event={}
                event['Url']=url
                print(url)
                eventlinks.append(url)
                eventpage = urllib.request.urlopen(url)
                eventsoup = BeautifulSoup(eventpage, 'html.parser')
                eventcontainersoup=eventsoup.find('div', class_="main-content-container")
                eventcontentsoup=eventcontainersoup.findAll(text=True)
                step=0
                typeflag=False
                dateflag=False
                locationflag=False
                for i in eventcontentsoup:
                    if step==0:
                        title=i
                        event['Title']=i
                        step+=1
                    if typeflag:
                        event['OldType']=i
                        typeflag=False
                    if i=='Event Type':
                        typeflag=True
                    if dateflag:
                        event['Date'] = i
                        dateflag=False
                    if i=='Date ':
                        dateflag=True
                    if locationflag:
                        event['Location'] = i
                        locationflag=False
                    if i=='Location':
                        locationflag=True
                eventdescriptionsoup=eventsoup.find('dd', class_="ws-description")
                if eventdescriptionsoup==None:
                    event['Description'] = ''
                else:
                    event['Description'] = eventdescriptionsoup.text
                ##add new tag
                event['NewType'] = ''
                allevents.append(event)

    #
    #
    #
    # ##convert the latest parsed events into new csv file
    #
    keys = allevents[0].keys()
    with open('temporary.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(allevents)
    #
    # #merge the latest events with the all the events( put the data into database)
    # # combine two csvs into new one and delete initial two.
    events = pd.read_csv('events.csv')
    temporary = pd.read_csv('temporary.csv')
    out = events.append(temporary)
    out = out.drop_duplicates(subset='Title', keep="last")
    os.remove('events.csv')
    os.remove('temporary.csv')
    with open('events.csv', 'w', encoding='utf-8') as f:
        out.to_csv(f, index=False)

    #read csv to list of dictionary
    reader = csv.DictReader(open('events.csv'))
    result = []
    for row in reader:
        new_row = dict(row)
        result.append(new_row)
    new_dict = {}
    for item in result:
       Title = item['Title']
       new_dict[Title] = item


    from sklearn.feature_extraction.text import TfidfVectorizer
    import operator
    def KNN(allevents,k):
        destype = []
        for eventname in allevents.keys():
            destype.append((allevents[eventname]['Description'], allevents[eventname]['OldType'],eventname))
        doclst = []
        for type in destype:
            doclst.append(type[0])
        vect = TfidfVectorizer(min_df=1)

        tfidf = vect.fit_transform(doclst)
        simmatrix = (tfidf * tfidf.T).A
        for i in range(len(simmatrix)):
            K=simmatrix[i]
            nearest = sorted(range(len(K)), key=lambda x: K[x])[-k-1:-1]
            nearest=list(reversed(nearest))
            nearesttypes={}
            for j in nearest:
                if destype[j][1] not in nearesttypes.keys():
                    nearesttypes[destype[j][1]]=K[j]
                else:
                    nearesttypes[destype[j][1]] += K[j]
            if allevents[destype[i][2]]['OldType'] not in nearesttypes.keys():
                nearesttypes[allevents[destype[i][2]]['OldType']]=0.5
            else:
                nearesttypes[allevents[destype[i][2]]['OldType']]+=0.5
            typedecided=max(nearesttypes.items(), key=operator.itemgetter(1))[0]
            allevents[destype[i][2]]['NewType']=typedecided
        return allevents

    update_events = KNN(new_dict,6)

    update_events = list(update_events.values())

    #store the data after csv
    os.remove('events.csv')
    keys = update_events[0].keys()
    with open('events.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(update_events)
    print('update_finish!')

