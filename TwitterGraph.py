import tweepy
import sys
import networkx as nx
from time import sleep
import matplotlib.pyplot as plt


class Twitter:
    def __init__(self, cfg=None):
        if cfg is None:
            cfg = {
                "consumer_key": "UDKklpVFJbjnrIeBbwyrwXw9F",
                "consumer_secret": "02aJXtk4OnxwTBLQ3h5ZsmHCj4N6BllC5qn8yQwAOlfc1PBHP4",
                "access_token": "804265252221308928-vQhGbdrjvt3mqNZD2X8GaZ5U4f1jIZZ",
                "access_token_secret": "MjNpV4fVRhV5Ag1nByRNhw9H4j5TXAys5REV7KwyzcsIl"
            }
        else:
            cfg = {
                "consumer_key": cfg["consumer_key"],
                "consumer_secret": cfg["consumer_secret"],
                "access_token": cfg["access_token"],
                "access_token_secret": cfg["access_token_secret"]
            }

        auth = tweepy.OAuthHandler(cfg["consumer_key"], cfg["consumer_secret"])
        auth.set_access_token(cfg["access_token"], cfg["access_token_secret"])
        self.api = tweepy.API(auth)

    def get_followers(self, user_id=None):
        if user_id is None:
            return tweepy.Cursor(self.api.followers_ids).items()
        else:
            return tweepy.Cursor(self.api.followers_ids, id=user_id).items()

    def build_graph(self, origin_user_id=None):
        graph = nx.Graph()
        graph.add_node(origin_user_id,id=origin_user_id)
        visited = [origin_user_id]
        for now_id in visited:
            followers = self.get_followers(now_id)
            i = 0
            while True:
                try:
                    follower_id = followers.next()
                    i+=1
                    if follower_id not in visited:
                        visited.append(follower_id)
                    if follower_id not in graph.neighbors(now_id):
                        graph.add_node(follower_id)
                        graph.add_edge(now_id,follower_id)
                    # test with a small graph, limiting just to 10 friends each node
                    if i >= 10:
                        break
                except tweepy.TweepError:
                    print("Rate limited. Sleeping for 15 minutes.")
                    sleep(15 * (60))
                    continue
                except StopIteration:
                    break
            plt.clf()
            pos = nx.spring_layout(graph)
            nx.draw_networkx_nodes(graph, pos)
            nx.draw_networkx_edges(graph, pos)
            plt.draw()
            plt.pause(0.5)
        return graph


def main():
    # Receives a username as argument
    user_name = sys.argv[1]
    twitter = Twitter()
    user_id = twitter.api.get_user(user_name).id
    graph = twitter.build_graph(user_id)

if __name__ == "__main__":
    main()