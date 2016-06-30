
# Static networks

### Networks of Swords

Analyzed GoT data based on parsing the sentences of a book (Available at: https://www.macalester.edu/~abeverid/thrones.html).

Input: stormofswords.csv
    1. Generate a .net file (stormofswords.net)

        $ python csv2net stormofswords.csv

    2. Generate a .tab file with augmented data (stormofswords.data.csv)

        $ python net2data.csv stormofswords.csv

    3. Load into Orange.


# Twitter Live feed data

## GoT

Building networks from mentions in Live Twitter feeds for popular hastags like #GoT or #EURO2016.

Input: A file with entity names (stormofswords.net) stored as network keys.

    1. Run a Twitter query and store tweets on disk (twitter_got_2016-06-20_2016-06-27_dump.tab)

    2. Generate a live network from tweets.
        (twitter_got_2016-06-20_2016-06-27_dump.net,
         twitter_got_2016-06-20_2016-06-27_dump.data.csv)

        $ python twitter_net.py

    3. Load into Orange.


## EURO 2016

    Get teams data from https://github.com/jokecamp/FootballData

## Ideje za sprotno delo
https://sl.wikipedia.org/wiki/Seznam_poslancev_7._dr%C5%BEavnega_zbora_Republike_Slovenije #slovenija #politika
http://www.wimbledon.com/en_GB/players/ #Wimbledon2016
http://www.gpupdate.net/en/f1-line-up/234/2016-formula-1-teams/ #F1
...
