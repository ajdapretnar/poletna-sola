from bs4 import BeautifulSoup
from Orange.data import *
from datetime import datetime

html = open("html//timeline.htm", 'r', encoding='utf-8')
parsed_html = BeautifulSoup(html, "html.parser")


def string_to_datetime(s):
    date, time = s.split(" at ")
    date = date.split()
    day = date[2].strip(",")
    if len(day) < 2:
        day = "0" + day
    month = date[1]
    year = date[3]
    date = "{}-{}-{}".format(year, month, day)
    time = time.split()[0]
    final = datetime.strptime((date + " " + time), "%Y-%B-%d %I:%M%p").strftime("%Y-%m-%d %H:%m")
    return final


def to_data_table(f):
    rules = {"(.*) and (.*) are now friends\.": ("friends", 1), "(.*) went to (.*)\.": ("event", 1),
             "(.*) is going to (.*)\.": ("event", 1), "(.*) is interested in (.*)\.": ("event", 1),
             "(.*) likes (.*)\.": ("pages", 1), "(.*) played (.*)\.": ("games", 1),
             "(.*) earned an achievement in (.*)\.": ("games", 1), "(.*) added (.*) new photos\. (.*)": ("photos", ""),
             "(.*) added a new photo to the album\: ([^.]*)": ("photos", 1), "(.*) updated (.*)\.": ("update", ""),
             "(.*) was added to (.*) by (.*)\.": ("added", 1), "(.*) added (.*) to the movies (.*) watched\.": ("movies", 1),
             "(.*) added (.*) to TV shows (.*) watched\.(.*)": ("TV shows", 1), "(.*) reviewed (.*) \— ": ("review", 1),
             "(.*) shared a link\.": ("share", ""), "(.*) shared a photo to your Timeline\.": ("share", 0),
             "(.*) feeling ([^.]*)": ("feeling", 1), "(.*) shared a video to your Timeline\.": ("share", 0)}
    domain = Domain([TimeVariable("timestamp"),
                     DiscreteVariable("tags", values=(["comment"] + [i for i, j in set(rules.values())]))],
                    metas=[StringVariable("content"), StringVariable("objects")])

    date = []
    content = []
    tags = []
    objects = []

    for tag in f.find_all('p'):
        temp_comment = []
        for child in tag.children:
            temp_comment.append(child.string)
        if temp_comment:
            if len(temp_comment) == 1:
                date.append(string_to_datetime(temp_comment[0]))
                content.append("")
            elif temp_comment[1] is not None:
                date.append(string_to_datetime(temp_comment[0]))
                content.append(" ".join(temp_comment[1:]))
            else:
                continue

    for comm in content:
        if comm:
            comment = comm.strip("[").strip("]").replace("\\n", " ")
            for regex, category in rules.items():
                if re.match(regex, comment):
                    tag, index = category
                    tags.append(tag)
                    if index:
                        objects.append(re.match(regex, comment).groups()[int(index)])
                    else:
                        objects.append(index)
                    break
            else:
                tags.append("comment")
                objects.append("")
        else:
            tags.append("")
            objects.append("")
    var = TimeVariable()
    data_table = Table(domain, list(zip((var.parse(i) for i in date), tags, content, objects)))
    return data_table

data = to_data_table(parsed_html)
Table.save(data, "facebook.tab")
html.close()
