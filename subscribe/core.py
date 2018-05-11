from django.core.mail import send_mail
import pandas as pd
import subprocess
import re
from datetime import datetime
from event_update import events_update
from django.conf import settings
settings.configure()

def isCurrent(enddate):
    a = re.findall(r'\w{3}\s+[0-9][0-9]?,\s+[0-9]{4}', enddate)
    endtime = a[-1]
    d = datetime.strptime(endtime, '%b %d, %Y')
    now = datetime.now()
    return d>now

def task():
    events_update()
    events = pd.read_csv('events.csv')
    # render different tag html
    tag_html = {'Exhibition': '<li>Exhibition<ul>', 'Informational': '<li>Inforamtional<ul>',
                'Festival/Celebration': '<li>Festival/Celebration<ul>',
                'Social/Informal Event': '<li>Social/Informal Event<ul>', 'Performance': '<li>Performance<ul>',
                'Seminar/Symposium': '<li>Seminar/Symposium<ul>', 'Lecture': '<li>Lecture<ul>',
                'Meeting': '<li>Meeting<ul>', 'Health/Fitness': '<li>Health/Fitness<ul>',
                'Conference/Workshop': '<li>Conference/Workshop<ul>', 'Ceremony/Service': '<li>Ceremony/Service<ul>',
                'Reception/Open House': '<li>Reception/Open House<ul>', 'Other': '<li>Other<ul>'}
    for index, row in events.iterrows():
        title = row['Title']
        url = row['Url']
        # Filter the future events only
        if type(row['Date']) is not float:
            if (isCurrent(row['Date'])):
                html_line = '<li><a href="' + url + '">' + title + "</a></li>"
                tag_html[row['NewType']] += html_line
    for key in tag_html:
        tag_html[key] += '</ul></li>'

    # extract subscription data
    subprocess.call('python ../manage.py dump_subscribe -o subscribe.csv', shell=True)
    # send events email to user
    subs = pd.read_csv('subscribe.csv')
    for index, row in subs.iterrows():
        email = row['email']
        nickname = row['nickname']
        tags = row['subscribed_tags']
        if type(tags) is float:
            continue
        tags = tags.split()
        html_content = '<html><body><h4>Coming Events</h4><ul>'
        for tag in tags:
            html_content += tag_html[tag]
        html_content += '</ul></body></html>'
        send_mail('Hi, '+nickname, 'Hi, '+nickname, 'helper@subscription.com', [email, ],html_message = html_content)
