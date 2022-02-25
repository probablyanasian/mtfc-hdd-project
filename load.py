import os
import glob

files = glob.glob('./backblaze_data/unzipped/**/*.csv', recursive=True)

print(files)