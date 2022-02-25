import os
import glob

files = glob.glob('./backblaze_data/unzipped/**/*.csv', recursive=True)

with open('custom_import.sql', 'w+') as outfile:
	outfile.write('.mode csv\n.echo on\n')
	for file in files:
		outfile.write(f'.import {file} drive_stats\n')

	outfile.write('.echo off\n.mode list\nDELETE FROM drive_stats WHERE model = \'model\';')