# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

df = dataiku.Dataset("required_files_check").get_dataframe()

try:
    nok = df[df["pass"]=="NOK"]
    assert len(nok)==0
except:
    m = ",".join(list(nok.file_list.values))
    raise Exception("Mandatory file missing: %s"%(m))


archive_folder_id = dataiku.get_custom_variables()["archive_folder"]

#modify the output folder id
output_folder = dataiku.Folder("bDGv9Em8") 
archived_folder = dataiku.Folder(archive_folder_id)


df = dataiku.Dataset("last_results_per_file").get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
output_folder.clear()

for i, row in df.iterrows():

    if  row["outdated"] == "no":
        country = row["country"]
        customer_type = row["customer_type"]
        file_name = row["dss_filename"]
        file_stream = archived_folder.get_download_stream(file_name)
        output_folder.upload_stream(file_name, file_stream)
        print("File %s uploaded for %s %s"%(file_name, country, customer_type))