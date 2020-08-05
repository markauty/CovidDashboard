import pandas as pd
from io import StringIO
import requests
import datetime

datestr=datetime.datetime.now().strftime("%Y%m%d")
url = 'https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
req = requests.get(url)#, headers=headers)

data = StringIO(req.text)



df3=pd.read_csv(data)#'https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv')

maxdate=df3['Specimen date'].max()
#df3=df3.drop(df3[df3['Area type']!='Upper tier local authority'].index)
df3=df3.drop(df3[df3['Area type']!='utla'].index)
df3=df3.drop(df3[df3['Specimen date']!=maxdate].index)

df3.rename(columns={'Area name': 'GSS_NM', 'Area code':'GSS_CD','Cumulative lab-confirmed cases':'TotalCases'},inplace=True)
df3.drop (["Area type","Daily lab-confirmed cases", "Specimen date"], axis=1, inplace=True)
df3.sort_values(by='GSS_NM',ascending=True, inplace=True)

#df3.to_csv("mytable.csv", index=False)
df3.to_csv('/home/markaut/dailyreports/'+datestr+".csv", index=False)