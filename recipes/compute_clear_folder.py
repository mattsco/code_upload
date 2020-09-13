# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
archived_folder = dataiku.Folder("vOv1eTkv", ignore_flow=True)
archived_folder_info = archived_folder.get_info()
tracking_folder = dataiku.Folder("3zAYHyFW",  ignore_flow=True)
tracking_folder_info = tracking_folder.get_info()
files_folder = dataiku.Folder("bDGv9Em8", ignore_flow=True)
files_folder_info = files_folder.get_info()


files_folder.clear()
tracking_folder.clear()
archived_folder.clear()


