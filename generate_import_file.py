import os
import glob

file_date = '2019_q1' # DOES NOT WORK WITH ANY YEAR WITH QUARTER DIFFS.
files = glob.glob(f'./backblaze_data/unzipped/**/data_Q1_2019/**/*.csv', recursive=True)

with open(f'./imports/custom_import_{file_date}.sql', 'w+') as outfile:
	outfile.write('.mode csv\n.echo on\n')
	for file in files:
		outfile.write(f'.import {file} drive_stats_{file_date}\n')

	outfile.write(f'.echo off\n.mode list\nDELETE FROM drive_stats_{file_date} WHERE model = \'model\';')