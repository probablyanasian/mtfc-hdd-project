import os
import glob

file_time = '2021' # DOES NOT WORK WITH 2018.
files = glob.glob(f'./backblaze_data/unzipped/**/*{file_time}*.csv', recursive=True)

with open(f'./imports/custom_import_{file_time}.sql', 'w+') as outfile:
	outfile.write('.mode csv\n.echo on\n')
	for file in files:
		outfile.write(f'.import {file} drive_stats_{file_time}\n')

	outfile.write(f'.echo off\n.mode list\nDELETE FROM drive_stats_{file_time} WHERE model = \'model\';')