# CNEOS NHATS AsteroidComparison Chart

Author: Charlie Hanner - 2022

 This is a repository for public release of the Python code generated to automatically tweet numbers of asteroids discovered every day. This release is under the CRAPL license as I wanted to make sure this code, while written for personal use and cannot guarantee anything, is available to the public. If you have any questions, please feel free to contact me!

The two accounts can be found at:
[https://twitter.com/AsteroidUpdates](https://twitter.com/AsteroidUpdates)
[https://twitter.com/MBA_Updates](https://twitter.com/AsteroidUpdates)


## Requirements

This code was written in Python 3.10.7, and uses the following libraries:
- requests
- csv
- json
- numpy
- platform
- datetime
- time
- twython

A set of local data files are required as well: 
- AstList.csv
- MBAList.csv
Then a series of local files for storing asteroid names that begin with Old_ with the following suffixes on the .txt files:
- AMO
- APO
- ATE
- IEO
- IMB
- MBA
- MCA
- OMB

Additionally a file called auth.py is required to store the Twitter API keys and tokens. This file is not included in the repository, but is required to run the code. The file should contain the following lines for each account:
- API_key
- API_secret
- bearer_token 
- token
- secret 

## Use
The batch file on the Raspberry Pi that runs these tweets uses the AsteroidUpdates.py and MBA_Updates.py files to generate the tweets. It runs the code for NEOs at 9:00 EST, and for MBAs at 9:05 EST. 
