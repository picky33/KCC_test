# create a program knows the last time i "Downloaded" a manga to my kindle and it keeps track of the last of that chapter
# it will create new .Mobi Files for every chapter from the last kindle download to newest chapter.
# I need to implement a button or command to "export" the .mobi files and
# then mark those chapters as last downloaded to my kindle

# HOW TO DO

# Grab a list of every directory and grab a list of every file in that directory - Done
# Grab the name of the newest file, that is "Newest Chapter" for that manga - Changed to grab last chapter - Done
#   - Use objects - make manga name the object name and add fields for each chapter, last exported, newest, etc. - Done
#
# Run manga_converter script for all chapters that from last exported to newest - Done
#   - Copy relevant files to a new directory - Done
#       - some how need to copy only relevant files and all in-between, i suspect this will be hardest part - Done
#   - Convert files - Done
#   - Copy .mobi files back (may need to rename or add date or list chapters!!! ) - !! Done
#   - delete copied data - Done
#
# Create a method to mark files for export - Done
#   - grab latest chapter and make it the last exported chapter - Done
#   - Move .mobi files to new destination - Done
#   - Do i need to delete any files and i should probably export the JPG images to - Done
# Make it a cron or scheduled task that runs 1-2 times a week
#
# Create a web interface that allows a user to control the program
#   - Create a button to select a manga folder
#   - Create a button to select a destination folder (maybe)
#   - Create a checkbox to export all chapters vs. unexported chapters
#   - Create a start button that starts the program
#   - add a way to view the console output
#   - create a checkbox to select single thread or multi thread
#
#
# Create a way to save settings to a file such as an ini file
#   - save the manga folder file path
#   - save the destination folder file path
#   - save the last exported chapter for each manga
#   - save the newest chapter for each manga
#   - save the options of single thread or multi threaded
#   - save whatever else is needed
#
# Create a way to load settings from a file such as an ini file
#   - load the manga folder file path
#   - load the destination folder file path
#   - somehow need to initialize the manga class with saved values
#   - load the last exported chapter for each manga
#   - load the newest chapter for each manga
#   - load the options of single thread or multi threaded
#   - load whatever else is needed
#
#
#
# NICE TO HAVES
# Make it so i can run it on an AWS server or something in clouds
# Give it a button or gui for these actions
#   - add python terminal or something to show status
#
#
#
# NEEDS to Research
# How do you send a command to an already running program?
#   - i could cheat and just have it read a text file for a 'Yes' or 'No"
#   - Gui would have to solve this
#   - *insert whatever i research*
# Haku is open source i should look into automatic downloading if that's possible

import kindlecomicconverter.comic2ebook as c2e
from multiprocessing import freeze_support, set_start_method
import os
import sys
import subprocess
import pathlib
import tkinter as tk
from tkinter import filedialog
import platform
import shutil
import checksumdir
import configparser

#File Paths for Debugging purposes
Fpath = '/Users/nicholasharman/Documents/Manga_to_try/To_Convert'
F_Temp_path = '/Users/nicholasharman/Documents/Manga_to_try/To_Convert/temp'

def get_manga_path():
    root = tk.Tk()
    if platform.system() == 'Windows':
        root.withdraw()
        file_path = filedialog.askdirectory(mustexist=True,initialdir = os.path.expanduser('~'),title = "Select a folder containing the manga")
    elif platform.system() == 'Linux':
        root.withdraw()
        file_path = filedialog.askdirectory(mustexist=True,initialdir = os.path.expanduser('~'),title = "Select a folder containing the manga")
    elif platform.system() == 'Darwin': #MAC OS X
        root.withdraw()
        file_path = filedialog.askdirectory(mustexist=True,initialdir = os.path.expanduser('~'),title = "Select a folder containing the manga")
    else:
        root.withdraw()
        file_path = filedialog.askdirectory(mustexist=True,initialdir = os.path.expanduser('~'),title = "Select a folder containing the manga")
    root.update()
    return file_path

def create_directory_dictionary(path):
    directory_dictionary = {}
    for dir in os.scandir(path):
        if dir.is_dir():
            directory_dictionary[dir.name] = [file.name for file in os.scandir(dir.path)]
    return directory_dictionary

#check keys in dictionary for a specific value, if value exists, delete value
def delete_value_from_dictionary(dictionary, value):
    for key in dictionary:
        if value in dictionary[key]:
            dictionary[key].remove(value)
    return dictionary

#get date modified time of a file to determine which file is the newest
def get_date_modified(file):
    return os.path.getmtime(file)

#sort dictionary values alaphabetically
def sort_dictionary_values(dictionary):
    for key in dictionary:
        dictionary[key].sort()
    return dictionary

#grab the last value in a given key
def get_last_value(dictionary, key):
    return dictionary[key][-1]

#replace spaces with underscores in a string
def replace_spaces_with_underscores(string):
    aa = string.replace(" ", "_")
    bb= aa.replace('-', '_')
    cc= bb.replace("__", "_")
    title = cc.replace("__", "_")
    return title

def copy_directory(source, destination):
    if not os.path.exists(destination):
        #os.makedirs(destination)
        shutil.copytree(source, destination)
    else:
        hashS = checksumdir.dirhash(source, 'sha1')
        hashD = checksumdir.dirhash(destination, 'sha1')
        if hashS == hashD:
            print('No changes')
        else:
            print('Copying')
            os.removedirs(destination)
            shutil.copytree(source, destination)
    #shutil.copytree(source, destination)

#get first and last unexported chapter
def get_first_and_last_unexported_chapters(M):
    first_unexported_chapter = M.unexported_chapters[0]
    last_unexported_chapter = M.unexported_chapters[-1]
    return first_unexported_chapter, last_unexported_chapter

def parse_Manga_Names(Fpath):
    #Turns each Manga into a dictionary with the name of the manga as the key and the list of chapters as the value
    subfolders = create_directory_dictionary(Fpath)
    subfolders = delete_value_from_dictionary(subfolders, '.DS_Store')
    subfolders = sort_dictionary_values(subfolders)
    return subfolders

# create a list of chapters that have not been exported
def get_unexported_chapters(self):
    unexported_chapters = []
    for chapter in self.chapters:
        if chapter not in self.last_exported:
            unexported_chapters.append(chapter)
    return unexported_chapters

def export_unexported_chapters():
    for M in Manga._registry:
        print (M.name)
        Unexported = M.unexported_chapters
        first = Unexported[0]
        last = Unexported[-1]
        #copy all chapters from last exported chapter to newest chapter to the manga folder
        for chapter in M.chapters:
            if chapter in (Unexported):
                copy_directory(Fpath + "/" + M.name + "/" + str(chapter), F_Temp_path + "/" + M.name + "/" + str(chapter))
                M.set_last_export()
                print("Copied " + str(chapter) + " to " + M.name)
            else:
                print("Chapter " + str(chapter) + " already exists")
        rename_directory(F_Temp_path + "/" + M.name, F_Temp_path + "/" + M.name + " " + first + " - " + last)

def export_all_chapters():
    for M in Manga._registry:
        print (M.name)
        #copy all chapters to the manga folder
        for chapter in M.chapters:
            #if directory does not exist, create it
            if not os.path.exists(F_Temp_path + "/" + M.name + "/" + str(chapter)):
                copy_directory(Fpath + "/" + M.name + "/" + str(chapter), F_Temp_path + "/" + M.name + "/" + str(chapter))
                M.set_last_export()
                print("Copied " + str(chapter) + " to " + M.name)
            else:
                print("Chapter " + str(chapter) + " already exists")

def convert_manga_to_ebook(F_Temp_path):
    #need to make a multi-threaded function that will convert each manga to an ebook
    dir_list = next(os.walk(F_Temp_path))
    set_start_method('spawn')
    freeze_support()
    place=0
    for a in dir_list[1]:
        place += 1
        print(str(place) + " of " + str(len(dir_list[1])) + " " + a)
        c2e.main(["--profile=KV", "--upscale", "--splitter=0", F_Temp_path + "/" + a])

def delete_temp_directory(F_Temp_path):
    shutil.rmtree(F_Temp_path)
    print("Deleted temp directory")

# i need to move all files that end in a .mobi to a new directory
def move_mobi_files(source,destination):
    dir_list = next(os.walk(source))
    for a in dir_list[2]:
        if a.endswith(".mobi"):
            shutil.move(source + "/" + a, destination)
            print("Moved " + a + " to MOBI")
        else:
            print("Not a mobi file")

#rename a directory
def rename_directory(source, destination):
    os.rename(source, destination)
    print("Renamed " + source + " to " + destination)

# try and read an ini file to get settings such as file paths last exported, etc., if it doesn't exist skip
def read_ini_file(file):
    try:
        config = configparser.ConfigParser()
        config.read(file)
        return config
    except:
        print("No ini file found")
        return None

# first check if ini file exists, if not create it and then write an ini file to save settings such as file paths last exported, etc
def write_ini_file(file, config):
    with open(file, 'w') as configfile:
        config.write(configfile)
    print("Wrote config file")

#create config file if it does not exist
def create_config_file(file):
    config = configparser.ConfigParser()
    config.add_section('Settings')
    config.set('Settings', 'last_exported', '0')
    with open(file, 'w') as configfile:
        config.write(configfile)
    print("Created config file")


#I need to turn the keys in a dictionary into a class with the key as the object name and values as the chapter names
#I need to make a class for this
class Manga(object):
    #__metaclass__ = IterManga
    _registry = []
    #constructor
    def __init__(self, my_dict, key, Fpath):
        self._registry.append(self)
        self.name = key
        self.chapters = my_dict[key]
        self.Filepath = Fpath + "/" +self.name
        #self.last_exported = self.chapters[0]
        self.last_exported = ""
        self.newest = self.chapters[-1]
        self.last_downloaded = self.chapters[-1]
        self.last_converted = self.chapters[-1]
        self.last_exported_date = get_date_modified(self.Filepath + "/" + self.last_exported)
        self.newest_date = get_date_modified(self.Filepath + "/" + self.newest)
        self.last_downloaded_date = get_date_modified(self.Filepath + "/" + self.last_downloaded)
        self.last_converted_date = get_date_modified(self.Filepath + "/" + self.last_converted)
        self.last_exported_chapter = self.last_exported
        self.newest_chapter = self.newest
        self.last_downloaded_chapter = self.last_downloaded
        self.last_converted_chapter = self.last_converted
        self.last_exported_chapter_date = self.last_exported_date
        self.newest_chapter_date = self.newest_date
        self.last_downloaded_chapter_date = self.last_downloaded_date
        self.last_converted_chapter_date = self.last_converted_date
        self.last_exported_chapter_name = self.last_exported
        self.newest_chapter_name = self.newest
        self.unexported_chapters = get_unexported_chapters(self)


    def set_last_export(self):
        self.last_exported = self.newest
        self.last_exported_date = get_date_modified(self.Filepath + "/" + self.last_exported)
        self.last_exported_chapter = self.last_exported
        self.last_exported_chapter_date = self.last_exported_date
        self.last_exported_chapter_name = self.last_exported
        #return self.last_exported




if __name__ == '__main__':
    print("Starting")

    #get the path to the manga - Turned off for debug purposes
    #Fpath= get_manga_path()
    #F_Temp_path = Fpath + "/Temp"

    subfolders = parse_Manga_Names(Fpath)

    print("Done")

    #converts my dictionary of manga titles and chapters into individual manga objects
    for key, val in subfolders.items():
        title = replace_spaces_with_underscores(key)
        exec(title + " = Manga(subfolders ,key, Fpath)")


    # print('Done')
    # export_unexported_chapters()
    # print("Done")
    # convert_manga_to_ebook(F_Temp_path)
    # print("Done")
    # move_mobi_files(F_Temp_path,Fpath)
    # print('Done')
    # delete_temp_directory(F_Temp_path)
    # print('Done')
