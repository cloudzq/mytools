# -*- coding:utf-8 -*-
"""
@Project:watchmen
@Language:Python3.6.4
@Author:Hans
@File:oracleClient.py
@Ide:PyCharm
@Time:2018/8/20 15:44
@Remark:
"""

import re
import datetime
import cx_Oracle


class OracleClient(object):
    def __init__(self, db_url='username/username@dbname.com.cn:1534/dbname'):
        self.db_url = db_url
        self.conn = None

    def __enter__(self):
        try:
            self.conn = self._connect()
            if self.conn:
                return self.conn
        except Exception as e:
            raise Exception("connet database failed...")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        self.conn = None

    def oracle_operation(self, sql):
        """
        oracle insert,delete,query,update function
        :param sql: str
        :return: None or list
        """
        result = None
        if self.conn is None:
            self.conn = self._connect()
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

        if 'select' in sql or 'SELECT' in sql:
            result = cur.fetchall()
        cur.close()
        return result

    def close(self):

        """
        close session
        :return: None
        """

        self.conn.close()

    def _connect(self):
        conn = cx_Oracle.connect(self.db_url)
        return conn

    def _insert_row(self, sql):
        if not self.conn:
            self.conn = self._connect()
        try:
            self.conn.cursor().execute(sql)
            self.conn.commit()
        except Exception as e:
            self.close()
            raise Exception(e.__str__())

    def insert_database(self, json_file):
        """
        insert data by json's file

        :param json_file: str
        :return: None
        """

        date = datetime.datetime.now().strftime("%Y-%m-%d")
        file_dir = json_file
        file_object = open(file_dir, 'r', 'utf-8')
        try:
            raw_data = file_object.read()
        finally:
            file_object.close()
        db_data = eval(raw_data)

        for table in db_data.get('tables'):
            table_name = table.get('name')
            for row in table.get('data'):
                if isinstance(row, dict):
                    values = ""
                    fileds = ""
                    for filed_key, filed_value in row.items():
                        fileds += "  %s," % (filed_key)
                        if isinstance(filed_value, str) and re.match('\d{4}-\d{2}-\d{2}', filed_value):
                            filed_value = "to_date('%s','yyyy-mm-dd hh24:mi:ss')" % (filed_value)
                            values += "  %s," % (filed_value)
                        else:
                            values += "  '%s'," % (filed_value)

                    sql = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, fileds.rstrip(','),
                                                               values.rstrip(','))
                    self._insert_row(sql)
                else:
                    sql = "insert into " + table_name + "values(to_date('" + date + " ','yyyy-mm-dd'),"
                    for values in row:
                        sql += "'" + str(values) + "',"
                    sql = sql[0:len(sql) - 1] + ")"
                    self._insert_row(sql)
        self.close()


if __name__ == '__main__':
    # 上下文管理方式，返回数据库连接对象conn，适合一次性操作数据库
    with OracleClient() as conn:
        # sql = 'select * from mytable where rownum<5'
        sql = "delete from mytable where name=43332"
        cur = conn.cursor()
        cur.execute(sql)
        # result = cur.fetchall()
        # for row in result:
        #     print(row)
        cur.commit()

    # 初始化oracle客户端后多次操作
    client = OracleClient(db_url='username/username@dbname.com.cn:1534/dbname')
    sql1 = 'select * from mytable where rownum<5'
    sql2 = 'update mytable set name=2231 where id =123'
    result1 = client.oracle_operation(sql1)
    result2 = client.oracle_operation(sql2)
    client.close()
    # 从文件中读取要插入的数据
    client = OracleClient(db_url='username/username@dbname.com.cn:1534/dbname')
    client.insert_database('/home/dir/test.txt')
    #从给定的文件中插入数据
    client = OracleClient(db_url='username/username@dbname.com.cn:1534/dbname')
    client.insert_database(json_file)
    #json_file格式：{"a":"b","c":"d","e":[{"a1":"a2","b1":[[87,7],[76,6]]}]}
    #{"a":"b","c":"d","e":[{"a1":"a2"},{"b1":"b2"}]}
    #
