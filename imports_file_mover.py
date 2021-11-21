import os
import shutil

def log(msg):
	print(msg)

def transfer(src, dst):
	# get all subdirectories in src and dst folders (first one removed bc it is just the toplevel dir)
	src_subdirs = [x[0] for x in os.walk(src)][1:]
	dst_subdirs = [x[0] for x in os.walk(dst)][1:]

	# get list of basenames for convenience later
	src_subdirs_basenames = [os.path.basename(x) for x in src_subdirs]
	dst_subdirs_basenames = [os.path.basename(x) for x in dst_subdirs]

	# initialize match/unmatched lists 
	matched_src_dirs, unmatched_src_dirs, matched_dst_dirs, unmatched_dst_dirs = [],[],[],[]

	# check if there are any subdirectories in src that are not in dst
	for subdir in src_subdirs:
		matched_src_dirs.append(subdir) if os.path.basename(subdir) in dst_subdirs_basenames else unmatched_src_dirs.append(subdir)

	# check if there are any subdirectories in dst that are not in src
	for subdir in dst_subdirs:
		matched_dst_dirs.append(subdir) if os.path.basename(subdir) in src_subdirs_basenames else unmatched_dst_dirs.append(subdir)

	# log any unmatched src subdirs 
	for subdir in unmatched_src_dirs:
		log("Subdirectory '{}' in source directory not found in destination directory; no files from that directory will be moved.".format(subdir))

	# log any unmatched dst subdirs 
	for subdir in unmatched_dst_dirs:
		log("Subdirectory '{}' in destination directory not found in source directory; no files will be moved to it.".format(subdir))

	# log which directories were matched and will be explored
	log("Transferring files between the following subdirectories: {}, {}".format(
		list(map(os.path.basename, matched_src_dirs)), 
		list(map(os.path.basename, matched_dst_dirs))))

	# iterate through the source subdirectories
	for (srcdir, dstdir) in zip(matched_src_dirs, matched_dst_dirs):
		for root, dirs, files in os.walk(srcdir):
			for f in files:
				src_path = os.path.join(root, f)
				dst_path = os.path.join(dstdir, f)
				try:
					shutil.move(src_path, dst_path)
					log("Moved '{}' to '{}'.".format(src_path, dst_path))
				except Error as err:
					log("Error occurred while moving '{}' to '{}': {}".format(src_path, dst_path, err))

	log("Done!")


if __name__ == "__main__":
	# Hardcoded paths to the directories here! This should be the directory
	# that has subdirectories in it corresponding to the different categories
	# one might import into. At the time of writing, the folders are:
	# AVImports
	#  |- MUSIC
	#  |- PSA
	#  |- SHOWS
	#  |- STATION_IDS

	# Directory for files from Google Drive (that need to be imported)
	source_dir = "H:/Shared drives/WIIT Internal Documents/EXPORT_TO_AUTOMATION"
	# Directory that AVImport is searching for imported files
	destination_dir = "C:/Users/Samuel/Desktop/AVImports"
	transfer(os.path.abspath(source_dir), os.path.abspath(destination_dir))