# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu


var = dataiku.get_custom_variables()
f0 = eval(var["file_list"])
f1 = eval(var["mandatory"])

df = pd.DataFrame(zip(f0,f1), columns=["file_list","mandatory"])

# Write recipe outputs
required_files = dataiku.Dataset("required_files")
required_files.write_with_schema(df)