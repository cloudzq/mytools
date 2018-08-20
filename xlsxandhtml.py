# -*- coding:utf-8 -*-
"""
@Project:watchmen
@Language:Python3.6.4
@Author:Hans
@File:xlsxtohtml.py
@Ide:PyCharm
@Time:2018/8/17 17:32
@Remark:
"""

import pandas as pd
import codecs

def xlsxTohtml():
    xd=pd.ExcelFile('./student.xls')
    df=xd.parse()

    with codecs.open('./student.html','w','utf-8') as html_file:
        html_file.write(df.to_html(header=True,index=False))

def htmlToxlsx():
    with open('./student.html', 'r') as f:
        df = pd.read_html(f.read().encode('utf-8'), encoding='utf-8')
    bb = pd.ExcelWriter('./out.xlsx')
    df[0].to_excel(bb)
    bb.close()

if __name__ == '__main__':
    # xlsxTohtml()
    htmlToxlsx()