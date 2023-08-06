import inspect
import sqlite3
from inspect import getframeinfo
from inspect import stack

#def debuginfo():
    #caller = getframeinfo(stack()[1][0])
    
    #return f"\n   File - {caller.filename} \n      Line - {caller.lineno}"

class view:
    def __init__(self, user_ID=None):
        self.user_ID = user_ID
        
    def wallet(self):
        #user ID has none
        if self.user_ID == None:
            print("user_ID")
        
        #User ID is there
        else:            
            conn = sqlite3.connect("economy.db")
            c = conn.cursor()
            
            c.execute(f"SELECT * FROM economy WHERE user_ID={self.user_ID}")
            
            items = c.fetchall()
            none = str(items)
            
            if none == "[]":
                return "0"
            
            else:
                for item in items:
                    wallet = item[1]
                    
                return wallet        

    def bank(self):
        #user ID has none
        if self.user_ID == None:
            print("user_ID")
        
        #User ID is there
        else:            
            conn = sqlite3.connect("economy.db")
            c = conn.cursor()
            
            c.execute(f"SELECT * FROM economy WHERE user_ID={self.user_ID}")
            
            items = c.fetchall()
            none = str(items)
            
            if none == "[]":
                return "0"
            
            else:
                for item in items:
                    bank = item[2]
                    
                return bank   
        
    def net(self):
        #user ID has none
        if self.user_ID == None:
            print("user_ID")
        
        #User ID is there
        else:            
            conn = sqlite3.connect("economy.db")
            c = conn.cursor()
            
            c.execute(f"SELECT * FROM economy WHERE user_ID={self.user_ID}")
            
            items = c.fetchall()
            none = str(items)
            
            if none == "[]":
                return "0"
            
            else:
                for item in items:
                    net = item[3]
                    
                return net   