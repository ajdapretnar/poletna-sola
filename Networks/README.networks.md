
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


# Examples for GOT
Vnesi št. ali ime uporabnika/vozlišča (-1 za izhod): Melisandre
Do 5 najprimernejsih priporocil/povezav:
	1. Olenna (napovedana ocena: 1.215)
	2. Nan (napovedana ocena: 1.212)
	3. Brienne (napovedana ocena: 1.153)
	4. Aerys (napovedana ocena: 1.142)
	5. Joffrey (napovedana ocena: 1.112)

Vnesi št. ali ime uporabnika/vozlišča (-1 za izhod): Walder
Do 5 najprimernejsih priporocil/povezav:
	1. Olenna (napovedana ocena: 1.294)
	2. Joffrey (napovedana ocena: 1.235)
	3. Margaery (napovedana ocena: 1.187)
	4. Petyr (napovedana ocena: 1.150)
	5. Aerys (napovedana ocena: 1.137)

Vnesi št. ali ime uporabnika/vozlišča (-1 za izhod): Tommen
Do 5 najprimernejsih priporocil/povezav:
	1. Aerys (napovedana ocena: 1.340)
	2. Joffrey (napovedana ocena: 1.321)
	3. Olenna (napovedana ocena: 1.309)
	4. Tommen (napovedana ocena: 1.288)
	5. Brienne (napovedana ocena: 1.235)


# Examples for EURO
Cabaye-Giroud-Pogba
Mangala-Sagna
Rashford-Sturridge
Vermaelen-Alderweireld
Brady-Ward
Keane-Chester
