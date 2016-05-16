#! /home/b51816/localpython/python3/bin/python3
import os
import sys
import re
import sqlite3

class analysis_files(object):
   re_class = re.compile(r'^\s{0,}(virtual)?\s{0,}class\s+(.*)\s+extends\s+(\w+)')  ## group[1]: virtual group[2]: class name group[3]: parent name
   re_end_class = re.compile(r'^\s{0,}endclass')  ## end of class
   re_function = re.compile(r'^\s{0,}(virtual)?\s{0,}function\s+([`\w]+\s+|)(([`\w]+)::|)([`\w]+)\s{0,}\(')   ## group[1]: virtual  group[2]: return type group[4:3]: extern function or not    group[5]: function name
   re_task = re.compile(r'^\s{0,}(virtual)?\s{0,}task\s+(([`\w]+)::|)([`\w]+)\s{0,}\(')## group[1]: virtual    group[3:2] extern task or not    group[4]: task name

   _file_list = "./file_list"    ## default file list
   output_db = "./db/default.db"   ## set default args
   ana_type = "sv"
   table_name = "classes"
   def __init__(self,**kwargs):
      print("initialization...")
      self._file_list = "./file_list"    ## default file list
      self.output_db = "./db/default.db"   ## set default args
      self.ana_type = "sv"
      self.table_name = "classes"

      if "output_db" in kwargs:
         self.output_db = kwargs["output_db"]
      if "ana_type" in kwargs:
         self.ana_type = kwargs["ana_type"]
      if "table_name" in kwargs:
         self.table_name = kwargs["table_name"]
      if "source_file" in kwargs:
         self._file_list = kwargs["source_file"]

   def IsTableExist(self,cursor,table_name): 
      cursor.execute('select name from sqlite_master where type="table" and name = ?',(table_name,))
      table=cursor.fetchall()
      if table:
         return True
      else:
         return False

   def analysis(self,file_name,**kwargs):
      output_db = self.output_db
      ana_type  = self.ana_type
      table_name = self.table_name
      print("-----------------File: "+file_name+"------------------------")

      if "arg_output_db" in kwargs :
         output_db = kwargs["arg_output_db"]
      if "arg_ana_type" in kwargs:
         ana_type = kwargs["arg_ana_type"]
      if "arg_table_name" in kwargs:
         table_name = kwargs["arg_table_name"]

      mx_conn = sqlite3.connect(output_db)
      mx_cursor = mx_conn.cursor()
      class_found = False
      my_class = []
      current_class = ""
      my_class_parent = dict() 
      functions = dict()    ## store function names
      tasks = dict()
      with open (file_name,'r') as f:
         for line in f.readlines():
            line=line.strip()
            line_class = self.re_class.match(line)
            line_end_class = self.re_end_class.match(line)
            line_function = self.re_function.match(line)
            line_task = self.re_task.match(line)
            if line_class:
               class_found = True
               current_class = line_class.group(2)
               my_class.append(line_class.group(2))
               my_class_parent[current_class] = line_class.group(3)
               functions[current_class]=[]
               tasks[current_class]=[]
               # print("class %s parent %s" % (line_class.group(2),line_class.group(3)))
            if line_end_class:
               class_found = False
               # print("End of Class")
            if line_function:
               # print(line_function.groups())
               if line_function.group(4):
                  functions[line_function.group(4)].append(line_function.group(5))
               else:
                  functions[current_class].append(line_function.group(5))
            if line_task:
               # print(line_task.groups())
               if line_task.group(3):
                  tasks[line_task.group(3)].append(line_task.group(4))
               else:
                  tasks[current_class].append(line_task.group(4))

      for cla in my_class:
         str_function = " ".join(functions[cla])
         str_task = " ".join(tasks[cla])
         print("---------------------------------------------------------------")
         print("Class   : "+cla)
         print("Parent  : "+my_class_parent[cla])
         print("Fuctions: "+str_function)
         print("Tasks   : "+str_task)
         print("---------------------------------------------------------------")
         mx_cursor.execute('insert into %s (class_name,parent_name,tasks,functions,file_location) values (?,?,?,?,?)' % table_name, (cla, my_class_parent[cla], str_function, str_task, file_name))

      mx_cursor.close()
      mx_conn.commit()
      mx_conn.close()

   def update_db(self,**kwargs):
      output_db = self.output_db
      ana_type  = self.ana_type
      table_name = self.table_name
      source_filelist = self._file_list
      if "arg_output_db" in kwargs :
         output_db = kwargs["arg_output_db"]
      if "arg_ana_type" in kwargs:
         ana_type = kwargs["arg_ana_type"]
      if "arg_table_name" in kwargs:
         table_name = kwargs["arg_table_name"]
      if "arg_file_list" in kwargs:
         source_filelist= kwargs["arg_file_list"]

      print("connecting to database: %s"% os.path.abspath(output_db))
      mx_conn = sqlite3.connect(output_db)
      mx_cursor = mx_conn.cursor()
      if self.IsTableExist(mx_cursor,table_name):
         print("table %s already exist, delete and re-generate" % table_name)
         mx_cursor.execute('drop table %s'% table_name)
      mx_cursor.execute('create table %s (id integer primary key autoincrement,class_name tinytext,parent_name tinytext,tasks text,functions text,file_location tinytext)' % table_name)
      mx_cursor.close()
      mx_conn.commit()
      mx_conn.close()
      with open (source_filelist,'r') as f:
         for line in f.readlines():
            line=line.strip()
            self.analysis(line,arg_output_db=output_db, arg_ana_type=ana_type, arg_table_name=table_name)
   pass

if __name__=='__main__':
   a=analysis_files(output_db="./db/jay_uvm.db")
   a.update_db(arg_file_list="jay_uvm.caf")

