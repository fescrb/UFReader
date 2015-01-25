import ufmodel

class UFController():
  def __init__(self,model):
    self.model = model
    self.select_subscription(model.subscriptions[0], None)
    
    
  def select_subscription(self, subscription, subscription_view):
    subscription.load_content()
    self.current_substriction = subscription
    if subscription_view != None:
      subscription_view.update(subscription.content_list)
    
    