# -*- coding:utf-8 -*-
"""
@Project:watchmen
@Language:Python3.6.4
@Author:Hans
@File:jsontoexcel.py
@Ide:PyCharm
@Time:2018/8/16 19:31
@Remark:
"""
import xlrd
from collections import OrderedDict
import json
import codecs

import xlwt
#/home/centos/my_code/mytools/student.xls
def excelTojson():
    file_name = input('请输入要转换的excle文件路径:')
    wb = xlrd.open_workbook(file_name)
    dict_list = []
    sh = wb.sheet_by_index(0)
    title = sh.row_values(0)
    for rownum in range(1, sh.nrows):
        rowvalue = sh.row_values(rownum)
        single = OrderedDict()
        for colnum in range(0, len(rowvalue)):
            print(title[colnum], rowvalue[colnum])
            single[title[colnum]] = rowvalue[colnum]
        dict_list.append(single)

    j = json.dumps(dict_list)

    with codecs.open(file_name[:-5] + '.json', "w", "utf-8") as f:
        f.write(j)

#/home/centos/my_code/mytools/studen.json
def jsonToexcel():
    file_name = input('请输入要转换的json文件路径:')
    jsonfile = json.load(open(file_name))
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('student')
    ll = list(jsonfile[0].keys())
    for i in range(0,len(ll)):
        sheet1.write(0,i,ll[i])
    for j in range(0,len(jsonfile)):
        m = 0
        ls = list(jsonfile[j].values())
        for k in ls:
            sheet1.write(j + 1, m, k)
            m += 1
            workbook.save('student.xls')

if __name__ == '__main__':
    jsonToexcel()
    # excelTojson()
