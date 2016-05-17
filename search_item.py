#! /home/b51816/localpython/python3/bin/python3
import os
import sys
import re
import sqlite3
from enum import Enum,unique
class VERBOSE(Enum):
   LOW = 0
   MIDDLE =1
   HIGH = 2

class search_item(object):
   '''example:
         my_search = search_item()
         my_search.config( 
            target_type = "type",      ## set target type ["sv", wait for add]
            db = "db",                 ## set database file used
            table = "table",           ## set search table
            level = 1,                 ## set up-parent search level, 0 means always up-search, 1 means no up-search
            open_result = True|False,  ## set if the file will be opened with gvim
         )

         my_search.search_sv(
            name, 
            search_type = "type",      ## search_type should be among [class, function, task, parent,]
            level = 1,                 ## override config
            open_result = True|False,  ## override config
         )
   '''
   
   search_type_scope = dict()
   def __init__(self):
      self.target_name = ""
      self.search_type = "class"
      self.target_type = "sv"    ## set default target type as system verilog
      self.search_type_scope["sv"]= ("class", "parent", "function", "task", "file_location")
      self.db = "./db/default.db"
      self.table = "classes"
      self.level = "1"  ## default only search current level, no up to parent
      self.open_result = False

   def config(self, **kwargs): #search_type,db,table,level):
      if "target_type" in kwargs:
         self.target_type = kwargs["target_type"]
      if "db" in kwargs:
         if not os.path.isfile(kwargs["db"]):
            raise ValueError("No such database named %s exist" % kwargs["db"])
         self.db = kwargs["db"]
      if "table" in kwargs:
         self.table = kwargs["table"]
      if "level" in kwargs:
         self.level = kwargs["level"]

      if "open_result" in kwargs:
         if not kwargs["open_result"] in [True,False]:
            raise ValueError("Invalid arg for open_result, should be True or False")
         self.open_result = kwargs["open_result"]

   def search_sv(self, name, **kwargs):
      self.target_name = name
      if "search_type" in kwargs:
         if not kwargs["search_type"] in self.search_type_scope[self.target_type]:
            raise ValueError("Invalid search type")
         self.search_type = kwargs["search_type"]

      if "open_result" in kwargs:
         if not kwargs["open_result"] in [True,False]:
            raise ValueError("Invalid arg for open_result, should be True or False")
         self.open_result = kwargs["open_result"]

      if "level" in kwargs:
         self.level = kwargs["level"]

      mx_conn = sqlite3.connect(self.db)
      mx_cursor = mx_conn.cursor()
      if self.search_type == "class":
         mx_cursor.execute('select * from %s where class = ?' % self.table, (self.target_name,))
         mx_results =mx_cursor.fetchall()
      
      valid_index = False
      # print(type(mx_results),mx_results.__len__())
      if mx_results.__len__() == 0: 
         print("No item recored for %s" % self.target_name)
         sys.exit()
      if mx_results.__len__() == 1:
         finall_result = mx_results.pop()
      else:
         for result_item in mx_results:
            print(result_item)
         index = input("Please choose the wanted item:")
         for result_item in mx_results:
            if result_item[0].__eq__(index):
               finall_result = result_item
               valid_index = True
               break
         if not valid_index:
            raise ValueError("Invalid Index")
      print("------------------------------ Result of %s %s -------------------------" % (self.search_type, self.target_name))
      print("----- Class Name   : "+finall_result[1])
      print("----- Parent Name  : "+finall_result[2])
      print("----- Function List: ")
      finall_result_functions = finall_result[3].split(" ")
      for f in finall_result_functions:
         print("-----                "+f)
      print("----- Task List    : ")
      finall_result_tasks = finall_result[4].split(" ")
      for t in finall_result_tasks:
         print("-----                "+t)
      print("----- File Location: "+finall_result[5])

      if self.open_result:
         os.system("gvim %s" % finall_result[5])
      
      next_search_level = 1
      if finall_result[2] and (self.level != 1):
         if self.level:  ## > 1
            next_search_level = self.level - 1 
         search_parent = input("Continue Search Parent %s ?:(yes|no) " % finall_result[2])
         if search_parent == "yes":
            self.search_sv(finall_result[2], search_type = "class", level = next_search_level )
         

if __name__ == "__main__":
   my_search = search_item()
   my_search.config(target_type = "sv", db = "./db/jay_uvm.db", table = "classes", level = 1, open_result = True)
   my_search.search_sv("zmk_ref_model", search_type = "class", level = 3)
