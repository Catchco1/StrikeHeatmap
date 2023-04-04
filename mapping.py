import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import pygris
from pygris.utils import shift_geometry


us = pygris.states(cb = True, resolution = "20m")
us_rescaled = shift_geometry(us)
print(us_rescaled)
us_rescaled.plot(figsize = (12, 8))

plt.savefig("test.png")