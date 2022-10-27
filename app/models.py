import datetime
import email
from sqlite3 import Timestamp
from turtle import st
from unicodedata import category
import uuid
from xmlrpc.client import DateTime
from cassandra.cqlengine import columns
from cassandra.cqlengine import models
from click import password_option
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# create user model
class CreateUser(BaseModel):
    __keyspace__ = "event_app" 
    user_id : str = Field(default_factory=uuid.uuid1)
    email : EmailStr = Field(default=None, unique= True)
    username : str = Field(default=None, unique= True)
    fullname : str = Field(default=None)
    phone_number : str = Field(default=None)
    password :  str = Field(default=None)
    business_name : str = Field(default=None)
    sector : str = Field(default=None)
   
#    user schema
    class Config:
        the_schema = {
            "user_demo" : {
                "email":"rectordev@gmail.com",
                "username":"rector",
                "fullname":"jerry jay",
                "phone_number":"09079927992",
                "password":"rector123",
                "business_name":"rectordev limited",
                "email":"technology",
                  
            }
        }

#create login model
class UserLogin(BaseModel):
    usernameOrEmail : str = Field(default=None)
    password :  str = Field(default=None)

#login schema 
    class Config:
        the_schema = {
            "login_demo" : {
                "email":"rectordev@gmail.com",
                "username":"rector",
                "password":"rector123",   
                
            }
        }
        
#create event model   
class CreateEvent(BaseModel):
    __keyspace__ = "event_app" 
    event_id : str = Field(default_factory=uuid.uuid1)
    user_id : str = Field(default_factory=uuid.uuid1)
    event_name : str = Field(default=None)
    event_organizer :  str = Field(default=None)
    event_type : str = Field(default=None)
    event_category : str = Field(default=None)
    event_tags :  str = Field(default=None)
    event_location : str = Field(default=None)
    event_datetime : datetime = Field(default_factory=datetime.now)
    
    
    # event schema
    class Config:
            the_schema = {
                "event_demo" : {
                    "event_name":"suya night",
                    "event_organizer":"rector",
                    "event_type":"birthday party",
                    "event_category":"personal",
                    "event_tags":"rector123",
                    "event_location":"Minna",
                    "event_datetime": "2021-09-09 09:09:09",      
                }
            }       
  
    
        

    
        
    
         
    
 