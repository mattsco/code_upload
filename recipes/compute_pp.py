# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
tracking_folder = dataiku.Folder("3zAYHyFW")
tf_path = tracking_folder.get_path()
tf_path

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
paths = tracking_folder.list_paths_in_partition()
paths

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
list_tracking = []
for tracking_file in paths:
    with tracking_folder.get_download_stream(tracking_file) as f:
        list_tracking.append(eval(f.read()))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
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
f0 = eval(var["file_list"])
f1 = eval(var["mandatory"])

opt = pd.DataFrame(zip(f0,f1), columns=["file_list","mandatory"])
opt.sort_values(by=["mandatory"], ascending=[0], inplace=True)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df.head()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Join with config
out = pd.merge(opt,df, how="left", left_on="file_list", right_on="file_type")
out_small = out[["file_list","mandatory","status"]].fillna("missing")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Raise error if missing files.
if "missing" in out_small[out_small["mandatory"]=="1"].status.unique():
    out_tmp = out_small[out_small["mandatory"]=="1"]
    out_tmp = out_tmp[out_tmp["status"]=="missing"]
    m = ",".join(list(out_tmp.file_list.values))
    raise Exception("Mandatory file missing: %s"%(m))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
pp = dataiku.Dataset("pp")
pp.write_with_schema(out_small)