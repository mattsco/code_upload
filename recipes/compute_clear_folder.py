# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
archived_folder = dataiku.Folder("vOv1eTkv")
archived_folder_info = archived_folder.get_info()
tracking_folder = dataiku.Folder("3zAYHyFW")
tracking_folder_info = tracking_folder.get_info()
files_folder = dataiku.Folder("bDGv9Em8")
files_folder_info = files_folder.get_info()


files_folder.clear()
tracking_folder.clear()
archived_folder.clear()


