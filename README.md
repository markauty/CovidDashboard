# CovidDashboard
Python Dashboard showing COVID charts for England. 

This is currently hosted at markaut.pythonanywhere.com

It is a small application that pulls daily UK covid infection totals for UK health areas from
https://www.arcgis.com/home/item.html?id=b684319181f94875a6879bbc833ca3a6#overview

Estimated population for each area is taken from 
https://www.ons.gov.uk/file?uri=%2fpeoplepopulationandcommunity%2fpopulationandmigration%2fpopulationprojections%2fdatasets%2flocalauthoritiesinenglandtable2%2f2016based/table2.xls

Charts report percentage infections for each area.

Downloader.py runs every day to pull the infections total data. Dash1_appa.py is the dash application which is served. The actual raw data is updated at around 5pm, however as it seemed to be variable during the early stages of the outbreak I decided to access it in the early hours, hence it lags the published data by about 10 hours....  ie, if you are in the UK, you are most likely to see the data that was published yesterday afternoon.


I am currently working on a Data Fellowship apprenticeship, hence the use of Pandas when I could probably have found a far more efficient way of getting the same effect. I do however use this code base for one or two other intersting things on my home system, so pandas isn't entirely going to waste.  While I don't object to anyone taking this code and using it for any purpose, it would be brilliant if you could drop me an email at markautysoftware@gmail.com, if nothing else, just to say hello. 
