'''
Documentation, License etc.

@package ufreader
'''

import ufmodel
import ufcontroller
import ufview

def main():
  model = ufmodel.UFModel()
  controller = ufcontroller.UFController(model)
  main_win = ufview.UFReaderWindow(model, controller)
  main_win.show_all()
  ufview.run()

if __name__ == "__main__":
  main()