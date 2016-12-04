import tweepy
from time import sleep

def main():
    cfg = {
        "consumer_key": "UDKklpVFJbjnrIeBbwyrwXw9F",
        "consumer_secret": "02aJXtk4OnxwTBLQ3h5ZsmHCj4N6BllC5qn8yQwAOlfc1PBHP4",
        "access_token": "804265252221308928-vQhGbdrjvt3mqNZD2X8GaZ5U4f1jIZZ",
        "access_token_secret": "MjNpV4fVRhV5Ag1nByRNhw9H4j5TXAys5REV7KwyzcsIl"
    }
    auth = tweepy.OAuthHandler(cfg["consumer_key"], cfg["consumer_secret"])
    auth.set_access_token(cfg["access_token"], cfg["access_token_secret"])
    api = tweepy.API(auth)

    me = api.me()

    print(me.created_at)
    #user = api.get_user("ichatzi")
    #print(user.id)
    #print(user.followers_count)
    #for friend in user.followers():
    #    print(friend.screen_name)

    #statuses = api.home_timeline()
    # for status in statuses:
    #     # process status here
    #     print(status.text)
    #     print(status.user.screen_name)
    #     print(status.created_at, "Fav: ",
    #           status.favorite_count)
    #     print("---")

    print("USERS")
    users = api.search_users("Sapienza",5)
    for user in users:
        print(user.id)

    last_user = api.get_user(user.id)
    print(last_user.screen_name)
    print("---")

    sapienza = api.get_user("SapienzaRoma")
    print("SapienzaRoma_ID = ", sapienza.id)

    # c = tweepy.Cursor(api.followers, id=sapienza.id).items(100)
    # while True:
    #     friend = c.next()
    #     print(friend.screen_name)

    # -----------------------------------------
    # -------------FOLLOWERS_ID----------------
    # -----------------------------------------

    test_user = api.get_user("fernandocremag")
    c = tweepy.Cursor(api.followers_ids, id=test_user.id).items()
    friends_id = []
    while True:
        try:
            friends_id.append(c.next())
        except tweepy.TweepError:
            print("Rate limited. Sleeping for 15 minutes.")
            sleep(15 * (60+1))
            continue
        except StopIteration:
            break
    print("Number of Fernando's followers: ", len(friends_id))
    print("There is no limit for getting the IDs, but a Rate Limit is reached when iterating over followers")

    flist = []
    for friend in tweepy.Cursor(api.followers_ids, id=test_user.id).items():
        flist.append(friend)

    batch = []
    while flist:
        batch.append(flist.pop())

        if len(batch) >= 100:
            print(batch)

            users = api.lookup_users(user_ids=batch)
            for u in users:
                print(u.screen_name)
            batch = []

    # Printing the remaining users
    users = api.lookup_users(user_ids=batch)
    for u in users:
        print(u.screen_name)
    print("END OF ALL BATCHES")



    # -----------------------------------------
    # -------FOLLOWERS AND RATE LIMIT----------
    # -----------------------------------------

    print("-----------------------------------")
    print("---Printing Sapienza's Followers---")
    print("-----------------------------------")
    test_user = api.get_user("SapienzaRoma")
    c = tweepy.Cursor(api.followers, id=test_user.id).items()
    followers = []
    while True:
        try:
            followers.append(c.next())
        except tweepy.TweepError:
            print("Rate limited. Sleeping for 15 minutes.")
            sleep(15 * (60))
            continue
        except StopIteration:
            break
    print(len(followers))




if __name__ == "__main__":
    main()