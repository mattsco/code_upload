# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
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

df = pd.DataFrame(list_tracking)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Filter records before only after date
var = dataiku.get_custom_variables()
date_only_after = var["only_after"]
df = df[df["date"]>=date_only_after]
df

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Keep last date for a specific file type.
df.sort_values(by=["date", "file_type"], ascending=[0,1], inplace=True)
df.drop_duplicates(subset=["file_type"], keep='first', inplace=True)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Create dataframe from variables
f0 = eval(var["file_list"])
f1 = eval(var["mandatory"])
opt = pd.DataFrame(zip(f0,f1), columns=["file_list","mandatory"])
opt.sort_values(by=["mandatory"], ascending=[0], inplace=True)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Join with config
out = pd.merge(opt,df, how="left", left_on="file_list", right_on="file_type")
out_small = out[["file_list","mandatory","status","initial_filename", "comment"]]
out_small["status"].fillna("missing", inplace=True)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Raise error if missing files.
if "missing" in out_small[out_small["mandatory"]=="1"].status.unique():
    out_tmp = out_small[out_small["mandatory"]=="1"]
    out_tmp = out_tmp[out_tmp["status"]=="missing"]
    m = ",".join(list(out_tmp.file_list.values))
    raise Exception("Mandatory file missing: %s"%(m))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write report
pp = dataiku.Dataset("output_report")
pp.write_with_schema(out_small)


#Copy output files in folder.
output_folder = dataiku.Folder(files_folder_ID) 
archived_folder = dataiku.Folder(archived_folder_ID)

output_folder.clear()
print df.columns
for i, row in df.iterrows():

    file_type = row["file_type"]
    file_name = row["dss_filename"]
    file_stream = archived_folder.get_download_stream(file_name)
    output_folder.upload_stream(file_name, file_stream)
    print("File %s uploaded for %s"%(file_name, file_type))