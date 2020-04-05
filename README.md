# CovidDashboard
Python Dashboard showing COVID charts for England. 

This is currently hosted at markaut.pythonanywhere.com

It is a small application that pulls daily UK covid infection totals for UK health areas from
https://www.arcgis.com/home/item.html?id=b684319181f94875a6879bbc833ca3a6#overview

Estimated population for each area is taken from 
https://www.ons.gov.uk/file?uri=%2fpeoplepopulationandcommunity%2fpopulationandmigration%2fpopulationprojections%2fdatasets%2flocalauthoritiesinenglandtable2%2f2016based/table2.xls

Charts report percentage infections for each area.

Downloader.py runs every day to pull the infections total data. Dash1_appa.py is the dash application which is served.
