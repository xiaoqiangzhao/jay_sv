#! /home/b51816/localpython/python3/bin/python3
import os
import sys
import re
import sqlite3

class analysis_files(object):
   _file_list = "./file_list"    ## default file list
   re_class = re.compile(r'^\s{0,}(virtual){0,1}\s{0,}class\s+(\w+)\s+extends\s+(\w+)')  ## group[0]: virtual group[1]: class name group[2]: parent name
   re_end_class = re.compile(r'^\s{0,}endclass')  ## end of class
   def IsTableExist(self,cursor,table_name): 
      cursor.execute('select name from sqlite_master where type="table" and name = ?',(table_name,))
      table=cursor.fetchall()
      print(table)
      if table:
         return True
      else:
         return False

   def analysis(self,file_name,output_db="./db/default.db",ana_type="sv",table_name="classes"):
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

   def update_db(self,source_filelist=_file_list,output_db="./db/default.db",ana_type="sv",table_name="classes"):
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
            self.analysis(line,output_db,ana_type,table_name)
   pass


a=analysis_files()
a.update_db("file_list_0")

