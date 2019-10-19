import os
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException , WebDriverException
from time import sleep,ctime
import multiprocessing
import time

df = pd.read_csv('top-1m.csv' , names=['rank','website'])

print(time.ctime())

rank_df = df.iloc[600:650]
#print(rank_df)
def open_website(url):
    #print(url)
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(20)
    try :
        driver.get(url)
        sleep(2)
        driver.close()
    except TimeoutException as ex1:
        print("Exception has been thrown. " + str(ex1))
        driver.close()
    except WebDriverException as ex2:
        print("Exception has been thrown. " + str(ex2))
        driver.close()

def capture_packet(sh_command) :
    #print(sh_command)
    os.system(sh_command)

count = 601
for domain in rank_df['website'] :
    url = 'http://www.'+domain
    print("rank = "+str(count)+ url)
    file_name = 'rank'+str(count)+'.pcap'
    count= count+1
    sh_command = 'sudo timeout 20 tcpdump -i wlo1 -w '+file_name+' port 53'

    #print(url)
    #print(sh_command)
    #capture_packet(sh_command)

    t1 = multiprocessing.Process(target=open_website, args=(url,))
    t2 = multiprocessing.Process(target=capture_packet, args=(sh_command,))
    
    
    t2.start()
    t1.start()

    t1.join()
    t2.join() 

    print("done") 
    sleep(2)

print(time.ctime())
