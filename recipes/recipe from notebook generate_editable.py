# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku
from dataiku import pandasutils as pdu
import pandas as pd
from datetime import datetime
import dateutil.relativedelta

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
mydataset = dataiku.Dataset("config_editable")
df = mydataset.get_dataframe()


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

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
today = str(datetime.today()).split()[0]
d = datetime.strptime(today, "%Y-%m-%d")

l_month = []
for i in range(6):
    d2 = datetime.today() - dateutil.relativedelta.relativedelta(months=i)
    l_month.append(str(d2)[:7])

v["standard"]["list_month"] = l_month

d2 = datetime.today() - dateutil.relativedelta.relativedelta(months=1)
v["standard"]["previous_month"] = str(d2)[:7]

p.set_variables(v)