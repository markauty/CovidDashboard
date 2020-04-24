#import time
import datetime
from bs4 import BeautifulSoup
import pandas as pd
#import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.firefox.options import Options as FirefoxOptions

#from pyvirtualdisplay import Display


URL = 'https://coronavirus.data.gov.uk/#local-authorities'
datestr=datetime.datetime.now().strftime("%Y%m%d")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

#print("selenium version", selenium.__version__)

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get(URL)

    #wait for the page to load completely
    wait = WebDriverWait(driver, 50)
    element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[6]/div/div[3]")))

finally:
    page = driver.page_source
    #print(driver.get_log("browser"))
    #driver.get_screenshot_as_file("/home/markaut/screenshot2.png")
    driver.quit()
#print(page)
#print('Selenium bit is completed')


#Use BeautifulSoup to extract the incidents table
soup = BeautifulSoup(page, 'html.parser')
results = soup.find(id='local-authorities')

#parse into a list of list
output_rows = []
for table_row in results.findAll('tr'):
    columns = table_row.findAll('td')
    output_row = []
    for column in columns:
        output_row.append(column.text)
    output_rows.append(output_row)

#Throw it into pandas to tidy it up and make same format as the original version
df = pd.DataFrame(output_rows)

#Make the same format as the original code
df.rename(columns={0: 'GSS_NM',1:'TotalCases'}, inplace=True)
df['GSS_CD']="Ignore"
df = df[['GSS_CD', 'GSS_NM','TotalCases',]]                      #reorganise as it is inconsistent otherwise
df = df.iloc[1:]

df.to_csv('dailyreports/'+datestr+".csv", index=False)
#df.to_csv(datestr+".csv", index=False)
