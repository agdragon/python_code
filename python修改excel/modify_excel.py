#!/usr/bin/python
#coding=utf-8


  
from xlrd import open_workbook
from xlutils.copy import copy
 
rb = open_workbook(u'Template.xlsx')
 
#通过sheet_by_index()获取的sheet没有write()方法
rs = rb.sheet_by_index(0)
 
wb = copy(rb)
 
#通过get_sheet()获取的sheet有write()方法
ws = wb.get_sheet(0)
ws.write(0, 0, 'changed!')
 
a = wb.save(u'Template.xls')
print a





import os 
from xlutils.copy import copy 
import xlrd as ExcelRead 
  
def write_append(file_name): 
  values = ["李四", "woman", 22, "UK"] 
  
  r_xls = ExcelRead.open_workbook(file_name) 
  r_sheet = r_xls.sheet_by_index(0) 
  rows = r_sheet.nrows 
  w_xls = copy(r_xls) 
  sheet_write = w_xls.get_sheet(0) 
  
  for i in range(0, len(values)): 
    sheet_write.write(rows, i, values[i]) 
  
  w_xls.save('out.xls'); 
  
if __name__ == "__main__": 
  write_append('Template.xlsx')