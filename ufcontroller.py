import ufmodel
import ufconfig

class UFController():
  def __init__(self,model, config):
    self.model = model
    self.config = config
    self.current_subscription = None
    self.current_content = None
    #self.select_subscription(model.subscriptions[0], None)
    
    
  def select_subscription(self, subscription, subscription_view):
    subscription.load_content()
    self.current_subscription = subscription
    if subscription_view != None:
      subscription_view.update(subscription.content_list)
    
  def select_content(self, content_item, content_view):
    if self.config.get_mark_read_on_close() and self.current_content != None:
      self.current_content.mark_read()
    self.current_content = content_item
    if content_item != None:
      if self.config.get_mark_read_on_open():
	self.current_content.mark_read()
      content_view.set_text(content_item.text)