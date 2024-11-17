import mysql.connector
import pandas as pd
import random
class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "website")
            self.mycursor = self.conn.cursor()
        except Exception as e:
            print("Can't connect with Database bacause ...." , e)
        else:
            print("Connection Successfully...")
    
    def push(self , row , count , total):
        try:
            self.mycursor.execute("""
                              INSERT INTO `scrapped_websites` (topic , link , content) VALUES ('{}' , '{}' , '{}' )
                              """.format(row[1] , row[2] , row[3]))
            self.conn.commit()
        except Exception as e:
            print(f"Can't insert the row{ count} Because " , e)
        else:
            print(f"row inserted row {count} / {total}")
        
    def pop(self , numRow , maxLimit):
        data = []
        while True:    
            try:
                rand_int = random.randint(0 , maxLimit)
                self.mycursor.execute("""
                                      SELECT * FROM `scrapped_websites` WHERE id = {}
                                      """.format(rand_int))
                values = self.mycursor.fetchall()
                data.append(values if values else None)
                
            except Exception as e:
                print("Can't fetch values for a row because " , e)
                
            if len(data) >= numRow:
                break 
        return data
            
        