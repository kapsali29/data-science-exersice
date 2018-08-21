from bs4 import BeautifulSoup
import requests
from collections import Counter
import matplotlib.pyplot as plt
import datetime
import plotly
from IPython.display import Image
from dateutil.parser import parse

url1 = requests.get("https://www.adslgr.com/forum/threads/6588-Seti-home-Greece-United")
url2 = requests.get("https://www.adslgr.com/forum/threads/6588-Seti-home-Greece-United/page2")
soup = BeautifulSoup(url1.text, "lxml")

user_names = []
for link in soup.find_all("a", {"class": "username offline popupctrl"}):
    user_names.append(link.strong.text)

user_post = []
for link in soup.find_all("div", {"class": "postrow"}):
    user_post.append(link.text)

urls_per_post = []
for link in soup.find_all('blockquote', {"class": "username_container"}):
    if link.a == None:
        urls_per_post.append([])
    else:
        temp = []
        for item in link.find_all("a"):
            temp.append(item['href'])
        urls_per_post.append(temp)

soup2 = BeautifulSoup(url2.text, "lxml")

for link in soup2.find_all("a", {"class": "username offline popupctrl"}):
    user_names.append(link.strong.text)

for link in soup2.find_all("div", {"class": "postrow"}):
    user_post.append(link.text)

for link in soup2.find_all("span", {"class": "date"}):
    posted_date_time.append(link.text.replace('\xa0', ' '))

for link in soup2.find_all('blockquote', {"class": "postcontent restore"}):
    if link.a == None:
        urls_per_post.append([])
    else:
        temp = []
        for item in link.find_all("a"):
            temp.append(item['href'])
        urls_per_post.append(temp)

dates = [k[0:k.find(',')] for k in posted_date_time]
count_dates = Counter(dates)
dates = list(count_dates.keys())
dates = [parse(x).strftime('%d/%m/%Y') for x in dates]
dates = sorted(dates, key=lambda x: datetime.datetime.strptime(x, '%d/%m/%Y'),reverse=False)

##Diagram 1
plt.bar(range(len(count_dates)), count_dates.values(), align="center")
plt.xticks(range(len(count_dates)), dates,rotation='vertical')
plt.suptitle('Number of posts per date', fontsize=12)
plt.style.use('ggplot')
plt.ylabel('Number of posts')
plt.ylim((0,12))
plt.show()

## Diagram 2
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)
number_of_posts_per_user = Counter(user_names)
data = [go.Bar(
    y=list(number_of_posts_per_user.keys()),
    x=list(number_of_posts_per_user.values()),
    orientation='h'
)]
layout = go.Layout(
    title='Number of posts per user',
    xaxis=dict(
        title='Number of posts',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(

        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
iplot(go.Figure(data=data, layout=layout))

## Diagram 3
out_degree = Counter(number_of_posts_per_user.values())
plt.bar(range(len(out_degree)), out_degree.values(), align="center")
plt.xticks(range(len(out_degree)), list(out_degree.keys()))
plt.suptitle('Forum members with the same number of posts', fontsize=12)
plt.xlabel('Number of posts')
plt.ylabel('Number of forum members')
plt.style.use('ggplot')
plt.ylim((0,10))
plt.show()