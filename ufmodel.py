from feedly_client import client
import json

userdatafile = open("user.json")
ufclient=client.FeedlyClient(client="", client_secret="", sandbox=False, token=json.load(userdatafile)['token'])
userdatafile.close()

class UFContentItem():
  def __init__(self,data):
    #print data['title']
    #for key in data.keys():
    #print data.keys()
    #print data['visual']
    #print "Summary: " + data['summary']['content']
    #print "Content: " + data['content']['content']
    self.label = data['title']
    self.id = data['id']
    if "content" in data.keys():
      self.text = data['content']
    else:
      self.text = data['summary']
    
  def mark_read(self):
    ufclient.mark_article_read(ufclient.token, self.id)

class UFSubscription():
  def __init__(self, data):
    self.label = data['title']
    self.id = data['id']
    self.content_list = []
    
  def load_content(self):
    content_items = ufclient.get_feed_content(ufclient.token, self.id, False, 0)['items']
    #print content_items
    for item in content_items:
      self.content_list.append(UFContentItem(item))

class UFModel():
  def __init__(self):
    self.subscriptions = []
    self.load_subscriptions()
    #print ufclient.token
    #print ufclient.get_user_subscriptions(ufclient.token)[0]
    
  def load_subscriptions(self):
    subscriptions = ufclient.get_user_subscriptions(ufclient.token)
    for sub in subscriptions:
      self.subscriptions.append(UFSubscription(sub))