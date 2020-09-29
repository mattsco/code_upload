# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
files_folder = dataiku.Folder("bDGv9Em8")
files_folder_info = files_folder.get_info()


# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

perzer_df = ... # Compute a Pandas dataframe to write into perzer


# Write recipe outputs
perzer = dataiku.Dataset("perzer")
perzer.write_with_schema(perzer_df)
