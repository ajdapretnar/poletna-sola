import twitter
import networkx as nx

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
t = twitter.Twitter(auth=auth)

followers_graph = nx.Graph()
following_graph = nx.Graph()
all = nx.Graph()

#Dopisi uporabniska imena
users = []

for user in users:
    result = t.users.show(screen_name=user)
    id = result["id"]
    followers_graph.add_node(id)
    followers = []
    following_graph.add_node(id)
    following = []
    all.add_node(id)
    cursor = -1
    while cursor != 0:
        response = t.followers.ids(screen_name=user, cursor=cursor)
        followers.extend(response['ids'])
        cursor = response['next_cursor']
    for f_id in followers:
        followers_graph.add_edge(id, f_id)
        all.add_edge(id, f_id)
    cursor = -1
    while cursor != 0:
        response = t.friends.ids(screen_name=user, cursor=cursor)
        following.extend(response['ids'])
        cursor = response['next_cursor']
    for f_id in following:
        following_graph.add_edge(id, f_id)
        all.add_edge(id, f_id)


nx.write_gml(followers_graph, "followers.gml")
nx.write_gml(following_graph, "following.gml")
nx.write_gml(all, "all.gml")