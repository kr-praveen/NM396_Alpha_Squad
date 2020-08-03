# -*- coding: utf-8 -*-
"""
Created on Sat Aug 01 2020

@author: Team Alpha Squad
"""

class TdObj():
    def __init__(self):
        self.id = 0
        self.name = None
        self.image = None
        self.file = None
        self.storage_type = 0
        self.desc = None
        self.model = None
        self.date = None
        self.accuracy = 0.0

    
class TdDAO:
    def getData(self, given_td_id):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        mycursor = sql_con.getSQLConn()
        td_obj = TdObj()
        query = "select * from tbl_trainingdata where td_id =" + str(given_td_id)
        if mycursor[1].execute(query) !=0:
            
            a = mycursor[1].fetchall()[0]
            td_obj.id = a[0]
            td_obj.name = a[1]
            td_obj.image = a[2]
            td_obj.file = a[3]
            td_obj.storage_type = a[4]
            td_obj.desc = a[5]
            td_obj.model = a[6]
            td_obj.date = a[7]
            td_obj.accuracy = a[8]
            mycursor[1].close()
            mycursor[0].close()
            return td_obj
        else: 
            print("No Such ID Present")
            
        return 0
        
    def getIDbyFileName(self, given_td_file_name):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        mycursor = sql_con.getSQLConn()
        query = "select td_id from tbl_trainingdata where td_file = '" + str(given_td_file_name)+"'"
        if mycursor[1].execute(query) !=0:           
            a = mycursor[1].fetchall()[0]
            td_id = a[0]
            mycursor[1].close()
            mycursor[0].close()
            return td_id
        else: 
            print("No Such File Present")
            mycursor[1].close()
            mycursor[0].close()
            
        return 0   


    def getFileNamebyID(self, given_td_id):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        mycursor = sql_con.getSQLConn()
        query = "select td_file from tbl_trainingdata where td_id = '" + str(given_td_id)+"'"
        if mycursor[1].execute(query) !=0:           
            a = mycursor[1].fetchall()[0]
            td_file = a[0]
            mycursor[1].close()
            mycursor[0].close()
            return td_file
        else: 
            print("No Such File Present")
            mycursor[1].close()
            mycursor[0].close()       
        return "TD20200309210544.json"
        
    
    def setData(self, name, img, file, storage_type, desc, model, date, acc):
        td_obj = TdObj()
        td_obj.name = name
        td_obj.image = img
        td_obj.file = file
        td_obj.storage_type = storage_type
        td_obj.desc = desc
        td_obj.model = model
        td_obj.date = date
        td_obj.accuracy = acc
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query = "insert into tbl_trainingdata (td_name, td_img, td_file, storage_type, td_desc, td_model, upload_date, model_accuracy) values('"+name+"', '"+img+"', '"+file+"',"+str(storage_type)+",'"+desc+"','"+model+"','"+date+"','"+str(acc)+"')"
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
        
        
    
    def updateName(self, dataset_id, new_name ):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query= "update tbl_trainingdata set td_name = '"+new_name+"' where td_id ="+str(dataset_id)
        #print(query)
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
        
            
      
    def updateImage(self, dataset_id, img_url):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query= "update tbl_trainingdata set td_image = '"+img_url+"' where td_id ="+str(dataset_id)
        #print(query)
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
        
    def updateDesc(self, dataset_id, new_desc):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query= "update tbl_trainingdata set td_desc = '"+new_desc+"' where td_id ="+str(dataset_id)
        #print(query)
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
    
    def updateModel(self, dataset_json_file, new_model, new_accuracy):
        dataset_id = self.getIDbyFileName(dataset_json_file)
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query1= "update tbl_trainingdata set td_model = '"+str(new_model)+"' where td_id ="+str(dataset_id)
        query2= "update tbl_trainingdata set model_accuracy = '"+str(new_accuracy)+"' where td_id ="+str(dataset_id)
        #print(query)
        try:
            obj[1].execute(query1)
            obj[1].execute(query2)
            obj[0].commit()
            
            return 1
        except:
            obj[0].rollback()
            return 0
        finally:
            obj[1].close()
            obj[0].close()
                
        return 0
    
   
    def fetch_all_td(self):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query= "select td_id , td_name , td_img from tbl_trainingdata"
        try:
            obj[1].execute(query)
            a = obj[1].fetchall()
            lst =[]
            for x in a:
                d = {}
                d['ID'] = x[0]
                d['Name'] = x[1]
                d['Image_URL'] = x[2]
                lst.append(d)
                
        except:
            print("error in fetching data in fetch_all_td()")
        #print(lst)
        return lst
        
        
    
    def delete_dataset(self, dataset_id, file_path, img_path, model_path, token_path):
        from db_access.config import SQLConn
        import os
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        if self.getData(dataset_id) !=0:
            if os.path.exists(img_path):
              os.remove(img_path)
            else:
              print("The image does not exist")
            if os.path.exists(file_path):
              os.remove(file_path)
            else:
              print("The file does not exist")
            if os.path.exists(model_path):
              os.remove(model_path)
            else:
              print("The model (pkl file) does not exist")
            if os.path.exists(token_path):
              os.remove(token_path)
            else:
              print("The token does not exist")
              
            query1 ="Update tbl_feedbackdata set td_id = "+str(sql_con.default_primary_key)+" where td_id = "+str(dataset_id)
            query2 = "Delete from tbl_trainingdata where td_id ="+str(dataset_id)
            
            try:
                obj[1].execute(query1)
                obj[1].execute(query2)
                
                obj[0].commit()
                
                return 1
            except:
                obj[0].rollback()
                return 0
            finally:
                obj[1].close()
                obj[0].close()
        else:
            print("No Such Dataset to Delete")            
        return 0
    