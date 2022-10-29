import requests  # For API string pull
import csv
import json
from datetime import date
import time
import platform
from alive_progress import alive_bar  # Creating a waitbar for to show progress during long sections
from twython import Twython
from auth import API_key_MBA, API_secret_MBA, token_MBA, secret_MBA


today = date.today()
twitter = Twython(API_key_MBA, API_secret_MBA, token_MBA, secret_MBA)

#Define twitter sending code
def send_it(tweetToSend):
        twitter.update_status(status=tweetToSend)
        # print(tweetToSend)

category = ["Mars-crossing", "Inner Main-belt", "Main-belt", "Outer Main-belt"]
url_suffix = ["MCA", "IMB", "MBA", "OMB"]
cat_nums = 4

tweet_format = "short"  # "short" or "long"

if platform.system() == "Windows":
    fullpath_spec = "C:/Users/Charlie/Documents/0 Personal Projects/PythonExp/Barbee NHATS Project/" #Windows
elif platform.system() == "Darwin":
    fullpath_spec = "/Users/charlie/Documents/Documents/PythonExp/Barbee_NHATS_Project/" #MAC
elif platform.system() == "Linux":
    fullpath_spec = "/home/pi/Documents/PythonExp/Barbee_NHATS_Project/" #Pi

# Atira -> MCA -> IEO
# Aten -> IMB -> ATE
# Apollo -> MBA -> APO
# Amor -> OMB -> AMO
SMDB_MCA = requests.get('https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,pdes,e,a,i,H&sb-class=MCA'); SMDB_MCA_unc = SMDB_MCA.json()
SMDB_IMB = requests.get('https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,pdes,e,a,i,H&sb-class=IMB'); SMDB_IMB_unc = SMDB_IMB.json()
SMDB_MBA = requests.get('https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,pdes,e,a,i,H&sb-class=MBA'); SMDB_MBA_unc = SMDB_MBA.json()
SMDB_OMB = requests.get('https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,pdes,e,a,i,H&sb-class=OMB'); SMDB_OMB_unc = SMDB_OMB.json()

# Latest count totals for each
MCA_tot = int(SMDB_MCA_unc['count'])
IMB_tot = int(SMDB_IMB_unc['count'])
MBA_tot = int(SMDB_MBA_unc['count'])
OMB_tot = int(SMDB_OMB_unc['count'])

if tweet_format == "short":

    f = open(fullpath_spec + 'Old_MCA.txt', 'r')
    Old_MCA = json.load(f)

    f = open(fullpath_spec + 'Old_IMB.txt', 'r')
    Old_IMB = json.load(f)

    f = open(fullpath_spec + 'Old_MBA.txt', 'r')
    Old_MBA = json.load(f)

    f = open(fullpath_spec + 'Old_OMB.txt', 'r')
    Old_OMB = json.load(f)

    num_disc_today = MCA_tot + IMB_tot + MBA_tot + OMB_tot - len(Old_MCA) - len(Old_IMB) - len(Old_MBA) - len(Old_OMB)

    day_add = [MCA_tot-len(Old_MCA), IMB_tot-len(Old_IMB), MBA_tot-len(Old_MBA), OMB_tot-len(Old_OMB)]

    hist = open(fullpath_spec + "AstList.csv", "r+")
    # CSV file with total number for day and last known asteroid
    hist_csv = csv.reader(hist, delimiter=',')
    WTD = []
    YTD = []
    for row in hist_csv:
        YTD.append(int(row[1]))
        WTD.append(int(row[2]))

    for i in range(0, len(WTD)):
        WTD[i] = WTD[i] + day_add[i]
        YTD[i] = YTD[i] + day_add[i]

    if num_disc_today == 0:
        tweet = "Yesterday, " + str(today.month) + "/" + str(today.day-1) + "/" + str(today.year) + ", there were no main-belt asteroids added to the small body database - check back again tomorrow!"
    elif num_disc_today == 1:
        tweet = "Yesterday there was " + str(num_disc_today) + " main-belt asteroid discovered/categorized: \n"
    else:
        tweet = "Yesterday there were " + str(num_disc_today) + " main-belt asteroids discovered/categorized: \n"

    def add_num_to_tweet(Cat, tot, tweet):
        tweet = tweet + Cat + ": " + str(tot) + "\n"
        return tweet
    
    for i in range(0, cat_nums):
        if day_add[i] != 0:
            tweet = add_num_to_tweet(category[i], day_add[i], tweet)

    # tweet = tweet + "Check out the full list here: https://ssd.jpl.nasa.gov/sbdb_query.cgi"

    send_it(tweet)

    # Get new names from pulled data for the local database update:
    MCA_names = [None]*MCA_tot
    for i in range(0, int(SMDB_MCA_unc['count'])):
        MCA_names[i] = SMDB_MCA_unc['data'][i][1]

    IMB_names = [None]*IMB_tot
    for i in range(0, int(SMDB_IMB_unc['count'])):
        IMB_names[i] = SMDB_IMB_unc['data'][i][1]

    MBA_names = [None]*MBA_tot
    for i in range(0, int(SMDB_MBA_unc['count'])):
        MBA_names[i] = SMDB_MBA_unc['data'][i][1]

    OMB_names = [None]*OMB_tot
    for i in range(0, int(SMDB_OMB_unc['count'])):
        OMB_names[i] = SMDB_OMB_unc['data'][i][1]

else:

    # Get new names from pulled data:
    MCA_names = [None]*MCA_tot
    for i in range(0, int(SMDB_MCA_unc['count'])):
        MCA_names[i] = SMDB_MCA_unc['data'][i][1]

    IMB_names = [None]*IMB_tot
    for i in range(0, int(SMDB_IMB_unc['count'])):
        IMB_names[i] = SMDB_IMB_unc['data'][i][1]

    MBA_names = [None]*MBA_tot
    for i in range(0, int(SMDB_MBA_unc['count'])):
        MBA_names[i] = SMDB_MBA_unc['data'][i][1]

    OMB_names = [None]*OMB_tot
    for i in range(0, int(SMDB_OMB_unc['count'])):
        OMB_names[i] = SMDB_OMB_unc['data'][i][1]

    # Open lists with the old names:
    f = open(fullpath_spec + 'Old_MCA.txt', 'r')
    Old_MCA = json.load(f)

    f = open(fullpath_spec + 'Old_IMB.txt', 'r')
    Old_IMB = json.load(f)

    f = open(fullpath_spec + 'Old_MBA.txt', 'r')
    Old_MBA = json.load(f)

    f = open(fullpath_spec + 'Old_OMB.txt', 'r')
    Old_OMB = json.load(f)


    # Initialize the new name vectors:
    new_MCA_names = [None]*abs(len(MCA_names) - len(Old_MCA))
    new_IMB_names = [None]*abs(len(IMB_names) - len(Old_IMB))
    new_MBA_names = [None]*abs(len(MBA_names) - len(Old_MBA))
    new_OMB_names = [None]*abs(len(OMB_names) - len(Old_OMB))


    # Compare the two lists for differences:
    def getNewNames(old_mat,  new_mat, toBeAppended, tot, barStr):
        # Create a new name file to return for each category
        k = 0
        with alive_bar(tot, spinner = 'wait3', bar = 'filling', title = 'Checking for new ' + barStr + ' names', force_tty = True) as bar: #Progress bar initiation - bar = 'classic3' also good
            for i in new_mat:
                if i not in old_mat:  # Found a missing one
                    if k >= abs(len(old_mat) - len(new_mat)):  # Asteroid recategorization has occured
                        toBeAppended.append(i)
                    else:
                        toBeAppended[k] = i
                        k = k + 1
                bar() #Update waitbar
        return toBeAppended


    new_MCA_names = getNewNames(Old_MCA,  MCA_names, new_MCA_names, MCA_tot, "MCA")
    new_IMB_names = getNewNames(Old_IMB,  IMB_names, new_IMB_names, IMB_tot, "IMB")
    new_MBA_names = getNewNames(Old_MBA,  MBA_names, new_MBA_names, MBA_tot, "MBA")
    new_OMB_names = getNewNames(Old_OMB,  OMB_names, new_OMB_names, OMB_tot, "OMB")


    def addNamesToTweet(name_list, twit, strName):
        if name_list == [None]:
            return
        elif len(name_list) > 1:
            twit = twit + "\n" + strName + ": "
            for i in name_list:
                if i == name_list[-1]:
                    twit = twit + i 
                else:
                    twit = twit + i + ", "
        elif len(name_list) == 1 and name_list[0] != None:
            twit = twit + "\n" + strName + ": "
            twit = twit + name_list[0]
            
        return twit


    num_disc_today = len(new_MCA_names) + len(new_IMB_names) + len(new_MBA_names) + len(new_OMB_names)
    day_add = [len(new_MCA_names), len(new_IMB_names), len(new_MBA_names), len(new_OMB_names)]

    hist = open(fullpath_spec + "AstList.csv", "r+")
    # CSV file with total number for day and last known asteroid
    hist_csv = csv.reader(hist, delimiter=',')
    WTD = []
    YTD = []
    for row in hist_csv:
        YTD.append(int(row[1]))
        WTD.append(int(row[2]))

    for i in range(0, len(WTD)):
        WTD[i] = WTD[i] + day_add[i]
        YTD[i] = YTD[i] + day_add[i]

    if num_disc_today == 0:
        tweet = "Yesterday, " + str(today.month) + "/" + str(today.day-1) + "/" + str(today.year) + ", there were no asteroids added to the small body database - check back again tomorrow!"
    elif num_disc_today == 1:
        tweet = "Yesterday there was " + str(num_disc_today) + " Main-Belt asteroid discovered/categorized:"
    else:
        tweet = "Yesterday there were " + str(num_disc_today) + " Main-Belt asteroids discovered/categorized:"

    if num_disc_today <= 20:
        tweet = addNamesToTweet(new_MCA_names, tweet, "MCA")
        tweet = addNamesToTweet(new_IMB_names, tweet, "IMB")
        tweet = addNamesToTweet(new_MBA_names, tweet, "MBA")
        tweet = addNamesToTweet(new_OMB_names, tweet, "OMB")


    def ReplyNamesToTweet(name_list, strName, t_ID):

        temp_list = name_list

        # Max number of asteroids in one tweet should be 25 for reliability maybe?
        max_per = 25

        while len(temp_list) > 0:  # While there are asteroids to still post about
            twit = strName + ": "
            if len(temp_list) < max_per:  # This will be the last tweet to go in the pile - let it rip

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

                        if i == temp_list[-1] or num == 25:
                            twit = twit + i 
                            # temp_list.remove(i)
                        else:
                            twit = twit + i + ", "  
                            # temp_list.remove(i)

                temp_list[0:max_per] = []

            if len(twit) != 0:
                twitter.update_status(status = twit, in_reply_to_status_id = t_ID , auto_populate_reply_metadata = True)
                # print(twit)

        # if len(name_list) > 0:
        #     twit = strName + ": "
        #     for i in name_list:
        #         if i == name_list[-1]:
        #             twit = twit + i 
        #         else:
        #             twit = twit + i + ", "
        # if len(twit) != 0:
        #     # twitter.update_status(status = twit, in_reply_to_status_id = t_ID , auto_populate_reply_metadata = True)
        #     print(twit)


    if num_disc_today > 20:  # tweet is too long, break all down into subreplies:

        tweet = "Since the last update tweet, there were " + str(num_disc_today) + " near Earth asteroids discovered/categorized:"  # Initial tweet 
        send_it(tweet)

        user_timeline = twitter.get_user_timeline(screen_name="MBA_Updates", count=1)
        twitter_ID = user_timeline[0]["id"]
        # twitter_ID = 1

        ReplyNamesToTweet(new_OMB_names, "OMB", twitter_ID)
        ReplyNamesToTweet(new_MBA_names, "MBA", twitter_ID)
        ReplyNamesToTweet(new_IMB_names, "IMB", twitter_ID)
        ReplyNamesToTweet(new_MCA_names, "MCA", twitter_ID)
        
    else:
        send_it(tweet)

# if date.today().weekday() == 6:  # It's sunday - it's also time for a wrapup
#     tweet_week = " \n It's sunday and also time for your weekly near-Earth asteroid wrapup. "
#     num_disc_week = sum(WTD)
#     if num_disc_week == 0:
#         tweet_week = tweet_week + "No new asteroids were discovered this week, we'll get 'em next time!"
#     elif num_disc_week == 1:
#         tweet_week = tweet_week + str(num_disc_week) + " new asteroid was discovered this week!"
#     else:
#         tweet_week = tweet_week + str(num_disc_week) + " new asteroids were discovered this week!"
#     # Now reset weekly counter
#     WTD = [0, 0, 0, 0]
#     send_it(tweet_week)


if today.month == 1 and today.day == 1:  # Happy new year 
    tweet = "Happy new year! As of today, the near-Earth asteroid totals are: \n"
    tweet = tweet + "MCAs: " + str(MCA_tot) + " - Discovered last year: " + str(YTD[0]) + "\n"
    tweet = tweet + "IMBs: " + str(IMB_tot) + " - Discovered last year: " + str(YTD[1]) + "\n"
    tweet = tweet + "MBAs: " + str(MBA_tot) + " - Discovered last year: " + str(YTD[2]) + "\n"
    tweet = tweet + "OMBs: " + str(OMB_tot) + " - Discovered last year: " + str(YTD[3])
    send_it(tweet)
    # Now reset year counter
    YTD = [0, 0, 0, 0]


w_CSV = open(fullpath_spec + "MBAList.csv", 'w', newline='')
wrtr = csv.writer(w_CSV)

wrtr.writerow([MCA_tot, YTD[0], WTD[0]])
wrtr.writerow([IMB_tot, YTD[1], WTD[1]])
wrtr.writerow([MBA_tot, YTD[2], WTD[2]])
wrtr.writerow([OMB_tot, YTD[3], WTD[3]])

# Write new corner files:
# Store the new lists for tomorrow:
with open(fullpath_spec + 'Old_MCA.txt', 'w') as filehandle:
    # store the data as binary data stream
    json.dump(MCA_names, filehandle)

with open(fullpath_spec + 'Old_IMB.txt', 'w') as filehandle:
    # store the data as binary data stream
    json.dump(IMB_names, filehandle)

with open(fullpath_spec + 'Old_MBA.txt', 'w') as filehandle:
    # store the data as binary data stream
    json.dump(MBA_names, filehandle)

with open(fullpath_spec + 'Old_OMB.txt', 'w') as filehandle:
    # store the data as binary data stream
    json.dump(OMB_names, filehandle)
 