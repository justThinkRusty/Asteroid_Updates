import requests #For API string pull
import csv
import json
import numpy as np
import platform
from datetime import date 
import time
from twython import Twython
from auth import *

today = date.today()
twitter = Twython(API_key, API_secret, token, secret)

category = ["Atira", "Aten", "Apollo", "_Amor"]
url_suffix = ["IEO", "ATE", "APO", "AMO"]
cat_nums = 4

if platform.system() == "Windows":
    fullpath_spec = "C:/Users/Charlie/Documents/0 Personal Projects/PythonExp/Barbee NHATS Project/" #Windows
elif platform.system() == "Darwin":
    fullpath_spec = "/Users/charlie/Documents/Documents/PythonExp/Barbee_NHATS_Project/" #MAC
elif platform.system() == "Linux":
    fullpath_spec = "/home/pi/Documents/PythonExp/Barbee_NHATS_Project/" #Py

# fullpath_spec = "C:/Users/Charlie/Documents/0 Personal Projects/PythonExp/Barbee NHATS Project/" #WIN
# fullpath_spec = "/Users/charlie/Documents/PythonExp/Barbee_NHATS_Project/" #MAC
# fullpath_spec = "/home/pi/Documents/PythonExp/Barbee_NHATS_Project/" #Py

SMDB_Atira = requests.get('https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,pdes,e,a,i,H&sb-class=IEO'); SMDB_Atira_unc = SMDB_Atira.json()
SMDB_Aten = requests.get('https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,pdes,e,a,i,H&sb-class=ATE'); SMDB_Aten_unc = SMDB_Aten.json()
SMDB_Apollo = requests.get('https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,pdes,e,a,i,H&sb-class=APO'); SMDB_Apollo_unc = SMDB_Apollo.json()
SMDB_Amor = requests.get('https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,pdes,e,a,i,H&sb-class=AMO'); SMDB_Amor_unc = SMDB_Amor.json()

#Latest count totals for each
Atira_tot = int(SMDB_Atira_unc['count'])
Aten_tot = int(SMDB_Aten_unc['count'])
Apollo_tot = int(SMDB_Apollo_unc['count'])
Amor_tot = int(SMDB_Amor_unc['count'])


#Get new names from pulled data:
IEO_names = [None]*Atira_tot
for i in range(0,int(SMDB_Atira_unc['count'])):
    IEO_names[i] = SMDB_Atira_unc['data'][i][1]

ATE_names = [None]*Aten_tot
for i in range(0,int(SMDB_Aten_unc['count'])):
    ATE_names[i] = SMDB_Aten_unc['data'][i][1]

APO_names = [None]*Apollo_tot
for i in range(0,int(SMDB_Apollo_unc['count'])):
    APO_names[i] = SMDB_Apollo_unc['data'][i][1]

AMO_names = [None]*Amor_tot
for i in range(0,int(SMDB_Amor_unc['count'])):
    AMO_names[i] = SMDB_Amor_unc['data'][i][1]

#Open lists with the old names:
f = open(fullpath_spec + 'Old_IEO.txt','r')
Old_IEO = json.load(f)

f = open(fullpath_spec + 'Old_ATE.txt','r')
Old_ATE = json.load(f)

f = open(fullpath_spec + 'Old_APO.txt','r')
Old_APO = json.load(f)

f = open(fullpath_spec + 'Old_AMO.txt','r')
Old_AMO = json.load(f)


# Initialize the new name vectors:
new_Atira_names = [None]*abs(len(IEO_names) - len(Old_IEO))
new_Aten_names = [None]*abs(len(ATE_names) - len(Old_ATE))
new_Apollo_names = [None]*abs(len(APO_names) - len(Old_APO))
new_Amor_names = [None]*abs(len(AMO_names) - len(Old_AMO))

def send_it(tweetToSend):
    twitter.update_status(status=tweetToSend)
    print(tweetToSend)

#Compare the two lists for differences:
def getNewNames(old_mat,  new_mat, toBeAppended):
    #Create a new name file to return for each category
    k = 0
    for i in new_mat:
        if i not in old_mat: #Found a missing one
            if k >= abs(len(old_mat) - len(new_mat)): #Asteroid recategorization has occured
                toBeAppended.append(i)
            else:
                toBeAppended[k] = i
                k = k + 1
    if toBeAppended == [None]: # This is where the bug fix is for the moment - must invetigate a more robust way of verifing all new asteroids were found and what deltas can exist
        toBeAppended = []
    return toBeAppended


new_Atira_names = getNewNames(Old_IEO,  IEO_names, new_Atira_names)
new_Aten_names = getNewNames(Old_ATE,  ATE_names, new_Aten_names)
new_Apollo_names = getNewNames(Old_APO,  APO_names, new_Apollo_names)
new_Amor_names = getNewNames(Old_AMO,  AMO_names, new_Amor_names)


def addNamesToTweet(name_list, twit, strName):
    if len(name_list) > 1:
        twit = twit + "\n" + strName + ": "
        for i in name_list:
            if i == name_list[-1]:
                twit = twit + i 
            else:
                twit = twit + i + ", "
    elif len(name_list) == 1:
        twit = twit + "\n" + strName + ": "
        twit = twit + name_list[0]
        
    return twit

num_disc_today = len(new_Atira_names) + len(new_Aten_names) + len(new_Apollo_names) + len(new_Amor_names)
day_add = [len(new_Atira_names), len(new_Aten_names), len(new_Apollo_names), len(new_Amor_names)]

hist = open(fullpath_spec + "AstList.csv", "r+")
#Formatted csv file with total number for day and last known asteroid (formatting to come)
hist_csv = csv.reader(hist, delimiter=',')
WTD = []
YTD = []
for row in hist_csv:
        YTD.append(int(row[1]))
        WTD.append(int(row[2]))

for i in range(0,len(WTD)):
    WTD[i] = WTD[i] + day_add[i]
    YTD[i] = YTD[i] + day_add[i]

if num_disc_today == 0:
    tweet = "Yesterday, " + str(today.month) + "/" + str(today.day-1) + "/" + str(today.year) + ", there were no near-Earth asteroids added to the small body database - check back again tomorrow!"
elif num_disc_today == 1:
    tweet = "Yesterday there was " + str(num_disc_today) + " near-Earth asteroid discovered/categorized:"
else:
    tweet = "Yesterday there were " + str(num_disc_today) + " near-Earth asteroids discovered/categorized:"

tweet = addNamesToTweet(new_Atira_names, tweet, "Atira")
tweet = addNamesToTweet(new_Aten_names, tweet, "Aten")
tweet = addNamesToTweet(new_Apollo_names, tweet, "Apollo")
tweet = addNamesToTweet(new_Amor_names, tweet, "Amor")

if  date.today().weekday() == 6: #It's sunday - it's also time for a wrapup
    tweet_week = " \n It's sunday and also time for your weekly near-Earth asteroid wrapup. "
    num_disc_week = sum(WTD)
    if num_disc_week == 0:
        tweet_week = tweet_week + "No new asteroids were discovered this week, we'll get 'em next time!"
    elif num_disc_week == 1:
        tweet_week = tweet_week + str(num_disc_week) + " new asteroid was discovered this week!"
    else:
        tweet_week = tweet_week + str(num_disc_week) + " new asteroids were discovered this week!"
    #Now reset weekly counter
    WTD = [0, 0, 0, 0]
    send_it(tweet_week)


if  today.month == 1 and today.day == 1: #Happy new year 
    tweet = "Happy new year! As of today, the near-Earth asteroid totals are: \n"
    tweet = tweet + "Atiras: " + str(Atira_tot) + " - Discovered last year: " + str(YTD[0]) + "\n"
    tweet = tweet + "Atens: " + str(Aten_tot) + " - Discovered last year: " + str(YTD[1]) + "\n"
    tweet = tweet +  "Apollos: " + str(Apollo_tot) + " - Discovered last year: " + str(YTD[2]) + "\n"
    tweet = tweet +  "Amors: " + str(Amor_tot) + " - Discovered last year: " + str(YTD[3])
    send_it(tweet)
    #Now reset year counter
    YTD = [0, 0, 0, 0]

def ReplyNamesToTweet(name_list, strName, t_ID):

    temp_list = name_list

    #Max number of asteroids in one tweet should be 20 for reliabile performance? Depends on how many we found in a month... 
    # like 2022 SX55 takes up two more characters - Assuming 9 characters max per name, 20 names would be 180 characters - In theory 30 possible 
    # But even at 25 I have an odd tweet length issue every few months. Need to think of a more robust solution
    max_per = 20

    while len(temp_list) > 0: #While there are asteroids to still post about
        twit = strName + ": "
        if len(temp_list) < max_per: #This will be the last tweet to go in the pile - let it rip

            for idx, i in enumerate(temp_list):

                if i == temp_list[-1]:
                    twit = twit + i 
                    
                else:
                    twit = twit + i + ", "  
                    temp_list.remove(i)
            temp_list = []

        else:
            num = 0
            for i in temp_list:
                if num < max_per:
                    num = num + 1
                    if i == temp_list[-1]:
                        twit = twit + i 
                        # temp_list.remove(i)
                    else:
                        twit = twit + i + ", "  
                        # temp_list.remove(i)
            temp_list[0:max_per-1] = []
        if len(twit) != 0:
            twitter.update_status(status = twit, in_reply_to_status_id = t_ID , auto_populate_reply_metadata=True)
            time.sleep(2)
            print(twit)


    # if len(name_list) > 0:
    #     twit = strName + ": "
    #     for i in name_list:
    #         if i == name_list[-1]:
    #             twit = twit + i 
    #         else:
    #             twit = twit + i + ", "
    # if len(twit) != 0:
    #     # twitter.update_status(status = twit, in_reply_to_status_id = t_ID , auto_populate_reply_metadata=True)
    #     print(twit)

if len(tweet) > 280: #tweet is too long, break all down into subreplies:

    tweet = "Since the last update tweet, there were " + str(num_disc_today) + " near Earth asteroids discovered/categorized:" #Reset beginning tweet
    send_it(tweet)

    # twitter_ID = input("Please enter twitter ID for tweet: ")
    user_timeline=twitter.get_user_timeline(screen_name="AsteroidUpdates", count=1)
    twitter_ID = user_timeline[0]["id"]
    # print(new_Amor_names)
    # print(new_Apollo_names)
    # print(new_Aten_names)
    # print(new_Atira_names)
    ReplyNamesToTweet(new_Amor_names, "Amor", twitter_ID)
    ReplyNamesToTweet(new_Apollo_names, "Apollo", twitter_ID)
    ReplyNamesToTweet(new_Aten_names, "Aten", twitter_ID)
    ReplyNamesToTweet(new_Atira_names, "Atira", twitter_ID)
    
else:
    send_it(tweet)


w_CSV = open(fullpath_spec + "AstList.csv", 'w', newline='')
wrtr = csv.writer(w_CSV)

wrtr.writerow([Atira_tot, YTD[0], WTD[0]])
wrtr.writerow([Aten_tot, YTD[1], WTD[1]])
wrtr.writerow([Apollo_tot, YTD[2], WTD[2]])
wrtr.writerow([Amor_tot, YTD[3], WTD[3]])

# Write new corner files:
#Store the new lists for tomorrow:
with open(fullpath_spec + 'Old_IEO.txt', 'w') as filehandle:
    # store the data as binary data stream
    json.dump(IEO_names, filehandle)

with open(fullpath_spec + 'Old_ATE.txt', 'w') as filehandle:
    # store the data as binary data stream
    json.dump(ATE_names, filehandle)

with open(fullpath_spec + 'Old_APO.txt', 'w') as filehandle:
    # store the data as binary data stream
    json.dump(APO_names, filehandle)

with open(fullpath_spec + 'Old_AMO.txt', 'w') as filehandle:
    # store the data as binary data stream
    json.dump(AMO_names, filehandle)
