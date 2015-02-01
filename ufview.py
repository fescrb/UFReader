import gi
gi.require_version("WebKit", "3.0")
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Pango
from gi.repository import WebKit

import ufmodel

# Magic numbers, sorry
def get_bold_value(unread):
  if unread:
    return Pango.Weight.BOLD # BOLD
  else:
    return Pango.Weight.NORMAL # NOT BOLD

class UFContentView(WebKit.WebView):
  def __init__(self):
      WebKit.WebView.__init__(self)
      
  def set_text(self, text):
    self.load_html_string(text, "")

class UFContentListView(Gtk.TreeView):
  def __init__(self, content_view, controller):
    self.content_view = content_view
    self.controller = controller
    # Column 1 has the title, column 2 has a reference to the model object, column 3 has the text weight (bold/notbold)
    self.contentstore = Gtk.ListStore(str, GObject.TYPE_PYOBJECT, int)
    Gtk.TreeView.__init__(self,self.contentstore)
    renderer = Gtk.CellRendererText()
    #renderer.set_property("weight", 700)
    title_column = Gtk.TreeViewColumn("Articles", renderer, text=0)
    title_column.add_attribute(renderer, "weight", 2)
    self.append_column(title_column)
    select = self.get_selection()
    select.connect("changed", self.on_selection_changed)
    self.prev_selection = None
    
  def update(self, contentList):
    self.contentstore.clear()
    for content_item in contentList:
      self.contentstore.append([content_item.label, content_item, get_bold_value(content_item.unread)])
    self.queue_draw()
    
  def on_selection_changed(self, selection):
    store, iter = selection.get_selected()
    if iter != None:
      print(store[iter][0] + " selected. Content id " + store[iter][1].id)
      self.controller.select_content(content_item=store[iter][1], content_view=self.content_view)
    else:
      print("Iter is none.")
    # I'd like this to be done by the controller
    if self.prev_selection != None:
      store[self.prev_selection][2] = get_bold_value(store[self.prev_selection][1].unread)
    store[iter][2] = get_bold_value(store[iter][1].unread)
    self.prev_selection = iter

class UFSubscriptionListView(Gtk.TreeView):
  def __init__(self, subscriptions, content_list_view, controller):
    self.content_list_view = content_list_view
    self.controller = controller
    self.substore = Gtk.ListStore(str, GObject.TYPE_PYOBJECT)
    for sub in subscriptions:
      self.substore.append([sub.label, sub])
    Gtk.TreeView.__init__(self,self.substore)
    self.renderer = Gtk.CellRendererText()
    self.column = Gtk.TreeViewColumn("Subscriptions", self.renderer, text=0)
    self.append_column(self.column)
    select = self.get_selection()
    select.connect("changed", self.on_selection_changed, )
    
  def on_selection_changed(self, selection):
    mod, iter = selection.get_selected()
    if iter != None:
      print(mod[iter][0] + " selected. Sub id " + mod[iter][1].id)
      self.controller.select_subscription(mod[iter][1], self.content_list_view)
    else:
      print("Iter is none.")
      
class UFOptionsWindow(Gtk.Window):
  def __init__(self, controller):
    Gtk.Window.__init__(self)
    self.set_title("UFReader Options")
    radiobutton = Gtk.RadioButton()
    radiobutton.set_label("Things")
    self.add(radiobutton)
      
class UFToolbar(Gtk.Toolbar):
  def __init__(self, controller):
    Gtk.Toolbar.__init__(self)
    self.set_size_request(-1, 60)
    self.controller = controller
    
    #Mark as read
    mark_as_read = Gtk.ToolButton(icon_widget=None, label="Mark As Read")
    self.insert(item=mark_as_read, pos=-1) #Negative numbers for pos append to the end of the bar
    
    #Save for later
    save_for_later = Gtk.ToolButton(icon_widget=None, label="Save For Later")
    self.insert(item=save_for_later, pos=-1)
    
    #Separator
    separator = Gtk.SeparatorToolItem()
    self.insert(item=separator, pos=-1)
    
    #Options
    options = Gtk.ToolButton(label="Options")
    #options.set_tooltips(<tooltip_object>, tip_text="Displays the options window.", tip_private="Private")
    options.connect("clicked", self.open_options_window)
    self.insert(item=options, pos=-1)
    self.options_window = None
    
  def open_options_window(self, event):
    if self.options_window is None:
      self.options_window = UFOptionsWindow(self.controller)
      self.options_window.connect("delete-event", self.close_options_window)
    self.options_window.present()
    
  def close_options_window(self, event, data):
    self.options_window = None

class UFReaderWindow(Gtk.Window):
  def __init__(self, model, config, controller):
    #Initialize self
    Gtk.Window.__init__(self)
    self.controller = controller
    self.set_title("UFReader")
    self.set_default_size(width=600,height=400)
    
    #Initialize sub-widgets
    self.content_view = UFContentView()
    self.content_list_view = UFContentListView(self.content_view, controller)
    self.subcription_view = UFSubscriptionListView(model.subscriptions,self.content_list_view, controller)
    
    # Setup scrollers
    scroller_for_content_view = Gtk.ScrolledWindow()
    scroller_for_content_view.add(self.content_view)
    scroller_for_content_list_view = Gtk.ScrolledWindow()
    scroller_for_content_list_view.set_size_request(-1,200)	
    scroller_for_content_list_view.add(self.content_list_view)
    scroller_for_subscription_view = Gtk.ScrolledWindow()
    scroller_for_subscription_view.set_size_request(100,-1)
    scroller_for_subscription_view.add(self.subcription_view)
    
    #Setup toolbar
    toolbar = UFToolbar(controller)
    
    top_pane = Gtk.HPaned()
    top_pane.add1(scroller_for_subscription_view)
    right_pane = Gtk.VPaned()
    right_pane.add1(scroller_for_content_list_view)
    right_pane.add2(scroller_for_content_view)
    top_pane.add2(right_pane)
    top_box = Gtk.VBox()
    top_box.pack_start(toolbar, False, False, 0)
    top_box.pack_start(top_pane, True, True, 0)
    self.add(top_box)
    self.connect("delete-event", self.shutdown)
    
  def shutdown(self, event, data):
    self.controller.shutdown()
    Gtk.main_quit()
      
def run():
  Gtk.main()