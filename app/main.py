from asyncio import events
from datetime import datetime
import json
import re
import uuid
import bcrypt
import uvicorn
from fastapi import Body, FastAPI, Depends
from app.db import get_session
from app.models import CreateUser, UserLogin, CreateEvent
from app.auth.jwt_handler import signJWT
from app. auth .jwt_bearer import jwtBearer

app = FastAPI()


#check if username already in the database
def check_username(username):
    length = len(get_session().execute("""SELECT * FROM users WHERE username = %s ALLOW FILTERING;""", (username,)).all())
    if length == 0:
        return False
    else:
        return True
    
#check if email already exist in the database
def check_email(email):
    length = len(get_session().execute("""SELECT * FROM users WHERE email = %s ALLOW FILTERING;""", (email, )).all())
    if length == 0:
        return False
    else:
        return True      

# defining a function to check if required fields are present
def required_fields(user,path):
   match path:
       case "signup":
           if user.username == None or len(user.username) == 0:
               return {"message" : "Username is required"}
           if user.email == None:
               return {"message" : "Email is required"}
           if user.password == None or len(user.password) < 6:
               return {"message" : "Password is required"}
           if user.fullname == None or len(user.fullname) == 0:
               return {"message" : "Fullname is required"}
           if user.phone_number == None or len(user.phone_number) < 11:
               return {"message" : "Phone number is required"}
           if user.business_name == None or len(user.business_name) == 0:
               return {"message" : "Business name is required"}
           if user.sector == None or len(user.sector) == 0:
               return {"message" : "Sector is required"}
           return True
       
       case "login":
           if user.usernameOrEmail == None or len(user.usernameOrEmail) == 0:
               return {"message" : "Username or Email is required"}
           if user.password == None or len(user.password) < 6:
               return {"message" : "Password is required"}
           return True
       
       case "create_event":
           if user.event_name == None or len(user.event_name) == 0:
               return {"message" : "Event name is required"}
           if user.event_organizer == None or len(user.event_organizer) == 0:
               return {"message" : "Event organizer is required"}
           if user.event_type == None or len(user.event_type) == 0:
               return {"message" : "Event type is required"}
           if user.event_category == None or len(user.event_category) == 0:
               return {"message" : "Event category is required"}
           if user.event_tags == None or len(user.event_tags) == 0:
               return {"message" : "Event tags is required"}
           if user.event_location == None or len(user.event_location) == 0:
               return {"message" : "Event location is required"}
           if user.event_datetime == None :
               return {"message" : "Event datetime is required"}
           return True
           
        

# User Signup [create a user]
@app.post("/users/signup", tags=["user"])
def user_signup(user : CreateUser=Body(default=None)):
    
    #check if required fields are present
    check_true = required_fields(user, "signup")
    
    if check_true == True:
        
        
        # check if username already taken
        user_exist = check_username(user.username)
        if user_exist:
            return {"message" : "Username already exist"}
        # check if email already taken
        user_exist = check_email(user.email)
        if user_exist:
            return {"message" : "Email already exist"}
        
        # hash password
        password = bytes(user.password, "utf-8")
        user.password = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
        get_session().execute("""INSERT INTO users ("user_id", "email", "username", "fullname", "phone_number", "password", "business_name", "sector") VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                            """, (str(uuid.uuid4()), user.email, user.username, user.fullname, user.phone_number, user.password, user.business_name, user.sector))
        user_response = {
                "user_id": user.user_id,
                "email": user.email,
                "username": user.username,
                "fullname": user.fullname,
                "phone_number": user.phone_number,
                "business_name": user.business_name,
                "sector": user.sector
            }    
        return {"message" : "User created successfully", 
                "user": user_response,
                "token": signJWT(str(user)) 
                }
        
    else:
        return check_true
    
    
   
# User Login [login a user] 
@app.post("/users/login", tags=["user"])
def user_login(user : UserLogin=Body(default=None)):
    check_required = required_fields(user, "login")
    if check_required == True:
        username_exist = check_username(user.usernameOrEmail)
        email_exist = check_email(user.usernameOrEmail)
        if ((username_exist or email_exist)) == False:
            return {"message" : "Username or Email does not exist"}
        
  
  
        if(username_exist):
            user_result = get_session().execute("""SELECT * FROM users WHERE username = %s ALLOW FILTERING;""", (user.usernameOrEmail, )).one()
            if bcrypt.checkpw(bytes(user.password, "utf-8"), bytes(user_result["password"], "utf-8")):
                user_respone = {
                    "username" : user_result["username"],
                    "fullname" : user_result["fullname"],
                    "email" : user_result["email"],
                    "phone_number" : user_result["phone_number"], 
                    "business_name" : user_result["business_name"],                            
                    "sector" : user_result["sector"], 
                    "user_id": user_result["user_id"],
                }
                
                return {
                    "message" : "Login successful",
                    "user": user_respone,
                    "token": signJWT(str(user_result))
                }
           
        if(email_exist):
            user_result = get_session().execute("""SELECT * FROM users WHERE email = %s ALLOW FILTERING;""", (user.usernameOrEmail, )).one()
            if bcrypt.checkpw(bytes(user.password, "utf-8"), bytes(user_result["password"], "utf-8")):
                user_respone = {
                    "username" : user_result["username"],
                    "fullname" : user_result["fullname"],
                    "email" : user_result["email"],
                    "phone_number" : user_result["phone_number"], 
                    "business_name" : user_result["business_name"],                            
                    "sector" : user_result["sector"], 
                    "user_id": user_result["user_id"], 
                }
                
                return {
                    "message" : "Login successful",
                    "user": user_respone,
                    "token": signJWT(str(user_result))
                }
           
    else:
        return check_required
    
    
# Create Event [create an event]      
@app.post("/events/create", dependencies=[Depends(jwtBearer())], tags=["event"])
def create_event(event : CreateEvent=Body(default=None)):
    check_required = required_fields(event, "create_event")
    if check_required == True:
        event_timestamp = datetime.timestamp(event.event_datetime)
        datetime.fromtimestamp(event_timestamp)
        stmt = get_session().prepare("INSERT INTO events (event_id, user_id, event_name, event_organizer, event_type, event_category, event_tags, event_location, event_datetime) VALUES (?, ?, ?, ?, ?,?,?,?,?)IF NOT EXISTS")
        get_session().execute(stmt, [str(uuid.uuid4()), event.user_id, event.event_name, event.event_organizer, event.event_type, event.event_category, event.event_tags, event.event_location, event_timestamp])
        return {"message" : "Event created successfully"}  

    else:
        return check_required


# get all trending events
@app.get("/events/get", tags=["event"])
def get_event():
    event_result = get_session().execute("""SELECT * FROM events;""").all()
    return event_result


# get all trending events by id
@app.get("/events/get/{event_id}", tags=["event"])
def get_event_by_id(event_id):
    event_result = get_session().execute("""SELECT * FROM events WHERE event_id = %s ALLOW FILTERING;""", (event_id, )).one()
    return event_result


# get event by type
@app.get("/events/get/type/{event_type}", tags=["event"])
def get_event_by_type(event_type):
    event_result = get_session().execute("""SELECT * FROM events WHERE event_type = %s ALLOW FILTERING;""", (event_type, )).all()
    return event_result

  


# # get all upcoming events
@app.get("/events/get/upcoming/parties", tags=["event"])
def get_upcoming_event():
    nowtime =datetime.timestamp(datetime.now())
    stmt = get_session().prepare("SELECT * FROM events WHERE event_datetime > ? ALLOW FILTERING")
    results = get_session().execute(stmt, [nowtime])
    values = results.all()
    return values

# get all upcoming events by id
@app.get("/events/get/upcoming/parties/{event_id}", tags=["event"])
def get_upcoming_event_by_id(event_id):
    nowtime =datetime.timestamp(datetime.now())
    stmt = get_session().prepare("SELECT * FROM events WHERE event_datetime > ? AND event_id = ? ALLOW FILTERING")
    results = get_session().execute(stmt, [nowtime, event_id])
    values = results.one()
    return values

