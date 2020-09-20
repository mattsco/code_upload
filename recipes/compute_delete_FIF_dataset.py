# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu



client = dataiku.api_client()

p = client.get_project(dataiku.get_custom_variables()["projectKey"])

to_delete = []
for d in p.list_datasets():
    if d['name'].startswith("FIF_"):
        to_delete.append(d['name'])

for d in to_delete:
    p.get_dataset(d).delete()