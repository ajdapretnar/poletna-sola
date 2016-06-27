import csv
import time

with open("Kaj nam lahko povedo družabna omrežja.csv", 'r') as fr:
    with open("Kaj nam lahko povedo družabna omrežja2.csv", 'w') as wr:
        reader = csv.reader(fr)
        writer = csv.writer(wr)

        all = []

        for i, row in enumerate(reader):
            if i == 0:
                all.append(row)
            else:
                date = row[0].split(' ')
                if len(date[1]) < 8:
                    date = "{}-{}-{} ".format(*(date[0].split('/'))) + '0' + date[1]
                else:
                    date = "{}-{}-{} ".format(*(date[0].split('/'))) + date[1]
                all.append([date] + row[1:])

        writer.writerows(all)
