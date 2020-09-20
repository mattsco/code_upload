# -*- coding: utf-8 -*-
#UPDATE CONFIG
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
col_extension = df.columns[2]
col_mandatory = df.columns[3]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
c = dataiku.api_client()
p = c.get_project(dataiku.get_custom_variables()["projectKey"])
v = p.get_variables()
v["standard"]["file_list"] = list(df[col_file_name].values)
v["standard"]["extension"] = list(df[col_extension].values)
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



#Run 
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

tracking_folder_ID = "3zAYHyFW"
archived_folder_ID = "vOv1eTkv"
files_folder_ID = "bDGv9Em8"
output_report = "output_report"

colname = ['comment', 'date', 'dss_filename', 'file_type', 'initial_filename', 'status', 'user']

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Iterate on tracking files. 
tracking_folder = dataiku.Folder(tracking_folder_ID)
paths = tracking_folder.list_paths_in_partition()
list_tracking = []
for tracking_file in paths:
    with tracking_folder.get_download_stream(tracking_file) as f:
        list_tracking.append(eval(f.read()))

df_t = pd.DataFrame(list_tracking)
if len(df) == 0:
    raise Exception("Folders empty")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Filter records before only after date
#var = dataiku.get_custom_variables()
#date_only_after = var["only_after"]
#df = df[df["date"]>=date_only_after]
#df

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Keep last date for a specific file type.
df_t.sort_values(by=["dss_filename", "file_type"], ascending=[0,1], inplace=True)
df_t.drop_duplicates(subset=["file_type"], keep='first', inplace=True)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Create dataframe from variables
#f0 = eval(var["file_list"])
#f1 = eval(var["mandatory"])
#opt = pd.DataFrame(zip(f0,f1), columns=["file_list","mandatory"])
#opt.sort_values(by=["mandatory"], ascending=[0], inplace=True)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Join with config
out = pd.merge(df,df_t, how="left", left_on=col_file_name, right_on="file_type")
out_small = out[["upload_date", "file_month", col_file_name, col_mandatory, "status", "initial_filename", "comment", 'user']]
out_small["status"].fillna("missing", inplace=True)


# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write report
pp = dataiku.Dataset("output_report")
pp.write_with_schema(out_small)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Raise error if missing files.
if "missing" in out_small[out_small[col_mandatory]=="Yes"].status.unique():
    out_tmp = out_small[out_small[col_mandatory]=="Yes"]
    out_tmp = out_tmp[out_tmp["status"]=="missing"]
    m = ", ".join(list(out_tmp[col_file_name].values))
    raise Exception("Files missing: %s"%(m))


#Copy output files in folder.
output_folder = dataiku.Folder(files_folder_ID) 
archived_folder = dataiku.Folder(archived_folder_ID)

output_folder.clear()
print df_t.columns
for i, row in df_t.iterrows():

    file_type = row["file_type"]
    file_name = row["dss_filename"]
    file_stream = archived_folder.get_download_stream(file_name)
    file_type_clean = file_type.split(".")[0].replace("-"," ").replace("_"," ").replace("MMMYYYY","")
    for i in range(4):
        file_type_clean = file_type_clean.replace("  "," ").strip() 
    file_type_clean = file_type_clean.replace(" ","_")
    output_folder.upload_stream(file_type_clean, file_stream)
    print("File %s uploaded for %s"%(file_name, file_type))
    
    
    params = {u'filesSelectionRules': {u'excludeRules': [],
              u'explicitFiles': [],
              u'includeRules': [{u'expr': file_type_clean,
                u'matchingMode': u'FULL_PATH',
                u'mode': u'GLOB'}],
              u'mode': u'RULES_INCLUDED_ONLY'},
             u'folderSmartId': files_folder_ID,
             u'notReadyIfEmpty': False}


    p.create_dataset("FIF_" + file_type_clean, 'FilesInFolder', params=params, formatType="excel", formatParams=None)