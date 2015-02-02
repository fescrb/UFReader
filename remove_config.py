#!/user/bin/python3

# Utility to remove the config file directory for UFReader, QOL script whilst in 
# development for testing purposes

import ufconfig
import os.path
import shutil

if os.path.isdir(ufconfig.config_file_directory):
  shutil.rmtree(ufconfig.config_file_directory)

