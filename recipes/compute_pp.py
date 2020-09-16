# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
tracking_folder = dataiku.Folder("3zAYHyFW")
tracking_folder_info = tracking_folder.get_info()


# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

pp_df = ... # Compute a Pandas dataframe to write into pp


# Write recipe outputs
pp = dataiku.Dataset("pp")
pp.write_with_schema(pp_df)
