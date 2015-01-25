from gi.repository import Gtk
from gi.repository import GObject

import ufmodel

#class UFSubscriptionView(Gtk

class UFContentListView(Gtk.TreeView):
  def __init__(self):
    self.contentstore = Gtk.ListStore(str, GObject.TYPE_PYOBJECT)
    Gtk.TreeView.__init__(self,self.contentstore)
    self.renderer = Gtk.CellRendererText()
    self.column = Gtk.TreeViewColumn("Articles", self.renderer, text=0)
    self.append_column(self.column)
    select = self.get_selection()
    select.connect("changed", self.on_selection_changed)
    
  def update(self, contentList):
    self.contentstore.clear()
    for content_item in contentList:
      self.contentstore.append([content_item.label, content_item])
    self.queue_draw()
    
    
    
  def on_selection_changed(self, selection):
    mod, iter = selection.get_selected()
    if iter != None:
      print mod[iter][0] + " selected. Content id " + mod[iter][1].id
    else:
      print "Iter is none."

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
      print mod[iter][0] + " selected. Sub id " + mod[iter][1].id
      self.controller.select_subscription(mod[iter][1], self.content_list_view)
    else:
      print "Iter is none."

class UFReaderWindow(Gtk.Window):
  def __init__(self, model, controller):
      Gtk.Window.__init__(self, title="UFReader")
      self.content_view = UFContentListView()
      self.subcription_view = UFSubscriptionListView(model.subscriptions,self.content_view, controller)
      top_pane = Gtk.HPaned()
      top_pane.add1(self.subcription_view)
      top_pane.add2(self.content_view)
      self.add(top_pane)
      self.connect("delete-event", Gtk.main_quit)
    
def run():
  Gtk.main()