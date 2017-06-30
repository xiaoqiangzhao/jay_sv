#! /home/b51816/local/bin/python3
import os
import sys
import re
import sqlite3
from get_files import get_files
from analysis_files import analysis_files
from search_item import search_item
import getopt

update = False
target_dbr = "jay_uvm.db"   ## default db
target_name = ""
search_type = "class"   ## default search_type
ana_type = "sv"
search_dir = ""
ana_len = 1  ## lines merged together for analysis
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
      search_dir = os.path.abspath(a)
   if o in ("--help"):
      help()

print(os.path.abspath(os.path.realpath(sys.argv[0])))
work_dir = os.path.dirname(os.path.abspath(os.path.realpath(sys.argv[0])))
temp_file = os.path.join(work_dir,"template/temp_file")
db_files =  re.split(r'[;,\s]+',target_db)
print(work_dir)
print(temp_file)
print("Database Used: {}".format(db_files))
# sys.exit()
if not target_db:
   raise ValueError("Need Target Database File")
if update and ((not search_dir) or (not ana_type)):
   raise ValueError("Need directory and ana_type for Update")
if (not update) and ((not search_type) or (not target_name)):
   raise ValueError("Need search_type and target_name")

if ana_type == "sv":
   file_type=("sv","svh","svp")
   table_name = "classes"
   ana_len = 3
else:
   raise ValueError("wait for adding")

if update:
   if not os.path.isdir(search_dir):
      raise ValueError("Illegal Directory")
   jay_get_files = get_files(list_name = temp_file)
   jay_get_files.search_files(*file_type, path = search_dir )

   db_file = os.path.join(work_dir,"db",db_files[0])
   jay_analysis_files = analysis_files(output_db = db_file)
   jay_analysis_files.update_db.set_verbose()
   jay_analysis_files.update_db(arg_table_name = table_name, arg_ana_type = ana_type, arg_file_list = temp_file, arg_ana_len = ana_len)
else:
   jay_search_item = search_item()
   for db_i in db_files:
       db_file = os.path.join(work_dir,"db",db_i)
       jay_search_item.config(target_type = ana_type, db = db_file, table = table_name, level = 1, open_result = True)
       jay_search_item.patch_search(target_name, target_type = ana_type, search_type = search_type)
       if jay_search_item.hit:
           break
