import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
theurl='http://calendars.illinois.edu/week/7'
thepage=urllib.request.urlopen(theurl)
soup=BeautifulSoup(thepage,'html.parser')
links=soup.find_all('a',href=True)
eventlinks=[]
allevents={}
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
                    event['Type']=i
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
            allevents[title]=event
            print(title)
for i in allevents.items():
    print(i)
