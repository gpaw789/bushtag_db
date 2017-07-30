import os
import sqlite3
import pandas as pd

'''
This script converts the csv data from bionet.nsw.gov.au to a sqlite db
input data: CSV from bionet.nsw.gov.au - you will need to remove all the headers
output data: sqlite db with correct column headers


'''

def build_df(pathname):
    with open(pathname, "r") as sfile:
        file = sfile.read()

    #split lines
    line = file.split("\n")

    #split tabs
    full = []
    for i in line:
        try:
            tabs = i.split("\t")
            full.append(tabs)
        except:
            print("SAVE ERROR {}".format(i))
            pass
    #convert to dataframe
    df = pd.DataFrame(full)

    #rename columns - need a blank at the end
    df.columns = ["dataset_name" ,  "sighting_key" ,  "species_code" ,  "kingdom_name" ,  "class_name" ,  "family_name" ,  "sort_order" ,  "scientific_name" ,  "exotic" ,  "common_name" ,  "nsw_status" ,  "comm_status" ,  "sensitivity_class" ,  "profile_id" ,  "date_first" ,  "date_last" ,  "number_individuals" ,  "estimate_typecode" ,  "source_code" ,  "observation_type" ,  "latitude_GDA94" ,  "longitude_GDA94" ,  "zone" ,  "easting" ,  "northing" ,  "accuracy", "image_url"]

    return df
def build_sql(dataframe):

    #create db
    conn = sqlite3.connect("test.db")

    #convert dataframe to sql
    dataframe.to_sql(name="bio", con = conn, if_exists = "replace")

#get path and remove non-files
path = "/YOUR_PATH_HERE/"
frames = []
file_list = os.listdir(path)
for file in file_list:
    if ".txt" not in file:
        file_list.remove(file)

#merge df
for file in file_list:
    df = build_df("{}/{}".format(path, file))
    frames.append(df)

result = pd.concat(frames)

build_sql(result)