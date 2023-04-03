from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
from LaborAction import LaborAction
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import pygris
from pygris.utils import shift_geometry

state_tracker = {
    "ALABAMA": 0,
    "ALASKA": 0,
    "ARIZONA": 0,
    "ARKANSAS": 0,
    "CALIFORNIA": 0,
    "COLORADO": 0,
    "CONNECTICUT": 0,
    "DELAWARE": 0,
    "FLORIDA": 0,
    "GEORGIA": 0,
    "HAWAII": 0,
    "IDAHO": 0,
    "ILLINOIS": 0,
    "INDIANA": 0,
    "IOWA": 0,
    "KANSAS": 0,
    "KENTUCKY": 0,
    "LOUISIANA": 0,
    "MAINE": 0,
    "MARYLAND": 0,
    "MASSACHUSETTS": 0,
    "MICHIGAN": 0,
    "MINNESOTA": 0,
    "MISSISSIPPI": 0,
    "MISSOURI": 0,
    "MONTANA": 0,
    "NEBRASKA": 0,
    "NEVADA": 0,
    "NEW HAMPSHIRE": 0,
    "NEW JERSEY": 0,
    "NEW MEXICO": 0,
    "NEW YORK": 0,
    "NORTH CAROLINA": 0,
    "NORTH DAKOTA": 0,
    "OHIO": 0,
    "OKLAHOMA": 0,
    "OREGON": 0,
    "PENNSYLVANIA": 0,
    "RHODE ISLAND": 0,
    "SOUTH CAROLINA": 0,
    "SOUTH DAKOTA": 0,
    "TENNESSEE": 0,
    "TEXAS": 0,
    "UTAH": 0,
    "VERMONT": 0,
    "VIRGINIA": 0,
    "WASHINGTON": 0,
    "WEST VIRGINIA": 0,
    "WISCONSIN": 0,
    "WYOMING": 0,
    "DISTRICT OF COLUMBIA": 0,
}

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

# Count strikes for one month
for action in laborActions:
    if action.State_Name in state_tracker:
        state_tracker[action.State_Name] += 1

labor_data = pd.DataFrame(state_tracker.items(), columns=['State_Name', 'Strikes'])

# Setup link between map and data
us_map = pygris.states(cb = True, resolution = "20m")
us_rescaled = shift_geometry(us_map)

map_and_data = us_map.merge(labor_data, on="State_Name")

# Drawing the map!
fix, ax = plt.subplots(1, figsize=(12, 8))
plt.xticks(rotation=90)

map_and_data.plot(column="Strikes", cmap="Reds", linewidth=0.4, ax=ax, edgecolor=".4")
plt.savefig("test.png")