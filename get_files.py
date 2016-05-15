#! /home/b51816/localpython/python3/bin/python3
import os
import sys
class get_files(object):
   _path = os.getcwd()   ## get pwd as default directory
   def search_files(self,*args,path=_path,list_name="file_list"):
      if not args:
         raise ValueError("no args specified")

      self._path = path
      cmd = ("find %s -follow -name '*.%s' "%(self._path,args[0],))
      print("search directory: %s" %(self._path,))
      print("search target:")
      for t in args:
         cmd = cmd + '-o -name  "*.' + t +'" '
         print(t)
      cmd = cmd + " > " + list_name
      print("search cmd:\n"+cmd)
      os.system(cmd)
   pass


test_c = get_files()
test_c.search_files("sv","py",list_name="file_list_0",path="/proj/ult1/design/workarea/b51816/ULT1_TO1P1_PROD/blocks/gpcv2/testbench")
