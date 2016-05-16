#! /home/b51816/localpython/python3/bin/python3
import os
import sys
class get_files(object):
   _path = os.getcwd()   ## get pwd as default directory
   
   def __init__(self,**kwargs):
      self._path = os.getcwd()
      self._list_name = "file_list"
      if "path" in kwargs:
         self._path = kwargs["path"]
      if "list_name" in kwargs:
         self._list_name = kwargs["list_name"]


   def search_files(self,*args,**kwargs):
      if not args:
         raise ValueError("no args specified")
      
      if "path" in kwargs:
         self._path = kwargs["path"]
      if "list_name" in kwargs:
         self._list_name = kwargs["list_name"]

      cmd = ("find %s -follow -name '*.%s' "%(self._path,args[0],))
      print("search directory: %s" %(self._path,))
      print("search target:")
      for t in args:
         cmd = cmd + '-o -name  "*.' + t +'" '
         print(t)
      cmd = cmd + " > " + self._list_name
      print("search cmd:\n"+cmd)
      os.system(cmd)
   pass

if __name__=='__main__':
   test_c = get_files(list_name="file_list_1",path="/proj/ult1/design/workarea/b51816/ULT1_TO1P1_PROD/blocks/gpcv2/testbench")
   test_c.search_files("sv","py",)
