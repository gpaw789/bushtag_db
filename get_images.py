import sys
import pandas as pd
import sqlite3
from time import sleep

from py_ms_cognitive import PyMsCognitiveImageSearch


'''
This script will read the db, extracting the common_name
search common_name using bing image api to return API image link

delete_error() will purge the db for entry with errors

get_thumb(searchterm) will return the thumbnail image link

update_link() will push all the bing image link into the main db

'''

def get_images(sourcedb, bing_api_key):
    #extract
    conn = sqlite3.connect(sourcedb)
    query = "SELECT common_name FROM bio"
    df = pd.read_sql(query, conn)
    conn.close()

    #unique
    list_object_df  = df.common_name.unique()
    list_df = list(list_object_df)


    #check if the item exist in image_db
    conn = sqlite3.connect("image_db.db")
    cursor = conn.cursor()
    query = "SELECT common_name FROM image_db"
    list_object = cursor.execute(query)
    list_image_db = []
    for entry in list_object:
        list_image_db.append(entry[0])

    #only new values to the image_db
    list_new = list(set(list_df) - set(list_image_db))


    #get image/create
    list_link = []
    #trim the list if too much
    #list_new = list_new[:100]
    count = 0
    print(list_new)
    for entry in list_new:
        try:
            if entry is not (None or ""):
                link = get_thumb(entry, bing_api_key)
            else:
                link = "ERROR NOT FOUND"
        except:
            print("Unexpected error:", sys.exc_info()[0])
            link = "ERROR"
        list_link.append(link)
        count = count + 1
        print("{}: {}".format(count,link))
        sleep(0.1)

    #save db
    conn = sqlite3.connect("image_db.db")
    cursor = conn.cursor()
    print(len(list_new))
    print(len(list_link))
    if len(list_new) == len(list_link):
        for index, value in enumerate(list_new):
            query = "INSERT INTO image_db VALUES (\"{}\", \"{}\")".format(list_new[index], list_link[index])
            print(query)
            cursor.execute(query)

    query = "SELECT * FROM image_db"
    list_object = cursor.execute(query)
    list_image_db = []
    for entry in list_object:
        print(entry)

    conn.commit()
    conn.close()

    return 0

def delete_error(image_db):
    #get list link from image_db
    conn = sqlite3.connect(image_db)
    cursor = conn.cursor()
    query = "DELETE FROM image_db WHERE image_link = \"ERROR\""
    cursor.execute(query)
    query = "DELETE FROM image_db WHERE image_link = \"ERROR NOT FOUND\""
    cursor.execute(query)
    conn.commit()
    conn.close()

def get_thumb(search_term, bing_api_key):
    #cd6f1ecf04544fcfaee3183b95ae87e6 - dead

    search_service = PyMsCognitiveImageSearch(bing_api_key, search_term)
    first_fifty_result = search_service.search(limit=3, format='json') #1-50
    return first_fifty_result[0].thumbnail_url

def update_link(sourcedb, image_db):
    #get list link from image_db
    conn = sqlite3.connect(image_db)
    query = "SELECT * FROM image_db"
    df = pd.read_sql(query, conn)
    list_name = list(df["common_name"])
    df_dict = dict(zip(df["common_name"],df["image_link"]))

    conn.close()


    #update db
    conn = sqlite3.connect(sourcedb)
    cursor = conn.cursor()
    for entry in list_name:
        query = "UPDATE bio SET image_url = \"{}\" WHERE common_name = \"{}\"".format(df_dict[entry],entry)
        cursor.execute(query)
    conn.commit()
    conn.close()


    return 0




delete_error("image_db.db")
get_images("2015.db", "GET_YOUR_OWN")
update_link("all.db", "image_db.db")