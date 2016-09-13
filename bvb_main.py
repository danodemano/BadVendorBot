#!/usr/bin/python
import praw
from prawoauth2 import PrawOAuth2Mini
import pdb
import re
import os
import sys
import sqlite3
import datetime
from bvb_config import *

#Get the current datetime for tracking later on
curdate = datetime.datetime.utcnow().isoformat()

#Connect to the sqlite database defined in the config file
con = None
con = sqlite3.connect(database)

#Create the reddit oauth instance - this is black magic, just roll with it
reddit_client = praw.Reddit(user_agent=user_agent)
oauth_helper = PrawOAuth2Mini(reddit_client, app_key=app_key,
                              app_secret=app_secret,
                              access_token=access_token,
                              refresh_token=refresh_token,
                              scopes=scopes)
		
#Get all the entries from the database to keep from replying twice
cursor = con.execute("SELECT post_id from post_tracking")
posts_replied_to = []
for row in cursor:
    print (row[0])
	#Append the current post ID to the array for tracking
    posts_replied_to.append(row[0])

#Get the top 5 values from our subreddit
subreddit = reddit_client.get_subreddit(subname)
for submission in subreddit.get_hot(limit=5):
	#print submission.title
    print (submission.title)

    #Search in the array to ensure we haven't replied to this post yet
    if submission.id not in posts_replied_to:
        #Do a case insensitive search for a specific text
        if re.search("Fuck", submission.title, re.IGNORECASE):
            #Reply to the post
            submission.add_comment("Bad vendor, no doughnut!!")
            print ("Bot replying to : ", submission.title)
            #Update the database with this record
            print ("INSERT INTO post_tracking(subreddit, title, post_id, datetime) VALUES('" + subname + "','" + submission.title + "','" + submission.id + "','" + curdate + "')")
            con.execute("INSERT INTO post_tracking(subreddit, title, post_id, datetime) VALUES('" + subname + "','" + submission.title + "','" + submission.id + "','" + curdate + "')")

#Commit the database changes
con.commit()

#Close the database connection
if con:
    con.close()
