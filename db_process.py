#! /home/b51816/localpython/python3/bin/python3
import os
import sys
import re
import sqlite3
from get_files import get_files
from analysis_files import analysis_files
import getopt

update = False
target_db = ""
target_name = ""
search_type = ""
ana_type = ""
base_dir = ""
try:
   opts,args = getopt.getopt(sys.argv[1:],"f:ut:",["name=","search_type=","ana_type=","dir=","help"])
except getopt.GetoptError:
   print("Bad Options")

def help():
   print("wait for fix")
   sys.exit()

for o,a in opts:
   if o in ("-f"):
      target_db = a
   if o in ("-u"):
      update = True
   if o in ("--name"):
      target_name = a
   if o in ("--search_type"):
      search_type = a
   if o in ("--ana_type"):
      ana_type = a
   if o in ("--dir"):
      base_dir = a
   if o in ("--help"):
      help()

if not target_db:
   raise ValueError("Need Target Database File")
if update and ((not base_dir) or (not ana_type)):
   raise ValueError("Need directory and ana_type for Update")
if (not update) and ((not search_type) or (not target_name)):
   raise ValueError("Need search_type and target_name")

if ana_type == "sv":
      file_type=("sv","svh")
      table_name = "classes"

if update:
   if not os.path.isdir(base_dir):
      raise ValueError("Illegal Directory")
   jay_get_files = get_files(list_name="./temp_file.caf", path = base_dir)
   jay_get_files.search_files(*file_type)

   jay_analysis_files = analysis_files(output_db = target_db)
   jay_analysis_files.update_db(arg_table_name = table_name, arg_ana_type = ana_type, arg_file_list = "./temp_file.caf")
