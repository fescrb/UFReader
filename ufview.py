import gtk
import gobject
import webkit

import ufmodel

# Magic numbers, sorry
def get_bold_value(unread):
  if unread:
    return 700 # BOLD
  else:
    return 400 # NOT BOLD

class UFContentView(webkit.WebView):
  def __init__(self):
      webkit.WebView.__init__(self)
      
  def set_text(self, text):
    self.load_html_string(text, "")

class UFContentListView(gtk.TreeView):
  def __init__(self, content_view, controller):
    self.content_view = content_view
    self.controller = controller
    # Column 1 has the title, column 2 has a reference to the model object, column 3 has the text weight (bold/notbold)
    self.contentstore = gtk.ListStore(str, gobject.TYPE_PYOBJECT, int)
    gtk.TreeView.__init__(self,self.contentstore)
    renderer = gtk.CellRendererText()
    #renderer.set_property("weight", 700)
    title_column = gtk.TreeViewColumn("Articles", renderer, text=0)
    title_column.add_attribute(renderer, "weight", 2)
    self.append_column(title_column)
    select = self.get_selection()
    select.connect("changed", self.on_selection_changed)
    self.prev_selection = None
    
  def update(self, contentList):
    self.contentstore.clear()
    for content_item in contentList:
      self.contentstore.append([content_item.label, content_item], get_bold_value(content_item.unread))
    self.queue_draw()
    
  def on_selection_changed(self, selection):
    store, iter = selection.get_selected()
    if iter != None:
      print store[iter][0] + " selected. Content id " + store[iter][1].id
      self.controller.select_content(content_item=store[iter][1], content_view=self.content_view)
    else:
      print "Iter is none."
    # I'd like this to be done by the controller
    if self.prev_selection != None:
      store[self.prev_selection][2] = get_bold_value(store[self.prev_selection][1].unread)
    store[iter][2] = get_bold_value(store[iter][1].unread)
    self.prev_selection = iter

class UFSubscriptionListView(gtk.TreeView):
  def __init__(self, subscriptions, content_list_view, controller):
    self.content_list_view = content_list_view
    self.controller = controller
    self.substore = gtk.ListStore(str, gobject.TYPE_PYOBJECT)
    for sub in subscriptions:
      self.substore.append([sub.label, sub])
    gtk.TreeView.__init__(self,self.substore)
    self.renderer = gtk.CellRendererText()
    self.column = gtk.TreeViewColumn("Subscriptions", self.renderer, text=0)
    self.append_column(self.column)
    select = self.get_selection()
    select.connect("changed", self.on_selection_changed, )
    
  def on_selection_changed(self, selection):
    mod, iter = selection.get_selected()
    if iter != None:
      print mod[iter][0] + " selected. Sub id " + mod[iter][1].id
      self.controller.select_subscription(mod[iter][1], self.content_list_view)
    else:
      print "Iter is none."

class UFReaderWindow(gtk.Window):
  def __init__(self, model, config, controller):
    #Initialize self
    gtk.Window.__init__(self)
    self.set_title("UFReader")
    self.set_default_size(width=600,height=400)
    
    #Initialize sub-widgets
    self.content_view = UFContentView()
    self.content_list_view = UFContentListView(self.content_view, controller)
    self.subcription_view = UFSubscriptionListView(model.subscriptions,self.content_list_view, controller)
    
    # Setup scrollers
    scroller_for_content_view = gtk.ScrolledWindow()
    scroller_for_content_view.add(self.content_view)
    scroller_for_content_list_view = gtk.ScrolledWindow()
    scroller_for_content_list_view.set_size_request(-1,200)	
    scroller_for_content_list_view.add(self.content_list_view)
    scroller_for_subscription_view = gtk.ScrolledWindow()
    scroller_for_subscription_view.set_size_request(100,-1)
    scroller_for_subscription_view.add(self.subcription_view)
    
    
    top_pane = gtk.HPaned()
    top_pane.add1(scroller_for_subscription_view)
    right_pane = gtk.VPaned()
    right_pane.add1(scroller_for_content_list_view)
    right_pane.add2(scroller_for_content_view)
    top_pane.add2(right_pane)
    self.add(top_pane)
    self.connect("delete-event", gtk.main_quit)
      
def run():
  gtk.main()