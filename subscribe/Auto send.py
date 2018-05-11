import pandas as pd
import subprocess
import re
from datetime import datetime

# from django.conf import settings

# find corresponding events of different tag
# load events.csv to dataframe
def isCurrent(enddate):
    a = re.findall(r'\w{3}\s+[0-9][0-9]?,\s+[0-9]{4}', enddate)
    endtime = a[-1]
    d = datetime.strptime(endtime, '%b %d, %Y')
    now = datetime.now()
    return d>now


events = pd.read_csv('events.csv')
#render different tag html
events = events.drop_duplicates(subset='Title',keep="last")

tag_html = {'Exhibition':'<li>Exhibition<ul>', 'Informational':'<li>Inforamtional<ul>', 'Festival/Celebration':'<li>Festival/Celebration<ul>', 'Social/Informal Event':'<li>Social/Informal Event<ul>', 'Performance':'<li>Performance<ul>', 'Seminar/Symposium':'<li>Seminar/Symposium<ul>', 'Lecture':'<li>Lecture<ul>', 'Meeting':'<li>Meeting<ul>', 'Health/Fitness':'<li>Health/Fitness<ul>','Conference/Workshop':'<li>Conference/Workshop<ul>','Ceremony/Service':'<li>Ceremony/Service<ul>','Reception/Open House':'<li>Reception/Open House<ul>','Other':'<li>Other<ul>'}
for index,row in events.iterrows():
    title = row['Title']
    url = row['Url']
    #Filter the future events only
    if type(row['Date']) is not float:
        if(isCurrent(row['Date'])):
            html_line = '<li><a href="'+url+'">'+title+"</a></li>"
            tag_html[row['OldType']]+=html_line
for key in tag_html:
    tag_html[key] += '</ul></li>'

#extract subscription data
subprocess.call('python ../manage.py dump_subscribe -o subscribe.csv',shell=True)
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
        html_content+= tag_html[tag]
html_content +='</ul></body></html>'
    #email
print(html_content)
    # subject, from_email, to = 'Coming Events!', 'helper@eventsubscription.com', email
    #
    # # html_content = render_to_string('mail_template.html', {'varname':'value'}) render with dynamic value
    # text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.
    #
    # # create the email, and attach the HTML version as well.
    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()





