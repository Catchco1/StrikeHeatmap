from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs

firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service('/usr/local/bin/geckodriver'),
                          options=firefox_options)
driver.get('https://striketracker.ilr.cornell.edu/')
print(driver.page_source.encode("utf-8"))
driver.quit()