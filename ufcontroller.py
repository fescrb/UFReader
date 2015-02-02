import ufmodel
import ufconfig

class UFController():
  def __init__(self,model, config):
    self.model = model
    self.config = config
    self.current_subscription = None
    self.current_content = None
    self.updatable = None
    self.content_list_view = None
    #self.select_subscription(model.subscriptions[0], None)
    
  def set_updatable(self, updatable):
    self.updatable = updatable
    
  def set_content_list_view(self, content_list_view):
    self.content_list_view = content_list_view
    
  def select_subscription(self, subscription):
    subscription.load_content()
    self.current_subscription = subscription
    self.updatable.update()
    
  def select_content(self, content_item):
    if self.config.get_mark_read_on_close() and self.current_content != None:
      self.mark_current_read()
    self.current_content = content_item
    if content_item != None:
      if self.config.get_mark_read_on_open():
        self.mark_current_read()
    self.updatable.update()
      
  def mark_current_read(self):
    if self.current_content != None:
      self.current_content.mark_read()
      
  def save_config(self):
    self.config.save_config()