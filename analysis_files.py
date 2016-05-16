#! /home/b51816/localpython/python3/bin/python3
import os
import sys
import re
import sqlite3

class analysis_files(object):
   re_class = re.compile(r'^\s{0,}(virtual){0,1}\s{0,}class\s+(.*)\s+extends\s+(\w+)')  ## group[1]: virtual group[2]: class name group[3]: parent name
   re_end_class = re.compile(r'^\s{0,}endclass')  ## end of class

   _file_list = "./file_list"    ## default file list
   output_db = "./db/default.db"   ## set default args
   ana_type = "sv"
   table_name = "classes"
   def __init__(self,**kwargs):
      print("initialization...")
      for k,w in kwargs.items():
         print(k,w)
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
      print(table)
      if table:
         return True
      else:
         return False

   def analysis(self,file_name,**kwargs):
      output_db = self.output_db
      ana_type  = self.ana_type
      table_name = self.table_name

      if "arg_output_db" in kwargs :
         output_db = kwargs["arg_output_db"]
      if "arg_ana_type" in kwargs:
         ana_type = kwargs["arg_ana_type"]
      if "arg_table_name" in kwargs:
         table_name = kwargs["arg_table_name"]

      mx_conn = sqlite3.connect(output_db)
      mx_cursor = mx_conn.cursor()
      class_found = False
      with open (file_name,'r') as f:
         for line in f.readlines():
            line=line.strip()
            line_class = self.re_class.match(line)
            line_end_class = self.re_end_class.match(line)
            if line_class:
               class_found = True
               print("class %s parent %s" % (line_class.group(2),line_class.group(3)))
            if line_end_class:
               class_found = False
               print("End of Class")
      mx_cursor.close()
      mx_conn.commit()
      mx_conn.close()

   def update_db(self,source_filelist=_file_list,**kwargs):
      output_db = self.output_db
      ana_type  = self.ana_type
      table_name = self.table_name
      if "arg_output_db" in kwargs :
         output_db = kwargs["arg_output_db"]
      if "arg_ana_type" in kwargs:
         ana_type = kwargs["arg_ana_type"]
      if "arg_table_name" in kwargs:
         table_name = kwargs["arg_table_name"]

      print("connecting to database: %s"% os.path.abspath(output_db))
      mx_conn = sqlite3.connect(output_db)
      mx_cursor = mx_conn.cursor()
      if self.IsTableExist(mx_cursor,table_name):
         print("table %s already exist, delete and re-generate" % table_name)
         mx_cursor.execute('drop table %s'% table_name)
      mx_cursor.execute('create table %s (id integer primary key autoincrement,class_name tinytext,parent_name tinytext,tasks text,functions text)' % table_name)
      mx_cursor.close()
      mx_conn.commit()
      mx_conn.close()
      with open (source_filelist,'r') as f:
         for line in f.readlines():
            line=line.strip()
            self.analysis(line,arg_output_db=output_db, arg_ana_type=ana_type, arg_table_name=table_name)
   pass

if __name__=='__main__':
   a=analysis_files(output_db="./db/test.db")
   a.update_db("file_list_0")

