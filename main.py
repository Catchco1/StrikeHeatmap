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
from datetime import datetime
import imageio

state_tracker = {
    "Alabama": 0,
    "Alaska": 0,
    "Arizona": 0,
    "Arkansas": 0,
    "California": 0,
    "Colorado": 0,
    "Connecticut": 0,
    "Delaware": 0,
    "Florida": 0,
    "Georgia": 0,
    "Hawaii": 0,
    "Idaho": 0,
    "Illinois": 0,
    "Indiana": 0,
    "Iowa": 0,
    "Kansas": 0,
    "Kentucky": 0,
    "Louisiana": 0,
    "Maine": 0,
    "Maryland": 0,
    "Massachusetts": 0,
    "Michigan": 0,
    "Minnesota": 0,
    "Mississippi": 0,
    "Missouri": 0,
    "Montana": 0,
    "Nebraska": 0,
    "Nevada": 0,
    "New Hampshire": 0,
    "New Jersey": 0,
    "New Mexico": 0,
    "New York": 0,
    "North Carolina": 0,
    "North Dakota": 0,
    "Ohio": 0,
    "Oklahoma": 0,
    "Oregon": 0,
    "Pennsylvania": 0,
    "Rhode Island": 0,
    "South Carolina": 0,
    "South Dakota": 0,
    "Tennessee": 0,
    "Texas": 0,
    "Utah": 0,
    "Vermont": 0,
    "Virginia": 0,
    "Washington": 0,
    "West Virginia": 0,
    "Wisconsin": 0,
    "Wyoming": 0,
    "District of Columbia": 0,
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
        dateFrom = datetime.strptime(divSplit[index[0]+1][2:], '%m/%d/%Y')
    else:
        dateFrom = None
    index = [x for x, e in enumerate(divSplit) if "End Date" in e]
    if index:
        dateTo = datetime.strptime(divSplit[index[0]+1][2:], '%m/%d/%Y')
    else:
        dateTo = None
    index = [x for x, e in enumerate(divSplit) if "State" == e]
    if index:
        state = divSplit[index[0]+1][2:].strip()
    else:
        state = None
    newAction = LaborAction(dateFrom, dateTo, employer, laborOrg, state)
    laborActions.append(newAction)

# Setup base map
us_map = pygris.states(cb = True, resolution = "20m")
us_rescaled = shift_geometry(us_map)

# Get the month range
if laborActions[0].dateTo is None:
    month_list = pd.date_range(start=laborActions[len(laborActions)-1].dateFrom.date(), end=laborActions[0].dateFrom.date(), freq='M').union([laborActions[len(laborActions)-1].dateFrom.date(), laborActions[0].dateFrom.date()])
else:
    month_list = pd.date_range(start=laborActions[len(laborActions)-1].dateFrom.date(), end=laborActions[0].dateTo.date(), freq='M').union([laborActions[len(laborActions)-1].dateFrom.date(), laborActions[0].dateTo.date()])

# Count strikes for one month
frames = []
stateDicts = []
maxStrikes = 0
for month in month_list:
    state_tracker = dict.fromkeys(state_tracker, 0)
    for action in laborActions:
        if action.dateTo is None:
            if action.dateFrom.month == month.month and action.dateFrom.year == month.year and action.State_Name in state_tracker:
                state_tracker[action.State_Name] += 1
        else:
            if action.dateFrom.month <= month.month <= action.dateTo.month and action.dateFrom.year <= month.year <= action.dateTo.year and action.State_Name in state_tracker:
                state_tracker[action.State_Name] += 1
    if max(state_tracker.values()) > maxStrikes:
        maxStrikes = max(state_tracker.values())
    stateDicts.append(state_tracker)

for index, state_tracker in enumerate(stateDicts):
    labor_data = pd.DataFrame(state_tracker.items(), columns=['State_Name', 'Strikes'])

    # Setup link between map and data
    map_and_data = us_rescaled.merge(labor_data, left_on="NAME", right_on="State_Name")

    # Drawing the map!
    fig, ax = plt.subplots(1, figsize=(12, 8))
    plt.xticks([])
    plt.yticks([])

    # For testing uncomment the following line to print number of strikes on each state
    map_and_data.apply(lambda x: ax.annotate(text=x.Strikes, xy=x.geometry.centroid.coords[0], ha='center', fontsize=10),axis=1)
    map_and_data.plot(column="Strikes", cmap="Reds", linewidth=0.4, ax=ax, edgecolor=".4", vmax=maxStrikes)
    bar_info = plt.cm.ScalarMappable(cmap="Reds", norm=plt.Normalize(vmin=0, vmax=maxStrikes))
    bar_info._A = []
    cbar = fig.colorbar(bar_info, ax=ax, shrink=0.75)
    plt.title("Heatmap of strikes per state per month\nCurrent Month: " + str(month_list[index].month) + "/" + str(month_list[index].year))
    plt.savefig(f"imgs/{month.year}_{month.month}.png")
    plt.close()

    # Save the GIF frames
    image = imageio.v2.imread(f'imgs/{month.year}_{month.month}.png')
    frames.append(image)

# Combine frames to make final GIF
imageio.mimsave('./strikes.gif', frames, fps = 1, loop = 0)