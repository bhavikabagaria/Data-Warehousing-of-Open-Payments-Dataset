# This code is to check & remove any irregularities in the data from the file which causes the SSIS to not able to
# identify the structure of the data properly

import pandas as pd
from pandas import Series, DataFrame
import csv
import shutil
import os

path = "H:\PGYR"
extension = "csv"
fileList = os.listdir(path)

for file in fileList:
    fileName, fileExtension = os.path.splitext(file)
    if fileExtension == ".csv":
        if "OP_DTL_OWNRSHP_PGYR" in fileName:
            with open(path + '\\' + file, "rU") as f:
                reader = csv.reader(f, delimiter=',', dialect="excel")
                rows = list(reader)

                for row in rows:
                    if ";" in row[20]:
                        row[20] = row[20].replace(';', ",")
                    if ";" in row[6]:
                        row[6] = row[6].replace(';', ":")

            with open(path + '\\' + file, mode="w") as outFile:
                writer = csv.writer(outFile, delimiter=";")
                writer.writerows(rows)
