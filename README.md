# Bitcointalk scrapper

## What is this ?
This script produces a JSON file in the ``data/`` folder.  
This file contains data on Twitter users.  
More precisely, it gets the data of a user if this user have twitted its bitcoin address.  

The JSON file have this structure :   
`` {   
      'bitcoin_address' : { 'Name': 'your_name', 'Age': 'your_age', ... },  
      ...  
   }  
``  


## Getting started

### Prerequisites

This is a Python 3 script.  
`` sudo apt-get install python3.6 ``  
  
So you need Python 3, but also tweepy  
`` pip install tweepy``

In order to user the Twitter API, you need access tokens from Twitter.  
More informations here : https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html    

In the ``access/`` folder, you just have to past each token into each corresponding name file.   
Do not rename files.
 
### Installation
Just clone this repository.  
`` git clone https://github.com/vdtdg/twitterbitcoinscrapper.git``

### How to use
Launch it by command line **directly in the folder src**  
`` python3 script.py``  
**Don't**  
`` python3 src/script.py``  

The script is just a draft of what can be done with the twitter API within the limitation of the free API.


## Authors
Valérian de THEZAN de GAUSSAN  
Université Claude Bernard Lyon 1
