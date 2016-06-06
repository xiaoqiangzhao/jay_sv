#### Repository: jay_sv
#### Author: Jay Zhao
#### Version 1.0
#### Email: zq496547199@126.com
#### Github: git@github.com:xiaoqiangzhao/jay_sv.git or https://github.com/xiaoqiangzhao/jay_sv.git
#### Description: To analysis TB or VIP based on systemverilog(UVM)



Existing issues:
   issue 1 (Already fixed): not able to detect multi-lines declaration as follow:
         class uvm_sequencer #(type REQ=uvm_sequence_item, RSP=REQ)
                                   extends uvm_sequencer_param_base #(REQ, RSP);
   issue 2 : no analysis for interface

