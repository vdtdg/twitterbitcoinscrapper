import os
import tweepy
import re

# Approx. des limites de l'api:
#  450 requests /  15 min
# 37.5 requests /   1 min
#    1 request  / 1.6 sec

#  GLOBAL VAR
PATH_DATA = ""
PATH_ACCESS = ""
if os.name == "nt":
    PATH_DATA = os.getcwd() + "\\..\\data\\"
elif os.name == "posix":
    PATH_DATA = os.getcwd() + "/../data/"
if os.name == "nt":
    PATH_ACCESS = os.getcwd() + "\\..\\access\\"
elif os.name == "posix":
    PATH_ACCESS = os.getcwd() + "/../access/"
with open(PATH_ACCESS + "Access_Token.txt", "r") as access_token_file:
    ACCESS_TOKEN = access_token_file.read()
with open(PATH_ACCESS + "Access_Token_Secret.txt", "r") as access_token_secret_file:
    ACCESS_TOKEN_SECRET = access_token_secret_file.read()
with open(PATH_ACCESS + "Consumer_key.txt", "r") as consumer_key_file:
    CONSUMER_KEY = consumer_key_file.read()
with open(PATH_ACCESS + "Consumer_secret.txt", "r") as consumer_secret_key_file:
    CONSUMER_SECRET = consumer_secret_key_file.read()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# En fonction de l'offre que l'on a, les limites de l'API sont différentes
# On récupère donc les valeurs limites des endpoints qui nous intéressent.
max_get_followers = 0
max_get_user_timeline = 0
rls = api.rate_limit_status()
if rls is not None:
    max_get_followers = rls['resources']['followers']['/followers/list']['limit']
    max_get_user_timeline = rls['resources']['statuses']['/statuses/user_timeline']['limit']


# Définition des valeurs par défaut
nb_objectif = 10
nb = 0
user_dict = dict()
users_to_do = []


# Transforme l'objet User en un dict intéressant pour nous
def user_to_dict(user):
    my_dict = dict()
    if user is not None:
        my_dict['description'] = user.description
        my_dict['followers_count'] = user.followers_count
        my_dict['id'] = user.id_str
        my_dict['location'] = user.location
        my_dict['name'] = user.name
        my_dict['screen_name'] = user.screen_name
        my_dict['time_zone'] = user.time_zone
        my_dict['url'] = user.url
    return my_dict


# Rajoute un utilisateur dans le json avec son adresse associée
# Vérifie si il y avait déjà quelque chose à cette adresse et update dans ce cas
def add_to_user_dict(addr, usr):
    if addr in user_dict:
        user_dict[addr] = user_to_dict(usr)
        return 1
    else:
        user_dict[addr] = user_to_dict(usr)
        return 2


# Vérifie que le message n'est pas un RT
# Cherche dans le message une adresse bitcoin et la retourne
def check(text):
    if not re.match("RT", text):
        exp = re.compile(r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}')
        return exp.search(text)
    else:
        return None


# On récupere une liste de max_get_followers tweets (parce qu'on est limité par cette valeur)
# Ces tweets possède des mots clés comme "bitcoin" et "address".
# On regarde s'il y a une adresse dans le tweet, puis on l'associe avec son utilisateur.
# Ces utilisateurs sont donc des utilisateurs de Bitcoin, ils ont probablement des followers qui les suit pour ça.
# On fait donc de même avec les followers de ces utilisateurs, dans la limites du nombre d'appel de l'API twitter.
tweets = api.search("my bitcoin address", tweet_mode='extended', count=max_get_followers)
if tweets:
    for tweet in tweets:
        if nb < nb_objectif:
            adr = check(tweet.full_text)
            u = tweet.user
            if adr:
                ret = add_to_user_dict(adr.group(0), u)
                if ret:
                    nb += 1
            followers = u.followers()
            for follower in followers:
                users_to_do.append(follower)
        else:
            break

if users_to_do:
    for user in users_to_do[:max_get_user_timeline-max_get_followers-1]:
        try:
            user_tweets = user.timeline(tweet_mode='extended')
        except tweepy.TweepError:
            print("Could not get timeline of that user, skipping...")
            user_tweets = None
        if user_tweets:
            for tw in user_tweets:
                adr = check(tw.full_text)
                if adr:
                    ret = add_to_user_dict(adr.group(0), user)
                    if ret:
                        nb += 1
                    break


# Affichage de nos découvertes.
print("On été découvert : " + str(len(user_dict)) + " couples utilisateurs / adresses BTC.")
print("Les voici :")
print(user_dict)

print("\nUn maximum de " + str(max_get_user_timeline) + " users ont été scannés.")
print("Les " + str(len(users_to_do)) + " followers suivants ont été scannés :")
print(users_to_do)
