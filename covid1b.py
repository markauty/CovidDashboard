
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd
import requests
import datetime
import time
import os





#generate incidence log
#incidencelog=pd.read_csv('incidencelog.csv')
#del incidencelog
#ranklog=pd.read_csv("AREAS.csv")
#proplog=pd.read_csv("AREAS.csv")
#incidencelog.drop(columns=['AGE GROUP'],inplace=True)
#incidencelog.head()

def download_population_Data():
    try:
        url='https://www.ons.gov.uk/file?uri=%2fpeoplepopulationandcommunity%2fpopulationandmigration%2fpopulationprojections%2fdatasets%2flocalauthoritiesinenglandtable2%2f2016based/table2.xls'
        print('Checking if population data exists')
        if os.path.isfile('PopulationData.xls')==False:
            print("...Need to download population data")
            header = {
              "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
              "X-Requested-With": "XMLHttpRequest"
            }
            print("......Downloading population data")
            r = requests.get(url, headers=header)
            print('......Writing file as PopulationData.xls')
            with open('PopulationData.xls', 'wb') as f:
                f.write(r.content)
        return 'PopulationData.xls'
    except:
        return 'Problem'


def Read_Population_Data(filename):
    #try:
    df = pd.read_excel(filename,sheet_name="Persons",skiprows=6)   #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #df = pd.read_excel('PopulationData.xls',sheet_name="Persons",skiprows=6)   #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    df.columns = df.columns.map(str)
    df2=df[['AREA','AGE GROUP','2020']]
    df2=df2[df2['AGE GROUP']=='All ages']
    df2['2020orig']=df2['2020'].astype(int)
    #print('Population of Health Authorities in England in 2020 df2')
    #print(df2.head())
    return df2
    #except:
    #    return 'Problem'

def Download_Latest_Cases_To_File(datestr):
    print('Importing latest COVID data')
    try:
        df3=pd.read_csv('https://www.arcgis.com/sharing/rest/content/items/b684319181f94875a6879bbc833ca3a6/data')
        #print("dailyreports\\"+datestr+".csv")
        df3.to_csv('dailyreports/'+datestr+".csv", index=False)
        return datestr+".csv"
    except:
        return 'Problem'

def Get_List_of_CSV_Files():
    file_list=[]
    for file in os.listdir("dailyreports"):
        if file.endswith(".csv"):
            file_list.append(file[:-4])
    file_list.sort()
    return file_list
        

#incidencelog=df2.copy()
#file_list=['20200320','20200321','20200322','20200323','20200324']

def Create_Incidence_Dataframes(incidencelog,file_list):
    try:
        incidencelog.drop(columns=["AGE GROUP"], inplace=True)
    except:
        pass
    incidencelog['2020']=incidencelog['2020orig']*1000

    #file_list=['20200320','20200321','20200322','20200323','20200324']
    
    #print(file_list)
    for files in file_list:
        datefile=pd.read_csv('dailyreports/'+files+".csv",thousands=',')
        datefile['TotalCases']=pd.to_numeric(datefile['TotalCases'])
        #convert filename string to date
        #filedate = datetime.datetime.strptime(files, '%Y%M%d')
        datefile.rename(columns={'TotalCases': files,'GSS_NM':'AREA'}, inplace=True)
        datefile.drop(columns=["GSS_CD"], inplace=True)

    
        incidencelog=incidencelog.merge(datefile,left_on='AREA', right_on='AREA')
        incidencelog['prop_'+files]=(incidencelog[files]/incidencelog['2020'])*100
        incidencelog['rank_'+files]=incidencelog['prop_'+files].rank(method='dense',ascending=False)

    incidencelog.sort_values(by='AREA', inplace=True)
    #incidencelog.reset_index(inplace=True)
    #proplog.sort_values(by='AREA', inplace=True)
    #proplog.reset_index(inplace=True)
    #ranklog.sort_values(by='AREA', inplace=True)
    #ranklog.reset_index(inplace=True)
    #proplog=incidencelog.copy()
    #ranklog=incidencelog.copy()
    print(incidencelog.head())
    #tidy up
    proplog_cols_to_keep=[]
    ranklog_cols_to_keep=[]
    incidencelog_cols_to_drop=[]
    for col in incidencelog.columns:
        if col=='AREA':
            proplog_cols_to_keep.append(col)
            ranklog_cols_to_keep.append(col)
        if col[0:5] in ("prop_"):
            proplog_cols_to_keep.append(col)
            incidencelog_cols_to_drop.append(col)
        
        elif col[0:5] in ("rank_"):
            ranklog_cols_to_keep.append(col)
            incidencelog_cols_to_drop.append(col)

    #print('proplog_cols_to_keep: ',proplog_cols_to_keep)
    proplog=incidencelog[proplog_cols_to_keep]
    ranklog=incidencelog[ranklog_cols_to_keep]
    #print(proplog.head())

    for col in ranklog.columns:
        if col !='AREA':
            #ranklog.rename(columns={col:col[5:]},inplace=True)
            #datetime.datetime.strptime(col[5:], '%Y%M%d')
            ranklog.rename(columns={col:datetime.datetime.strptime(col[5:], '%Y%m%d').date().strftime('%Y%m%d')},inplace=True)
    for col in proplog.columns:
        if col !='AREA':
            proplog.rename(columns={col:col[5:]},inplace=True)
            #proplog.rename(columns={col:datetime.datetime.strptime(col[5:], '%Y%m%d').date().strftime('%Y%m%d')},inplace=True)

    
    
    #tidy ranklog
    ranklog.set_index('AREA',inplace=True)
    ranklog=ranklog.T
    ranklog.reset_index(inplace=True)
    ranklog.rename(columns={"index":"Date"}, inplace=True)
    print(ranklog.head())
    ranklog['formatted_date']=pd.to_datetime(ranklog['Date'],format='%Y%m%d')
    print(ranklog.head())
    
    #proportion by date
    probydate=proplog.copy()
    probydate.set_index('AREA',inplace=True)
    probydate=probydate.T
    probydate.reset_index(inplace=True)
    probydate.rename(columns={"index":"Date"}, inplace=True)
    probydate['formatted_date']=pd.to_datetime(probydate['Date'],format='%Y%m%d')
    
    incidencelog.drop(columns=incidencelog_cols_to_drop,inplace=True)
    incidencelog.head()
    #print('probydate')
    #print(probydate.head(10))
    proplog.to_csv("proplog.csv")
    return incidencelog, proplog,ranklog,probydate
#del df


def Plot_Proportion_by_Area(df,date):
    df=df.copy()
    df.sort_values(by=date,ascending=False, inplace=True)
    try:
        df.reset_index(inplace=True)
    except:
        pass
    
    Wirral=df.index[df['AREA']=='Wirral']
    Liverpool=df.index[df['AREA']=='Liverpool']
    CheshireWest=df.index[df['AREA']=='Cheshire West and Chester']
    
    fig = plt.figure(figsize=(25,10))
    ax = fig.add_subplot(1, 1, 1)
    barplot=plt.bar(df["AREA"],df[date], width=.8, align='center')
    plt.xticks(rotation=90)
    plt.ylabel('Percentage infected', fontsize=10)
    plt.suptitle('Percentage Population with COVID-19', fontsize=15)
    barplot[Wirral[0]].set_color('red')
    barplot[CheshireWest[0]].set_color('Orange')
    barplot[Liverpool[0]].set_color('lime')
    ax.spines['left'].set_position(('data', -1))
    ax.spines['right'].set_position(('data', 146))
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.tight_layout()
    #ax.figure.savefig(datestr+".jpeg")  #needs to be png for server.  
    plt.show()
    
def Chart_Proportion_Over_Time(df,areas):
    ax=df.plot(x='Date',y=areas)
    ax.set_ylabel('Proportion of population (%)')
    ax.set_title('Change in Proportion over time')
    
def Chart_Rank_Over_Time(df,areas):
    #areas=list(pl)[1:]#
    #areas=['Wirral','Liverpool','Cheshire West and Chester']
    ymin=0
    for area in areas:
        if df[area].max()>ymin:
            ymin=df[area].max()

    fig = plt.figure()
    ax=df.plot('Date',areas)
    ax.set_ylim(ymin+10,0)
    ax.set_ylabel('Rank')
    ax.set_title('Change in Ranking over time')
    plt.show()
	
	
if __name__ == '__main__':	
    #set date
    datestr=datetime.datetime.now().strftime("%Y%m%d")
    #Download population data
    print(download_population_Data())
    #Read in the population data
    populationdata=Read_Population_Data('PopulationData.xls').copy()

    #download latest cases
    print(Download_Latest_Cases_To_File(datestr))

    csvfiles=Get_List_of_CSV_Files()

    incidencelog2, proplog2,ranklog2,propbydate2=Create_Incidence_Dataframes(populationdata,csvfiles)
    print('Done')


    #Plot_Proportion_by_Area(proplog2,'20200325')
    #Chart_Proportion_Over_Time(propbydate2,['Wirral','Liverpool','Cheshire West and Chester'])
    #Chart_Rank_Over_Time(ranklog2,['Wirral','Liverpool','Cheshire West and Chester'])
    #print(proplog2.head(10))
    #print(proplog2.columns)
            
