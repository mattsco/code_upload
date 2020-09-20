# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu



# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

delete_FIF_dataset_df = ... # Compute a Pandas dataframe to write into delete_FIF_dataset


# Write recipe outputs
delete_FIF_dataset = dataiku.Dataset("delete_FIF_dataset")
delete_FIF_dataset.write_with_schema(delete_FIF_dataset_df)
