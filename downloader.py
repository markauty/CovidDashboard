#downloader
import datetime
import time
import covid1a as cov

datestr=datetime.datetime.now().strftime("%Y%m%d")
finished=False
#while finished==False:
#    print("trying to download")
#    downloaded=cov.Download_Latest_Cases_To_File(datestr)
#    if downloaded!="Problem":
#        print("Success")
#        finished=True
#    else:
#        print("failed")
#        time.sleep(10)
#print(cov.Download_Latest_Cases_To_File('goose'))

for n in range(0,20):
    print("try", n)
    downloaded=cov.Download_Latest_Cases_To_File(datestr)
    if downloaded!="Problem":
        print("Success")
        break
    else:
        print("failed")
        time.sleep(30)