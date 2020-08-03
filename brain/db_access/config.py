# -*- coding: utf-8 -*-
"""
Created on Sat Aug 01 2020

@author: Tean Alpha Squad
"""
import pymysql
class SQLConn:
    host = "localhost"
    username = "username_here"
    password = "password_here"
    db_name = "db_alpha"
    default_primary_key = 42
    def getSQLConn(self):
        mydb = pymysql.connect(self.host,self.username,self.password,self.db_name)
        return [mydb, mydb.cursor()]

    def get_default_td_pk(self):
        return self.default_primary_key
    