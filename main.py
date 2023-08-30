from selenium import webdriver
import time
import os

from selenium.webdriver.chrome.service import Service

proxy_url = "http://{username}:{password}@{host}:{port}".format(
    username="8yn4lm9edef2svn-country-es-sid-22671226",
    password="nw8A9TWC43Njpb5",
    host="resi.rainproxy.io",
    port="9090",
)

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Do something with the driver
driver.get("https://www.google.com")
print(driver.title)
time.sleep(50)

driver.quit()
