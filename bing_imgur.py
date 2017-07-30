#convert bing image to imgur
from imgurpython import ImgurClient
import pandas as pd
import sqlite3
import time

'''
this script is to generate a backup imgur link in case bing deides to pull their API

'''




# staging imgur client - use https://api.imgur.com/oauth2/addclient
client_id = 'GET_YOUR_OWN'
client_secret = 'GET_YOUR_OWN'
client = ImgurClient(client_id, client_secret)

def read_bing_db(source):
    # extract
    conn = sqlite3.connect(source)
    query = "SELECT * FROM image_db"
    df = pd.read_sql(query, conn)
    conn.close()

    df["imgur"] = ""

    #df = df[:15]
    #add imgur link
    for bing_link in df["image_link"]:

                #write to db
                conn = sqlite3.connect("image_db_dual.db")
                cursor = conn.cursor()

                #check if exist
                query = "SELECT imgur FROM image_db WHERE image_link = \"{}\"".format(bing_link)
                cursor.execute(query)
                if cursor.fetchone()[0] is "":
                    # upload from url
                    print("Uploading... {}".format(bing_link))
                    callback = client.upload_from_url(bing_link, config=None, anon=False)
                    imgur_link = callback['link']
                    query = "UPDATE image_db SET imgur = \"{}\" WHERE image_link = \"{}\"".format(imgur_link,bing_link)
                    cursor.execute(query)
                    print("Query executed! {}".format(imgur_link))
                    time.sleep(10)       #not to spam the API request
                print(query)
                conn.commit()

    conn.close()



read_bing_db("image_db.db")