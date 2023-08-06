# %%
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd

# df1 = zp_issues(place_of_distribution="Altona")
df2 = zp_pages(place_of_distribution="Altona", plainpagefulltext='Bramsche')
df2

# %%
df2["place_of_distribution"]
# %%
