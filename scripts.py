import os
import shutil

def move(ending, dirname, root = os.getcwd()):
	directory = os.path.join(root,dirname)
	if not os.path.exists(directory):
		os.makedirs(directory)
		print(f"Creating the folder {directory}....")
		
		
	for subdir, dirs, files in os.walk(root):
		for File in files:
			if File.endswith(ending):
				filePath = os.path.join(root,File)
				if not os.path.exists(os.path.join(subdir,File)):
					print(f"Moving {File} to {subdir} folder....")
					shutil.move(filePath, subdir)			

#To create a list of directories inside the root folder.
def create_dirs(dirlist, root = os.getcwd()):
	for dirname in dirlist:
		dirpath = os.path.join(root,dirname)
		if not os.path.exists(dirpath):
			print(f"Creating the folder {dirname}....")
			os.makedirs(dirpath)


#To destruct file hierarchy within the root folder.	
def destruct(root = os.getcwd(), curr):
	for File in os.listdir(curr):
		if (os.path.isfile(os.path.join(curr,File))):
			print(f"Moving {File} to {root}...")
			shutil.move(os.path.join(curr,File),os.path.join(root,File))
		elif (os.path.isdir(os.path.join(curr,File))):
			destruct(root,os.path.join(curr,File))
		else:
			sys.exit(f"{File} is neither file nor folder...")
		if (curr != root):
			os.rmdir(curr)
			print(f"Deleting {curr}")

