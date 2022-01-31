import os
import shutil
from datetime import datetime

def log(msg):
	global logfilepath
	with open(logfilepath, 'a') as f:
		f.write(str(msg) + '\n')
	print(msg)

def transfer(src, dst, exc):
	global logfilepath
	global logfolder

	# get current datetime for filename of log
	logfilepath = datetime.now().strftime("%m-%d-%Y_%H-%M-%S.txt")
	logfilepath = os.path.join(os.path.abspath(logfolder), logfilepath)

	log(f'INFO:\tLOGFILE AT {logfilepath}')

	# get all subdirectories in src and dst folders (first one removed bc it is just the toplevel dir)
	src_subdirs = list(filter(lambda x: os.path.isdir(x[0]), [(os.path.join(src, subdir), subdir) for subdir in os.listdir(src)]))

	# filter out excluded folders
	src_subdirs = list(filter(lambda x: not x[1] in exc, src_subdirs))

	log(f'INFO:\tFound these subdirectories in source: {[x[1] for x in src_subdirs]}')
	log(f'INFO:\tSubdirectories in exclusion list: {exc}')

	# counter for how many total files are moved between src and dst
	moved_file_count = 0

	# iterate through subdirs of src
	for (subdir_path, subdir_name) in src_subdirs:
		# create path to where corresponding dst subdir should be
		dst_subdir = os.path.join(dst, subdir_name)

		# check if that directory actually exists
		if not os.path.isdir(dst_subdir):
			log(f"WARN:\tNo directory called '{subdir_name}' found in destination dir '{dst}', no files will be moved from that source directory.")
			continue # next dir if it doesn't

		# walk all subdirs of src subdir (os.walk is recursive)
		for root, dirs, files in os.walk(subdir_path):
			for f in files:
				# create paths that include the filename
				src_file_path = os.path.join(root, f)
				dst_file_path = os.path.join(dst_subdir, f)
				try:
					# try to move it
					shutil.move(src_file_path, dst_file_path)
				except Error as err:
					# log and continue if something goes wrong
					log("ERROR:\t shutil.move() error while moving '{}' to '{}': {}".format(src_file_path, dst_file_path, err))
					continue 
				moved_file_count += 1
				log("INFO:\tMoved '{}' to '{}'.".format(src_file_path, dst_file_path))

	log(f"Done! {moved_file_count} files moved.")


if __name__ == "__main__":
	global logfolder
	# Hardcoded paths to the directories here! This should be the directory
	# that has subdirectories in it corresponding to the different categories
	# one might import into. At the time of writing, the folders are:
	# AVImports
	#  |- MUSIC
	#  |- PSA
	#  |- SHOWS
	#  |- STATION_IDS

	# Directory for files from Google Drive (that need to be imported)
	source_dir = "C:/Users/Samuel/Desktop/EXPORT_TO_AUTOMATION"

	# Directory that AVImport is searching for imported files
	destination_dir = "C:/Users/Samuel/Desktop/AVImports"

	# Directory to place log files in
	logfolder = "C:/Users/Samuel/Desktop/EXPORT_TO_AUTOMATION/export_logs"

	# List of subdirectories that the program should ignore when searching for files to move
	exclude_list = [
		"export_logs",
	]

	transfer(os.path.abspath(source_dir), os.path.abspath(destination_dir), exclude_list)