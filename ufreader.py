'''
Documentation, License etc.

@package ufreader
'''

import ufmodel
import ufconfig
import ufcontroller
import ufview

def main():
  model = ufmodel.UFModel()
  config = ufconfig.UFConfig()
  controller = ufcontroller.UFController(model, config)
  main_win = ufview.UFReaderWindow(model, config, controller)
  main_win.show_all()
  ufview.run()

if __name__ == "__main__":
  main()