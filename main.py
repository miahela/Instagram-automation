from selenium import webdriver
import time
import os

from selenium.webdriver.chrome.service import Service

proxy_url = "http://{username}:{password}@{host}:{port}".format(
    username="REMOVED_PRIVATE_VALUE",
    password="REMOVED_PRIVATE_VALUE",
    host="REMOVED_PRIVATE_VALUE",
    port="9090",
)

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Do something with the driver
driver.get("https://www.google.com")
print(driver.title)
time.sleep(50)

driver.quit()
