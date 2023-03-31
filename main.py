from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
from LaborAction import LaborAction

firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service('/usr/local/bin/geckodriver'),
                          options=firefox_options)
driver.get('https://striketracker.ilr.cornell.edu/')
page_source = driver.page_source.encode("utf-8")

soup = bs(page_source, 'html.parser')

laborActionDivs = soup.find_all("div", {"class": "tab-content"})

laborActions = []
for div in range(0, 10):
    divSplit = laborActionDivs[div].get_text(separator="|", strip=True).split('|')
    index = [x for x, e in enumerate(divSplit) if "Employer" in e]
    employer = divSplit[index[0]+1][2:]
    index = [x for x, e in enumerate(divSplit) if "Labor Organization" in e]
    laborOrg = divSplit[index[0]+1][2:]
    index = [x for x, e in enumerate(divSplit) if "Start Date" in e]
    dateFrom = divSplit[index[0]+1][2:]
    index = [x for x, e in enumerate(divSplit) if "End Date" in e]
    dateTo = divSplit[index[0]+1][2:]
    index = [x for x, e in enumerate(divSplit) if "State" in e]
    state = divSplit[index[0]+1][2:]
    newAction = LaborAction(dateFrom, dateTo, employer, laborOrg, state)
    laborActions.append(newAction)

for i in range(0, 10):
    print(laborActions[i])

driver.quit()