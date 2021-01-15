from selenium import webdriver
import json
import sys
import os
import time
import scraper as sc




driver = webdriver.Chrome(chrome_options=sc.set_chrome_options())

executor_url = driver.command_executor._url
session_id = driver.session_id
dic={
    "url":executor_url,
    "id":session_id
}
print(json.dumps(dic))
sys.stdout.flush()

sc.loginUser(driver)
#os.system(f'cmd /k "python scrape.py {executor_url} {session_id}"')

while len(driver.window_handles)!=0:
    pass

