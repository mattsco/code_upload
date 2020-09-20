import dataiku
from dataiku import pandasutils as pdu
import pandas as pd

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE

mydataset = dataiku.Dataset("config_editable")
df = mydataset.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
dataiku.get_custom_variables()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
col_file_name = df.columns[1]
col_extention = df.columns[2]
col_mandatory = df.columns[3]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
c = dataiku.api_client()
p = c.get_project(dataiku.get_custom_variables()["projectKey"])
v = p.get_variables()
v["standard"]["file_list"] = list(df[col_file_name].values)
v["standard"]["extention"] = list(df[col_extention].values)
v["standard"]["mandatory"] = list(df[col_mandatory].values)
p.set_variables(v)

