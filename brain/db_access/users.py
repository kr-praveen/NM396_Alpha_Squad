# -*- coding: utf-8 -*-
"""
Created on Sat Aug 01 2020

@author: Team Alpha Squad
"""

class UserObj():
    def __init__(self):
        self.username = None
        self.pwd = None
        self.name = None
        self.dept = None
        self.email = None
        self.phone = None
        
class UserDAO:
    def getData(self, u_name, password):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        mycursor = sql_con.getSQLConn()
        user_obj = UserObj()
        query = 'select * from tbl_users where u_username = "' + str(u_name) +'" and u_pwd = "' + str(password) +'"'
        if mycursor[1].execute(query) !=0:
            a = mycursor[1].fetchall()[0]
            user_obj.username = a[0]
            user_obj.pwd = a[1]
            user_obj.name = a[2]
            user_obj.dept = a[3]
            user_obj.email = a[4]
            user_obj.phone = a[5]
            mycursor[1].close()
            mycursor[0].close()
            return user_obj
        else: 
            return False
        
        
    
    def setData(self, uname_, pwd_, name_, dept_, email_, phone_):
        user_obj = UserObj()
        user_obj.username = uname_
        user_obj.pwd = pwd_
        user_obj.name = name_
        user_obj.dept = dept_
        user_obj.email = email_
        user_obj.phone = phone_
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query = "insert into tbl_users(u_username, u_pwd, u_name, u_dept, u_email, u_phone) values('"+uname_+"', '"+pwd_+"', '"+name_+"','"+dept_+"','"+email_+"','"+phone_+"')"
        try:
            obj[1].execute(query)
            obj[0].commit()
            
            return 1
        except:
            obj[0].rollback()
            return 0
        finally:
            obj[1].close()
            obj[0].close()
                
        return 0
        
        
    
    def updateName(self, username_, new_name ):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query= "update tbl_users set u_name = '"+new_name+"' where u_username ='"+username_+"'"
        try:
            obj[1].execute(query)
            obj[0].commit()
            
            return 1
        except:
            obj[0].rollback()
            return 0
        finally:
            obj[1].close()
            obj[0].close()
                
        return 0
        


    def updatePwd(self, username_, new_pwd ):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query= "update tbl_users set u_pwd = '"+new_pwd+"' where u_username ='"+username_+"'"
        try:
            obj[1].execute(query)
            obj[0].commit()
            
            return 1
        except:
            obj[0].rollback()
            return 0
        finally:
            obj[1].close()
            obj[0].close()
                
        return 0
    

    def updateDept(self, username_, new_dept ):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query= "update tbl_users set u_dept = '"+new_dept+"' where u_username ='"+username_+"'"
        try:
            obj[1].execute(query)
            obj[0].commit()
            
            return 1
        except:
            obj[0].rollback()
            return 0
        finally:
            obj[1].close()
            obj[0].close()
                
        return 0

    def updateEmail(self, username_, new_email ):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query= "update tbl_users set u_email = '"+new_email+"' where u_username ='"+username_+"'"
        try:
            obj[1].execute(query)
            obj[0].commit()
            
            return 1
        except:
            obj[0].rollback()
            return 0
        finally:
            obj[1].close()
            obj[0].close()
                
        return 0

    def updatePhone(self, username_, new_phone ):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query= "update tbl_users set u_phone = '"+new_phone+"' where u_username ='"+username_+"'"
        try:
            obj[1].execute(query)
            obj[0].commit()
            
            return 1
        except:
            obj[0].rollback()
            return 0
        finally:
            obj[1].close()
            obj[0].close()
                
        return 0    
      
   
    def fetch_all_users(self):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query= "select * from tbl_users"
        try:
            obj[1].execute(query)
            a = obj[1].fetchall()
            lst =[]
            for x in a:
                d = {}
                d['Uname'] = x[0]
                d['Pwd'] = x[1]
                d['Name'] = x[2]
                d['Dept'] = x[3]
                d['Email'] = x[4]
                d['Phone'] = x[5]
                lst.append(d)
                
        except:
            print("error in fetching data in fetch_all_td()")
        #print(lst)
        return lst
        
        
    
    def delete_user(self, user_name):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query = "Delete from tbl_users where u_username = '"+user_name+"'"
        try:
            obj[1].execute(query)
            
            obj[0].commit()
            
            return 1
        except:
            obj[0].rollback()
            return 0
        finally:
            obj[1].close()
            obj[0].close()
