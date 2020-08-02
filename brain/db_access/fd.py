# -*- coding: utf-8 -*-
"""
Created on Sat Aug 01 2020

@author: Team Alpha Squad
"""


class FdObj():
    def __init__(self):
        self.fid = 0
        self.name = None
        self.image = None
        self.tid = 0
        self.file = None
        self.desc = None
        self.date = None
        self.result_page = None
  
  
class FdDAO:
    def getData(self, given_fd_id):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        mycursor = sql_con.getSQLConn()
        fd_obj = FdObj()
        query = "select * from tbl_feedbackdata where fd_id =" + str(given_fd_id)
        #print(query)
        if mycursor[1].execute(query) !=0:
            
            a = mycursor[1].fetchall()[0]
            fd_obj.fid = a[0]
            fd_obj.name = a[1]
            fd_obj.image = a[2]
            fd_obj.tid = a[3]
            fd_obj.file = a[4]
            fd_obj.desc = a[5]
            fd_obj.date = a[6]
            fd_obj.result_page = a[7]
            mycursor[1].close()
            mycursor[0].close()
            return fd_obj
        else: 
            print("No Such ID Present")
            
        return 0

        
    def getFileNamebyID(self, given_fd_id):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        mycursor = sql_con.getSQLConn()
        query = "select fd_file from tbl_feedbackdata where fd_id = '" + str(given_fd_id)+"'"
        if mycursor[1].execute(query) !=0:           
            a = mycursor[1].fetchall()[0]
            fd_file = a[0]
            mycursor[1].close()
            mycursor[0].close()
            return fd_file
        else: 
            print("No Such File Present")
            mycursor[1].close()
            mycursor[0].close()       
        return "TD20200502024521.json"        
    


    def setData(self, name, img, tid, file, desc, date, res_page):
        fd_obj = FdObj()
        fd_obj.name = name
        fd_obj.image = img
        fd_obj.tid = tid
        fd_obj.file = file
        
        fd_obj.desc = desc
        
        fd_obj.date = date
        fd_obj.result_page = res_page
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query = "insert into tbl_feedbackdata (fd_name, fd_img, td_id, fd_file, fd_desc, upload_date, result_page) values('"+name+"', '"+img+"',"+str(tid)+" ,'"+file+"','"+desc+"','"+date+"','"+res_page+"')"
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
        
    def updateTrainingData(self, dataset_id, training_dataset_id):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query = "update tbl_feedbackdata set td_id ="+training_dataset_id+" where fd_id = "+dataset_id
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
        query = "update tbl_feedbackdata set fd_name = '"+new_name+"' where fd_id ="+str(dataset_id)
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
        query= "update tbl_feedbackdata set fd_image = '"+img_url+"' where fd_id ="+str(dataset_id)
       # print(query)
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
        query= "update tbl_feedbackdata set fd_desc = '"+new_desc+"' where fd_id ="+str(dataset_id)
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
   
    def fetch_all_fd(self):
        from db_access.config import SQLConn
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        query= "select fd_id , fd_name, fd_img from tbl_feedbackdata"
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
            print("error in fetching data in fetch_all_fd()")
        return lst
        
        
    
    def delete_dataset(self, dataset_id, file_path, img_path, result_path, file_name):
        from db_access.config import SQLConn
        import os, re
        sql_con = SQLConn()
        obj = sql_con.getSQLConn()
        if self.getData(dataset_id) !=0:
            if os.path.exists(img_path):
              os.remove(img_path)
            else:
              print("The Image file does not exist")
              
            if os.path.exists(file_path):
              os.remove(file_path)
            else:
              print("The Feedback file does not exist")
            
            
            file_name = re.sub(".json", "", file_name)
            
            if os.path.exists(result_path+str(file_name)+"_Individual_Comment_Ratings.xlsx"):
              os.remove(result_path+str(file_name)+"_Individual_Comment_Ratings.xlsx")
            else:
              print("The Individual Review (.xlsx) file does not exist")
            
            if os.path.exists(result_path+str(file_name)+"_Individual_Comment_Ratings.csv"):
              os.remove(result_path+str(file_name)+"_Individual_Comment_Ratings.csv")
            else:
              print("The Individual Review (.csv) file does not exist")
              
            if os.path.exists(result_path+str(file_name)+"_Aspect_Based_Analysis.xlsx"):
              os.remove(result_path+str(file_name)+"_Aspect_Based_Analysis.xlsx")
            else:
              print("The Aspect Based Analysis (.xlsx) file does not exist")
              
            if os.path.exists(result_path+str(file_name)+"_Aspect_Based_Analysis.csv"):
              os.remove(result_path+str(file_name)+"_Aspect_Based_Analysis.csv")
            else:
              print("The Aspect Based Analysis (.csv) file does not exist")
              
            if os.path.exists(result_path+str(file_name)+"_Progress_Timeline.xlsx"):
              os.remove(result_path+str(file_name)+"_Progress_Timeline.xlsx")
            else:
              print("The Progress Timeline (.xlsx) file does not exist")
              
            if os.path.exists(result_path+str(file_name)+"_Progress_Timeline.csv"):
              os.remove(result_path+str(file_name)+"_Progress_Timeline.csv")
            else:
              print("The Progress Timeline (.csv) file does not exist")
            
            if os.path.exists(result_path+str(file_name)+"_Suggestions.json"):
              os.remove(result_path+str(file_name)+"_Suggestions.json")
            else:
              print("The Suggestion (.json) file does not exist")
            
            if os.path.exists(result_path+str(file_name)+".json"):
              os.remove(result_path+str(file_name)+".json")
            else:
              print("The Sentiment rated JSON file (.json) does not exist")
            

            query = "Delete from tbl_feedbackdata where fd_id ="+str(dataset_id)
            
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
        else:
            print("No Such Dataset to Delete")            
        return 0
    
    
    def delete_cloud_files(self, file_path, img_path, result_path, file_name):
        import os, re
        if os.path.exists(img_path):
          os.remove(img_path)
        else:
          print("The Image file does not exist")
          
        if os.path.exists(file_path):
          os.remove(file_path)
        else:
          print("The Feedback file does not exist")
        
        
        file_name = re.sub(".json", "", file_name)
        
        if os.path.exists(result_path+str(file_name)+"_Individual_Comment_Ratings.xlsx"):
          os.remove(result_path+str(file_name)+"_Individual_Comment_Ratings.xlsx")
        else:
          print("The Individual Review (.xlsx) file does not exist")
        
        if os.path.exists(result_path+str(file_name)+"_Individual_Comment_Ratings.csv"):
          os.remove(result_path+str(file_name)+"_Individual_Comment_Ratings.csv")
        else:
          print("The Individual Review (.csv) file does not exist")
          
        if os.path.exists(result_path+str(file_name)+"_Aspect_Based_Analysis.xlsx"):
          os.remove(result_path+str(file_name)+"_Aspect_Based_Analysis.xlsx")
        else:
          print("The Aspect Based Analysis (.xlsx) file does not exist")
          
        if os.path.exists(result_path+str(file_name)+"_Aspect_Based_Analysis.csv"):
          os.remove(result_path+str(file_name)+"_Aspect_Based_Analysis.csv")
        else:
          print("The Aspect Based Analysis (.csv) file does not exist")
          
        if os.path.exists(result_path+str(file_name)+"_Progress_Timeline.xlsx"):
          os.remove(result_path+str(file_name)+"_Progress_Timeline.xlsx")
        else:
          print("The Progress Timeline (.xlsx) file does not exist")
          
        if os.path.exists(result_path+str(file_name)+"_Progress_Timeline.csv"):
          os.remove(result_path+str(file_name)+"_Progress_Timeline.csv")
        else:
          print("The Progress Timeline (.csv) file does not exist")
        
        if os.path.exists(result_path+str(file_name)+"_Suggestions.json"):
          os.remove(result_path+str(file_name)+"_Suggestions.json")
        else:
          print("The Suggestion (.json) file does not exist")
        
        if os.path.exists(result_path+str(file_name)+".json"):
          os.remove(result_path+str(file_name)+".json")
        else:
          print("The Sentiment rated JSON file (.json) does not exist")

        return 0
        