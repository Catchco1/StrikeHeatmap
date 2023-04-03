from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
from LaborAction import LaborAction
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Selenium setup
firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service('/usr/local/bin/geckodriver'),
                          options=firefox_options)

# Get raw web data
driver.get('https://striketracker.ilr.cornell.edu/')
page_source = driver.page_source.encode("utf-8")
driver.quit()

# Parse for specific labor data
soup = bs(page_source, 'html.parser')
laborActionDivs = soup.find_all("div", {"class": "tab-content"})
laborActions = []
for div in range(0, len(laborActionDivs)):
    try:
        divSplit = laborActionDivs[div].get_text(separator="|", strip=True).split('|')
        index = [x for x, e in enumerate(divSplit) if "Employer" in e]
        if index:
            employer = divSplit[index[0]+1][2:]
        else:
            employer = None
        index = [x for x, e in enumerate(divSplit) if "Labor Organization" in e]
        if index:
            laborOrg = divSplit[index[0]+1][2:]
        else:
            laborOrg = None
        index = [x for x, e in enumerate(divSplit) if "Start Date" in e]
        if index:
            dateFrom = divSplit[index[0]+1][2:]
        else:
            dateFrom = None
        index = [x for x, e in enumerate(divSplit) if "End Date" in e]
        if index:
            dateTo = divSplit[index[0]+1][2:]
        else:
            dateTo = None
        index = [x for x, e in enumerate(divSplit) if "State" in e]
        if index:
            state = divSplit[index[0]+1][2:].strip()
        else:
            state = None
        newAction = LaborAction(dateFrom, dateTo, employer, laborOrg, state)
        laborActions.append(newAction)
    except:
        print(laborActionDivs[div].get_text(separator="|", strip=True).split('|'))

# Setup link between map and data
us_map = gpd.read_file("Shapefiles/States_shapefile.shp")

labor_data = pd.DataFrame([vars(x) for x in laborActions])
map_and_data = us_map.merge(labor_data, on="State_Name")