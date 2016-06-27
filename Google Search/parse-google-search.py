from bs4 import BeautifulSoup
from Orange.data import *

html = open("search-history.html", 'r', encoding='utf-8')
parsed_html = BeautifulSoup(html, "html.parser")

date = []
query = []
dates = []

for tag in parsed_html.find_all('tr'):
    temp = []
    for child in tag.children:
        temp.append(child.string)
    query.append(temp[0])
    date.append(temp[1])

domain = Domain([TimeVariable(date[0])], metas=[StringVariable(query[0])])

for datum in date:
    dates.append(datum.replace(u'T', ' ').replace(u'Z', ''))

var = TimeVariable()
data_table = Table(domain, list(zip((var.parse(i) for i in dates[1:]), query[1:])))
Table.save(data_table, "google-search.tab")
html.close()