import requests
import json
import time

#its bad practice to place your bearer token directly into the script (this is just done for illustration purposes)

BEARER_TOKEN = ""
#define search twitter function
def search_twitter(user, next_token, bearer_token = BEARER_TOKEN):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    if next_token is not None:
        url = "https://api.twitter.com/2/users/{}/liked_tweets?pagination_token={}".format(user,next_token)
    else:
        url = "https://api.twitter.com/2/users/{}/liked_tweets".format(user)
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def also_search_twitter(user, bearer_token = BEARER_TOKEN):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/users/{}?user.fields=created_at,description,id,verified,public_metrics".format(user)
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


user_list = [50393960,
             44196397,
             813286,
             428333,
             5402612,
             1367531,
             783214,
             19663706,
             38612007,
             35787166,
             826065164504006657,
             27948977,
             40891771,
             1289910485685501952]
user_list = [str(x) for x in user_list]

info_user_list =[]
like_list = []
for user in user_list:
    next_token = None
    likes = 0
    json_response = search_twitter(user, next_token, bearer_token=BEARER_TOKEN)
    likes = likes + json_response["meta"]["result_count"]
    try:
        next_token = json_response["meta"]["next_token"]
    except KeyError:
        pass
    while next_token is not None:
        time.sleep(1)
        try:
            json_response = search_twitter(user, next_token, bearer_token=BEARER_TOKEN)
            likes = likes + json_response["meta"]["result_count"]
            next_token = json_response["meta"]["next_token"]
        except KeyError:
            print("Keyerror")
            break
        #print(next_token)
        #print("next_token" in json_response["meta"])
        #if "next_token" in json_response["meta"]:
            #print(next_token)
            #json_response = search_twitter(user, next_token, bearer_token=BEARER_TOKEN)
            #likes = likes + json_response["meta"]["result_count"]
            #next_token = json_response["meta"]["next_token"]
        #else:
        #    next_token = None
    like_list.append(likes)
    also_json_response = also_search_twitter(user, bearer_token=BEARER_TOKEN)
    print(also_json_response)

    #['verified',
    #'register_time',
    #'status_count',
    #'favourites_count',
    #'followers_count',
    #'friend_count',
    #'male', 'female',
    #'age_1', 'age_2', 'age_3', 'age_4',
    #'org_1', 'org_2',
    #'B']

    info_user_list.append([also_json_response["data"]["verified"],
                           also_json_response["data"]["created_at"],
                           also_json_response["data"]["public_metrics"]["tweet_count"],
                           likes,
                           also_json_response["data"]["public_metrics"]["followers_count"],
                           also_json_response["data"]["public_metrics"]["following_count"],
                           "gender",
                           "age",
                           "org"])

    print(info_user_list)
print(info_user_list)


'''
@billgates => 50393960
@elonmusk => 44196397
@barackobama => 813286
@cnnbrk => 428333
@bbcbreaking => 5402612
@foxnews => 1367531
@twitter => 783214
@sweden => 19663706
@chaser => 38612007
@nickiminaj => 35787166
@mtgreenee => 826065164504006657
@kenglueck => 27948977
@whitlockjason => 40891771
@leehurstcomic => 1289910485685501952
'''

