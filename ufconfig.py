import json
import os.path

config_file_directory = os.path.expanduser("~/.config/ufreader/")
config_file_location = config_file_directory + "config.json"

class UFConfig(dict) :
  def __init__(self):
    # init defaults?
    if not os.path.isfile(config_file_location):
      if not os.path.isdir(config_file_directory):
        os.makedirs(config_file_directory)
      self.set_defaults()
      config_file = open(config_file_location, "w+")
      self.write_to_file(config_file)
    else:
      config_file = open(config_file_location, "r")
      self.load_from_file(config_file)
    config_file.close()
    
  # Full-config methods
  def set_defaults(self):
    self['mark_read_on_open'] = False
    self['mark_read_on_close'] = True
    
  def load_from_file(self, f):
    jsonfile = json.load(f)
    for key in jsonfile.keys():
      self[key] = jsonfile[key]
      
  def write_to_file(self, f):
    json.dump(self, f, indent = 4)
    
  def save_config(self):
    config_file = open(config_file_location, "w+")
    self.write_to_file(config_file)
    
  # Getters
  def get_mark_read_on_open(self):
    return self['mark_read_on_open']
  
  def get_mark_read_on_close(self):
    return self['mark_read_on_close']
  
  # Setters
  def set_mark_read_on_open(self, val):
    self['mark_read_on_open'] = val
    
  def set_mark_read_on_close(self, val):
    self['mark_read_on_close'] = val